# GNU-GPL license, v3 or later

import json
import re
import shutil
from copy import deepcopy
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pyzotero import zotero
from pyzotero.zotero_errors import UserNotAuthorised, PyZoteroError


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
        self.matched = ""
        self.isNew = datetime.now().strftime("%Y%m")[2:] == self.link[-10:-6]

    def __str__(self):
        return f"[Matched {self.matched}]\nTitle: {self.title}\nAuthors: {self.authors}\nAbstract: {self.abstract}\nLink: {self.link}"

    def search(self, author_list, term_list):
        if (not self.isNew) and (not preferences["MatchResubmissions"]): return False
        for author in author_list:
            if author in self.authors:
                self.matched = author
                return True
        for term in term_list:
            if term.lower() in self.title.lower() or term.lower() in self.abstract.lower():
                self.matched = term
                return True
        return False

    def zoterify(self, template, zlib, col):
        # add zotero item
        template = deepcopy(template)
        template['title'] = self.title
        template['url'] = self.link  # self.link[:18]+"pdf"+self.link[21:]
        template['collections'] = [col]
        template['libraryCatalog'] = "arXiv.org"
        template['abstractNote'] = str(self.abstract)
        template['creators'] = [deepcopy(template['creators'][0]) for i in range(len(self.authors))]
        template['extra'] = f"followXiv matched: {self.matched}"
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
    shutil.copy("sample_configuration.json", "configuration.json")
    print("Please set up configuration file `configuration.json`. It was prepopulated with some generic defaults :)")
    print("Exiting")
    exit()

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
    try:
        zcol = zlib.create_collections([collection])
    except UserNotAuthorised as auth_err:
        print(f"Authorization failed! {str(auth_err)}")
        print("Exiting")
        exit()
    except PyZoteroError as e:
        print(f"Zotero error: {e}")
        print("Exiting")
        exit()
    except:
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

    article_tops = soup.find_all('dt')
    articles = soup.find_all('dd')

    for (article, article_top) in zip(articles, article_tops):
        entries_list.append(
            Entry(get_title(article), get_authors(article), get_abstract(article), get_url(article_top)))
        if entries_list[-1].search(my_authors, my_keywords):
            matches.add(entries_list[-1])

# Search entries and write to output file
with open("output.txt", "w") as output_file:
    output_file.write(f"Matched {len(matches)} new articles from {len(entries_list)} total\n\n")
    output_file.write('\n\n'.join(str(entry) for entry in matches))

if use_zotero:
    template = zlib.item_template('Preprint')
    items = [entry.zoterify(template, zlib, zkey) for entry in matches]
    # zotero lets us batch create up to 50 objects per call, so if we somehow matched more than that, split the list up
    size = 50
    if len(items) > size:
        for i in range(0, len(items), size):
            zlib.create_items(items[i:i + size])
    else:
        zlib.create_items(items)
