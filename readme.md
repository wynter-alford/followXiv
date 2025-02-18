# followXiv.py

FollowXiv is a simple Python script for monitoring arXiv for new papers by specified authors or relating to specified topics. The tool filters papers on the .../new field on arXiv based on specified authors and keywords in the title or abstract. I hope to expand this into a tool that will run regularly, with a nice UI (possibly interacting with Zotero) allowing one to easily 'follow' certain authors or topics on arXiv.

## Usage:

User preferences are specified in the ``configuration.json`` file, which allows inputs of the following types:

- Feeds: which pages on arXiv to pull content from (currently just .../new)
- Authors: papers by any listed author will be selected by the filter 
- Keywords: papers whose title or abstract contain any of the keywords will be selected by the filter

All steps are then performed by the followXiv.py script. Papers found by the filter are saved to ``output.txt`` with their title, authors, abstract, and url.

A way to make this run every weekday morning on Linux/Unix systems is to run ``crontab -e`` and then paste ``0 9 * * 1-5 cd [installation path]/followXiv && git stash && git pull && python3 followXiv.py && mv output.txt "$(date -I).txt"``. There are probably other clever options that I haven't thought of.

## Potential features to add:

- **Fuzzy author matching**: Currently, authors will only match if they appear exactly as entered in the json file. So "Wynter R Alford" will not match "Wynter Alford" or "Wynter R. Alford".
- **"And" conditions:** Allow conditions like "Author 1 AND Author 2" or "Keyword 1 AND Keyword 2 AND Keyword 3" for the filter
- **Some kind of UI** that isn't just the python script and a json file.
- **"Run Daily" functionality** or customizable repetition that is part of the package, rather than relying on setting up ``cron``.
- **Monitor for citations?**: Longer term, not sure how feasible this one is, but it would be nice to be able to flag papers that cite particular references.
- **Integration with Zotero?**: Longer term, I'd love to look into how Zotero plugins work and see if there's a way to add matching papers directly into a folder in Zotero.

Issues & PRs welcome.
