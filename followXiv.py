#! .venv/bin/python3

from bs4 import BeautifulSoup
import re
import json
import requests
import shutil

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
    
    def __str__(self):
        return f"[Matched {self.matched}]\nTitle: {self.title}\nAuthors: {self.authors}\nAbstract: {self.abstract}\nLink: {self.link}"
    
    def search(self, author_list, term_list):
        for author in author_list:
                    if author in self.authors:
                        self.matched = author
                        return True
        for term in term_list:
            if term.lower() in self.title.lower() or term.lower() in self.abstract.lower():
                self.matched = term
                return True
        return False


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
my_feeds = config['Feeds']
my_authors = config['Authors']
my_keywords = config['Keywords']

entries_list = []

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


# Search entries and write to output file
output_file = open("output.txt", "w")

for entry in entries_list:
    if entry.search(my_authors, my_keywords):
        output_file.write(str(entry) + "\n\n")

output_file.close()
