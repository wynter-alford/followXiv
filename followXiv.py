#  followXiv.py    Copyright (C) 2025    Wynter Alford

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import re
# import shutil
from copy import deepcopy
from datetime import datetime, timedelta

try:
    import requests
    from bs4 import BeautifulSoup
    from pyzotero import zotero
    from pyzotero.zotero_errors import *
except ModuleNotFoundError as err:
    print(err)
    print("\nAn error occurred because a required package is missing. FollowXiv requires the following packages: requests, bs4, pyzotero. Please ensure they are all installed, then try again.")
    print("\nExiting")
    exit()


# Functions for processing html file
def get_authors(article):
    html_string = str(article)
    section = re.compile(r'<div class="list-authors">(.+?)</div>').findall(html_string)[0]
    pattern = re.compile(r'">(.+?)</a>')
    return pattern.findall(section)


def get_title(article):
    html_string = str(article)
    pattern = re.compile(r'class="descriptor">Title:</span>\s*(.*?)\s*</div>', re.DOTALL)
    return pattern.findall(html_string)


def get_abstract(article):
    html_string = str(article)
    pattern = re.compile(r'<p class="mathjax">\s*(.*?)\s*</p>', re.DOTALL)
    return pattern.findall(html_string)


def get_url(article):
    html_string = str(article)
    pattern = re.compile(r'arXiv:(.+?)\n')
    return "https://arxiv.org/abs/" + pattern.findall(html_string)[0]


# Functions for processing individual entries
class Entry:

    def __init__(self, title, authors, abstract, link):
        self.title = title[0]
        self.authors = authors
        self.abstract = abstract[0]
        self.link = link
        self.matches = []

    def __str__(self):
        return f"[Matched {self.list_matches()}]\nTitle: {self.title}\nAuthors: {self.authors}\nAbstract: {self.abstract}\nLink: {self.link}"

    def list_matches(self):
        return ', '.join(self.matches)

    def search(self, author_list, term_list) -> bool:
        for author in author_list:
            if author in self.authors:
                self.matches.append(author)
        for term in term_list:
            if term.lower() in self.title.lower() or term.lower() in self.abstract.lower():
                self.matches.append(term)
        return len(self.matches) > 0

    def zoterify(self, template, col, zprefix):
        # add zotero item
        template = deepcopy(template)
        template['title'] = self.title
        template['url'] = self.link  # self.link[:18]+"pdf"+self.link[21:]
        template['collections'] = [col]
        template['libraryCatalog'] = "arXiv.org"
        template['abstractNote'] = str(self.abstract)
        template['creators'] = [deepcopy(template['creators'][0]) for i in range(len(self.authors))]
        template['date'] = datetime.now().strftime("%Y-%m-%d")
        template["accessDate"] = datetime.now().strftime("%Y-%m-%d")
        template['extra'] = f"{zprefix}: {self.list_matches()}"
        for i in range(len(self.authors)):
            splitname = self.authors[i].split()
            template['creators'][i]['lastName'] = splitname[-1]
            template['creators'][i]['firstName'] = " ".join(splitname[:-1])
        return template

    def __eq__(self, other):
        return self.link == other.link

    def __hash__(self):
        return hash(self.link)


## Main Program

# Load user configuration
try:
    config_file = open("configuration.json", "r")
except OSError:
    exec(open("followXiv-setup.py").read())
    config_file = open("configuration.json", "r")
    # shutil.copy("sample_configuration.json", "configuration.json")
    # print("Please set up configuration file `configuration.json`. It was prepopulated with some generic defaults :)")
    # print("Exiting")
    

config = json.load(config_file)

filters = config['Filters']
my_feeds = filters['Feeds']
my_authors = filters['Authors']
my_keywords = filters['Keywords']

preferences = config['Preferences']
use_zotero = preferences['UseZotero']

entries_list = []
matches = set()
config_file.close()

# Set up Zotero
if use_zotero:
    zinfo = config['Zotero']
    zlib = zotero.Zotero(zinfo['LibraryID'], zinfo['LibraryType'], zinfo['APIToken'])
    collection = {"name": datetime.now().strftime("%Y-%m-%d"), "parentCollection": zinfo['followXivCID']}
    zprefix = zinfo.get('ZoteroPrefix', 'fX') 
    try:
        zcol = zlib.create_collections([collection])
    except UserNotAuthorisedError as auth_err:
        print(f"Authorization failed! {str(auth_err)}")
        print("Exiting")
        exit()
    except PyZoteroError as e:
        print(f"Zotero error: {e}")
        print("Exiting")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        print(
            "Please make sure you have correctly specified your library ID, API token, and the collection ID in which followXiv should store its results.")
        print("Exiting")
        exit()
    zkey = zcol['successful']['0']['key']  # key for today's collection, to add stuff to

# Process feeds
for feed_name in my_feeds:

    # Obtain and parse html
    url = "https://arxiv.org/list/" + feed_name + "/new"
    feed = requests.get(url)
    soup = BeautifulSoup(feed.text, "html.parser")

    if not preferences["MatchResubmissions"]:
        try:
            resubmission_pattern = re.compile('Replacement submissions \\(showing ([1-9]{1,2})')
            resub_count_source = str(soup.find_all('h3'))
            num_resubmissions = int(resubmission_pattern.findall(resub_count_source)[0])
        except:
            num_resubmissions = 0
    else:
        num_resubmissions = 0

    article_tops = soup.find_all('dt')[:-num_resubmissions]
    articles = soup.find_all('dd')[:-num_resubmissions]

    for (article, article_top) in zip(articles, article_tops):
        entries_list.append(
            Entry(get_title(article), get_authors(article), get_abstract(article), get_url(article_top))
        )
        if entries_list[-1].search(my_authors, my_keywords):
            matches.add(entries_list[-1])

# Search entries and write to output file
with open("output.txt", "w") as output_file:
    output_file.write(f"Matched {len(matches)} new articles from {len(entries_list)} total\n\n")
    output_file.write('\n\n'.join(str(entry) for entry in matches))

if use_zotero:
    template = zlib.item_template('Preprint')
    items = [entry.zoterify(template, zkey, zprefix) for entry in matches]
    # zotero lets us batch create up to 50 objects per call, so if we somehow matched more than that, split the list up
    size = 50
    if len(items) > size:
        for i in range(0, len(items), size):
            # todo will this cause an indexing error?
            zlib.create_items(items[i:i + size])
    else:
        zlib.create_items(items)
