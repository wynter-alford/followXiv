# GNU-GPL license, v3 or later

from bs4 import BeautifulSoup
import re
import json
import requests
import shutil
from pyzotero import zotero
from datetime import datetime
from copy import deepcopy

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

    def zoterify(self, zlib, col):
        # add zotero item
        template = zlib.item_template('Preprint')
        template['title'] = self.title
        template['url'] = self.link # self.link[:18]+"pdf"+self.link[21:]
        template['collections'] = [col]
        template['libraryCatalog'] = "arXiv.org"
        template['abstractNote'] = f"[followXiv matched {self.matched}]\n\n {self.abstract}"
        template['creators'] = [deepcopy(template['creators'][0]) for i in range(len(self.authors))]
        for i in range(len(self.authors)):
            splitname = self.authors[i].split()
            template['creators'][i]['lastName'] = splitname[-1]
            template['creators'][i]['firstName'] = " ".join(splitname[:-1])
        resp = zlib.create_items([template])
        return resp


## Main Program

# Load user configuration
try:
    config_file = open("configuration.json", "r")
except:
     shutil.copy("sample_configuration.json", "configuration.json")
     print("Please set up configuration file `configuration.json`. It was prepopulated with some generic defaults :)")
     print("Exiting")
     exit()

config =  json.load(config_file)

filters = config['Filters']
my_feeds = filters['Feeds']
my_authors = filters['Authors']
my_keywords = filters['Keywords']

preferences = config['Preferences']

entries_list = []
matches_list = []
config_file.close()

# Set up Zotero
if preferences['UseZotero']:
    zinfo = config['Zotero']
    zlib = zotero.Zotero(zinfo['LibraryID'],zinfo['LibraryType'],zinfo['APIToken'])
    try:
        collection = {"name":datetime.now().strftime("%Y-%m-%d"), "parentCollection":zinfo['followXivCID']}
    except:
        print("Please make sure you have correctly specified your library ID, API token, and the collection ID in which followXiv should store its results.")
        print("Exiting")
        exit()
    zcol = zlib.create_collections([collection])
    zkey = zcol['successful']['0']['key'] # key for today's collection, to add stuff to

# Process feeds
for feed_name in my_feeds:

    # Obtain and parse html
    url = "https://arxiv.org/list/" + feed_name + "/new"
    feed = requests.get(url)
    soup = BeautifulSoup(feed.text, "html.parser")

    article_tops = soup.find_all('dt')
    articles = soup.find_all('dd')

    for i in range(len(articles)):
        entries_list.append(Entry(get_title(articles[i]), get_authors(articles[i]), get_abstract(articles[i]), get_url(article_tops[i])))
        if entries_list[-1].search(my_authors, my_keywords):
            matches_list.append(entries_list[-1])


# Search entries and write to output file
output_file = open("output.txt", "w")
output_file.write(f"Matched {len(matches_list)} new articles from {len(entries_list)} total\n\n")

for entry in matches_list:
    output_file.write(str(entry) + "\n\n")
    if preferences['UseZotero']:
        entry.zoterify(zlib, zkey)

output_file.close()
