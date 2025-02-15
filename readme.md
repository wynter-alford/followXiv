# followXiv.py

FollowXiv is a simple Python script for monitoring arXiv for new papers by specified authors or relating to specified topics. The tool filters papers on the .../new field on arXiv based on specified authors and keywords in the title or abstract. I hope to expand this into a tool that will run regularly, with a nice UI (possibly interacting with Zotero) allowing one to easily 'follow' certain authors or topics on arXiv.

## Usage:

User preferences are specified in the ``configuration.json`` file, which allows inputs of the following types:

- Feeds: which pages on arXiv to pull content from (currently just .../new)
- Authors: papers by any listed author will be selected by the filter 
- Keywords: papers whose title or abstract contain any of the keywords will be selected by the filter

All steps are then performed by the followXiv.py script. Papers found by the filter are saved to ``output.txt`` with their title, authors, abstract, and url.

## Potential features to add:

- **Fuzzy author matching**: Currently, authors will only match if they appear exactly as entered in the json file. So "Wynter R Alford" will not match "Wynter Alford" or "Wynter R. Alford".
- **Some kind of UI** that isn't just the python script and a json file.
- **Integration with Zotero?**: Longer term, I'd love to look into how Zotero plugins work and see if there's a way to add matching papers directly into a folder in Zotero.

Issues & PRs welcome.