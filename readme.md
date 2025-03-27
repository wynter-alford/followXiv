# followXiv.py

FollowXiv is a simple Python script for monitoring arXiv for new papers by specified authors or relating to specified topics. The tool filters papers on the .../new field on arXiv based on specified authors and keywords in the title or abstract. I hope to expand this into a tool that will run regularly, with a nice UI (possibly interacting with Zotero) allowing one to easily 'follow' certain authors or topics on arXiv.

## Setup:

Before running, ensure that all required packages are installed (see ``requirements.txt``). On first usage, first run the ``followXiv-setup.py`` script. This will take you through an interactive setup tool to choose which feeds to follow, choose which authors and keywords to monitor for, and set up Zotero integration if desired. After this script runs, it will create a file ``configuration.json`` to contain your preferences. To update these preferences, run the ``followXiv-setup.py`` script again or edit the json file directly.

## Usage

To use, run the followXiv.py script. Papers found by the filter are saved to ``output.txt`` with their title, authors, abstract, url, and list of matched authors and keywords. If Zotero is enabled, papers are also added to a Zotero subcollection under the specified followXiv collection whose name is today's date.

A way to make this run every weekday morning on Linux/Unix systems is to run ``crontab -e`` and then paste ``0 9 * * 1-5 cd [PATH-TO-FOLLOWXIV]/followXiv && git reset --hard HEAD && git pull && [PATH-TO-ENVIRONMENT]/python3 followXiv.py && mv output.txt "$(date -I).txt" >/dev/null``. A similar method for Windows probably exists. The '9' as the second number means run at 09:00; this time can be changed but should be set so that your computer reliably has internet access at the time or it will return an error.

## Zotero Integration:

This tool can be used with Zotero by setting the following in ``configuration.json`` or in the interactive setup tool:
- Set ``UseZotero`` to ``True`` under Preferences
- Under Zotero, specify your library ID and library type (either ``"user"`` or ``"group"``)
- Obtain an API token and specify that under Zotero as well.
- Create a collection in your library for followXiv to store its output in, and specify that collection's ID under ``followXivCID``

Your library ID and API tokens can be managed at https://www.zotero.org/settings/keys. Your collection ID can be found by navigating to that collection in the web version of Zotero. Zotero integration relies heavily on the Pyzotero package: http://doi.org/10.5281/zenodo.2917290

## Potential features to add:

- **Fuzzy author matching**: Currently, authors will only match if they appear exactly as entered in the json file. So "Wynter R Alford" will not match "Wynter Alford" or "Wynter R. Alford".
- **"And" conditions:** Allow conditions like "Author 1 AND Author 2" or "Keyword 1 AND Keyword 2 AND Keyword 3" for the filter
- **Some kind of UI** that isn't just the python script and a json file.
- **"Run Daily" functionality** or customizable repetition that is part of the package, rather than relying on setting up ``cron``.
- **Improvements to followXiv-setup** including an option to help set up ``cron`` and greater setup customizability

Issues & PRs welcome.
