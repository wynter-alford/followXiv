import shutil
import textwrap
import json

TERMINAL_WIDTH, TERMINAL_HEIGHT = shutil.get_terminal_size()

# Check whether setup has been performed before
try:
    config_file = open("configuration.json", "r")
    NEW_SETUP = False
    CONFIGURATION = json.load(config_file)
    config_file.close()
except OSError:
    config_file = open("sample_CONFIGURATION.json", "r")
    CONFIGURATION = json.load(config_file)
    config_file.close()
    NEW_SETUP = True

def tprint(text):
    print(textwrap.fill(text, width=TERMINAL_WIDTH))

def print_space():
    tprint("\n")
    tprint("-"*TERMINAL_WIDTH)
    tprint("\n")


# Header and license information
def show_licensing():
    print_space()
    tprint("\n followXiv is (c) Wynter Alford, 2025, and licensed under the GNU GPL v3.0 license or later.\n")
    tprint("\n This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or(at your option) any later version.")
    tprint("\n This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n")
    tprint("\n You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.\n")

    i1 = input("\n To view the full license, enter 'l' (or view the file LICENSE.md). To continue with setup, press enter. To exit, enter 'q': ")
    if i1 == 'l' or i1 == 'L':
        print("\n\n\n\n\n")
        with open('LICENSE.md', 'r') as f:
            print(f.read())
        
        i2 = input("\n Press enter to continue with setup or 'q' to exit: ")
        if i2 == 'q' or i2 == 'Q':
            print("Exiting setup.")
            exit()
        else:
            print("Continuing with setup.\n")
    elif i1 == 'q':
        print("Exiting setup.")
        exit()
    else:
        print("Continuing with setup.\n")


# if not new, ask what to update
def reconfigure():
    while True:
        print_space()
        tprint("\nEnter an option to configure:")
        tprint("\n1. Change feed list")
        tprint("\n2. Change author list")
        tprint("\n3. Change keyword list")
        tprint("\n4. Change Zotero settings")
        tprint("\n5. Change other settings")
        tprint("\n6. Set followXiv to run daily using cron")
        tprint("\n0. Proceed with full interactive setup")
        tprint("\nOr enter 'l' to view licensing information, 's' to save and exit, or 'q' to quit without saving.")
        i3 = input("\nEnter a choice: ")
        if i3 == "1":
            config_feed_list()
        elif i3 == "2":
            config_author_list()
        elif i3 == "3":
            config_keyword_list()
        elif i3 == "4":
            config_zotero()
        elif i3 == "5":
            config_other()
        elif i3 == "6":
            config_crontab()
        elif i3 == "0":
            print_space()
            print("Proceeding with full interactive setup.")
            first_configure()
        elif i3 == "q":
            print("Exiting setup. Your changes will not be saved.")
            exit()
        elif i3 == "s":
            save_and_exit()
        elif i3 == "l":
            show_licensing()
        else:
            print("Invalid choice. Please try again.")

# if new, go through the whole setup
def first_configure():
    show_licensing()
    config_feed_list()
    config_author_list()
    config_keyword_list()
    config_crontab()
    config_zotero()
    config_other()
    tprint("\n\n\n Setup complete! Enter 'a' to adjust settings further, 's' to save and exit, or 'q' to quit without saving.")
    while True:
        i4 = input("\nEnter a choice: ")
        if i4 == "a":
            reconfigure()
        elif i4 == "s":
            save_and_exit()
        elif i4 == "q":
            print("Exiting setup.")
            exit()
        else:
            print("Invalid choice.")
            reconfigure()

# Configure feed list
def config_feed_list():
    print_space()
    if NEW_SETUP:
        tprint("A sample feed list has been provided. \n")
    while True:
        tprint("Your current feed list is:\n")
        feeds = CONFIGURATION["Filters"]["Feeds"]
        for ind in range(len(feeds)):
            tprint(feeds[ind])
        tprint("\nChoose an option from the following:")
        tprint("1. Add a new feed")
        tprint("2. Remove a feed")
        tprint("3. Remove all feeds")
        tprint("Or press enter to continue with setup.")
        i5 = input("\nEnter a choice: ")
        if i5 == "1":
            new_feed = input("\nEnter the new feed name: ")
            feeds.append(new_feed)
            CONFIGURATION["Filters"]["Feeds"] = feeds
            print("\nFeed added.\n\n")
            print("-"*TERMINAL_WIDTH)
        elif i5 == "2":
            tprint("Your current feed list is:\n")
            for ind in range(len(feeds)):
                tprint(str(ind+1)+". "+feeds[ind])
            i6 = input("\nEnter the number of the feed to remove: ")
            try:
                i6 = int(i6)
                if i6 > 0 and i6 <= len(feeds):
                    feeds.pop(i6-1)
                    CONFIGURATION["Filters"]["Feeds"] = feeds
                    print("\nFeed removed.")
            except:
                print("\nInvalid choice.")
            else:
                print("\nInvalid choice.")
        elif i5 == "3":
            feeds.clear()
            CONFIGURATION["Filters"]["Feeds"] = feeds
            print("\nAll feeds removed.")
        elif i5 == "":
            return
        else:
            print("\nInvalid choice.")
        print_space()


def config_author_list():
    if NEW_SETUP:
        tprint("A sample author list has been provided. \n")
    while True:
        tprint("Your current author list is:\n")
        authors = CONFIGURATION["Filters"]["Authors"]
        for ind in range(len(authors)):
            tprint(authors[ind])
        tprint("\nChoose an option from the following:")
        tprint("1. Add a new author")
        tprint("2. Remove a author")
        tprint("3. Remove all authors")
        tprint("Or press enter to continue with setup.")
        i5 = input("\nEnter a choice: ")
        if i5 == "1":
            new_author = input("\nEnter the new author name: ")
            authors.append(new_author)
            CONFIGURATION["Filters"]["Authors"] = authors
            print("\nFeed added.\n\n")
            print("-"*TERMINAL_WIDTH)
        elif i5 == "2":
            tprint("Your current author list is:\n")
            for ind in range(len(authors)):
                tprint(str(ind+1)+". "+authors[ind])
            i6 = input("\nEnter the number of the author to remove: ")
            try:
                i6 = int(i6)
                if i6 > 0 and i6 <= len(authors):
                    authors.pop(i6-1)
                    CONFIGURATION["Filters"]["Authors"] = authors
                    print("\nFeed removed.")
            except:
                print("\nInvalid choice.")
            else:
                print("\nInvalid choice.")
        elif i5 == "3":
            authors.clear()
            CONFIGURATION["Filters"]["Authors"] = authors
            print("\nAll authors removed.")
        elif i5 == "":
            return
        else:
            print("\nInvalid choice.")
        print_space()


def config_keyword_list():
    if NEW_SETUP:
        tprint("A sample keyword list has been provided. \n")
    while True:
        tprint("Your current keyword list is:\n")
        keywords = CONFIGURATION["Filters"]["Keywords"]
        for ind in range(len(keywords)):
            tprint(keywords[ind])
        tprint("\nChoose an option from the following:")
        tprint("1. Add a new keyword")
        tprint("2. Remove a keyword")
        tprint("3. Remove all keywords")
        tprint("Or press enter to continue with setup.")
        i5 = input("\nEnter a choice: ")
        if i5 == "1":
            new_keyword = input("\nEnter the new keyword name: ")
            keywords.append(new_keyword)
            CONFIGURATION["Filters"]["Keywords"] = keywords
            print("\nFeed added.\n\n")
            print("-"*TERMINAL_WIDTH)
        elif i5 == "2":
            tprint("Your current keyword list is:\n")
            for ind in range(len(keywords)):
                tprint(str(ind+1)+". "+keywords[ind])
            i6 = input("\nEnter the number of the keyword to remove: ")
            try:
                i6 = int(i6)
                if i6 > 0 and i6 <= len(keywords):
                    keywords.pop(i6-1)
                    CONFIGURATION["Filters"]["Keywords"] = keywords
                    print("\nFeed removed.")
            except:
                print("\nInvalid choice.")
            else:
                print("\nInvalid choice.")
        elif i5 == "3":
            keywords.clear()
            CONFIGURATION["Filters"]["Keywords"] = keywords
            print("\nAll keywords removed.")
        elif i5 == "":
            return
        else:
            print("\nInvalid choice.")

def config_zotero():
    # Set up Zotero for the first time
    if NEW_SETUP:
        config_zotero_new()
        return

    # Adjust Zotero preferences
    elif not CONFIGURATION["Preferences"]["UseZotero"]:
        print_space()
        tprint("Zotero is currently disabled. Would you like to enable it?")
        i5 = input("\nEnter 'y' to enable Zotero or 'n' to keep it disabled: ")
    else:
        print_space()
        tprint("Zotero is currently enabled. Would you like to keep it enabled?")
        i5 = input("\n Enter 'y' to keep Zotero enabled, or 'n' to disable it: ")
    if i5 == 'n' or i5 == 'N':
        CONFIGURATION['Preferences']['UseZotero'] = False
        tprint("Zotero is now disabled.")
    elif i5 == 'y' or i5 == 'Y':
        CONFIGURATION['Preferences']['UseZotero'] = True
        tprint("Zotero is now enabled!")
        if CONFIGURATION["Zotero"]["LibraryID"] == 12345678:
            config_zotero_new()
            return
        
        while True:
            print_space()
            tprint("Your current Zotero settings are:")
            tprint(f"Library ID: {CONFIGURATION['Zotero']['LibraryID']}")
            tprint(f"API Token: {CONFIGURATION['Zotero']['APIToken']}")
            tprint(f"Library Type: {CONFIGURATION['Zotero']['LibraryType']}")
            tprint(f"Collection ID: {CONFIGURATION['Zotero']['followXivCID']}")
            tprint("\nChoose an option from the following:")
            tprint("1. Change library ID")
            tprint("2. Change API token")
            tprint("3. Change library type")
            tprint("4. Change collection ID")
            tprint("5. Disable Zotero")
            tprint("Or press enter to continue with setup.")
            i6 = input("\nEnter a choice: ")
            if i6 == "1":
                i7 = input("\nEnter your new library ID: ")
                try:
                    CONFIGURATION["Zotero"]["LibraryID"] = int(i7)
                    tprint("Library ID updated.")
                except:
                    tprint("\nInvalid library ID.")
            elif i6 == "2":
                i7 = input("\nEnter your new API token: ")
                CONFIGURATION["Zotero"]["APIToken"] = i7
                tprint("API token updated.")
            elif i6 == "3":
                tprint("\n Next, specify the library type. This will either be 'user' or 'group'. If this is a shared library, enter 'group'. Otherwise, enter 'user'.")
                while True:
                    i8 = input("\nEnter your new library type: ")
                    if i8 == 'user' or i8 == 'group':
                        break
                    else:
                        tprint("\nInvalid library type. Please enter 'user' or 'group'.")
                CONFIGURATION["Zotero"]["LibraryType"] = i8
                tprint("Library type updated.")
            elif i6 == "4":
                i7 = input("\nEnter your new collection ID: ")
                CONFIGURATION["Zotero"]["followXivCID"] = i7
                tprint("Collection ID updated.")
            elif i6 == "5":
                CONFIGURATION['Preferences']['UseZotero'] = False
                tprint("Zotero is now disabled.")
            elif i6 == "":
                return


def config_zotero_new():
    print_space()
    tprint("Would you like to enable Zotero? If you choose not to, you can always enable it later.")
    i5 = input("\nEnter 'y' to enable Zotero or 'n' to disable it: ")
    if i5 == "n" or i5 == "N":
        CONFIGURATION['Preferences']['UseZotero'] = False
        return
    elif i5 == "y" or i5 == "Y":
        CONFIGURATION['Preferences']['UseZotero'] = True
        tprint("All right, let's get Zotero set up for you. First, you will need your Zotero library ID and API token. You can find these at https://www.zotero.org/settings/keys.")
        tprint("\n Your library ID should be an 8-digit number, and your API token should be a 24-character string.")
        i6 = input("\nEnter your library ID: ")
        i7 = input("\nEnter your API token: ")
        tprint("\n Next, specify the library type. This will either be 'user' or 'group'. If this is a shared library, enter 'group'. Otherwise, enter 'user'.")
        while True:
            i8 = input("\nEnter your library type: ")
            if i8 == 'user' or i8 == 'group':
                break
            else:
                tprint("\nInvalid library type. Please enter 'user' or 'group'.")
        tprint("\n Great! Finally, please specify the collection ID for the Zotero collection in which you would like to store the results of followXiv.")
        tprint("\n You can find this by going to the collection in the browser version of Zotero and looking at the URL. The collection ID is the string of 8 letters at the end of the URL.")
        i9 = input("\nEnter your collection ID: ")
        try: CONFIGURATION["Zotero"]["LibraryID"] = int(i6) 
        except: tprint("\nInvalid library ID.")
        CONFIGURATION["Zotero"]["LibraryType"] = i8
        CONFIGURATION["Zotero"]["APIToken"] = i7
        CONFIGURATION["Zotero"]["followXivCID"] = i9
        tprint("\n Zotero has been set up! If you encounter Zotero authentication errors, double-check your library ID, API token and collection ID.")
        return
    else:
        tprint("\nInvalid choice. Please enter 'y' or 'n'.")
        config_zotero()


def config_crontab(): # TODO: test this
    while True:
        print_space()
        tprint("Would you like help setting followXiv to run daily on this computer using crontab? This will likely not work on Windows systems.")
        tprint("Note that this feature is experimental and may return errors. For best results, configure cron manually.")
        i5 = input("\nEnter 'y' to set up crontab or 'n' to skip this step: ")
        if i5 == 'n' or i5 == 'N':
            tprint("\n Crontab setup skipped.")
            return
        elif i5 == 'y' or i5 == 'Y':
            import os
            if os.name == 'posix':
                try: check_cron = os.system("crontab -l")
                except: 
                    tprint("Sorry, your system appears to be incompatible with cron setup :(")
                    return
                if check_cron > 0: 
                    tprint("Sorry, your system appears to be incompatible with cron setup :(")
                    return
            else:
                tprint("Sorry, your system appears to be incompatible with cron setup :(")
                return

            # get path to virtual env
            print_space()
            tprint("First, you'll need the path to the virtual environment in which the followXiv packages are stored. This might be something like ./venv/bin/python or perhaps /opt/anaconda3/envs/followXiv/bin/python")
            tprint("If you don't know the path, you can find it by running 'which python' in the terminal.")
            tprint(f"\nYour path appears to be \"{os.popen("which python").read().strip()}\". If this is correct, press enter; otherwise, enter the path to your virtual environment.")
            while True:
                venv_path = input("\nEnter the path to your virtual environment: ")
                if venv_path.strip() == "": 
                    venv_path = os.popen("which python").read().strip()
                    break
                else:
                    if os.path.isfile(venv_path): break
                    else: tprint("\nInvalid path. Please enter the full path to your virtual environment.")
            
            # get path to followXiv directory
            print_space()
            tprint("Next, you'll need the full path to the followXiv directory (not using shortcuts like ~). This might be something like /home/user/followXiv")
            tprint("If you don't know the path, you can find it by running 'pwd' in the terminal.")
            tprint(f"\nYour path appears to be \"{os.popen("pwd").read().strip()}\". If this is correct, press enter; otherwise, enter the path to your followXiv directory.")
            while True:
                followxiv_path = input("\nEnter the full path to followXiv.py: ")
                if followxiv_path.strip() == "":
                    followxiv_path = os.popen("pwd").read().strip()
                    break
                else:
                    if os.path.isdir(followxiv_path): break
                    else: tprint("\nInvalid path. Please ensure that the path points to the directory containing followXiv.py.")

            # choose run time
            print_space()
            tprint("What time would you like followXiv to run every weekday? Note that the cron job will fail if your computer is not connected to the internet at the time at which it is scheduled. Enter this in 24 hour format: for example, enter 13 for 1:00 p.m.")
            run_time = input("\nEnter the time to run followXiv (in 24 hour format): ")
            tprint("Setting up crontab. Your terminal may give a warning or ask for permission during this step.")
            
            # attempt setup
            try: 
                followxiv_path = os.system("pwd")
                os.system(f'(crontab -l ; echo "0 {run_time} * * 1-5 cd {followxiv_path} && git reset --hard HEAD && git pull && {venv_path} followXiv.py && mv output.txt "$(date -I).txt" >/dev/null")| crontab -')
            except OSError as err:
                tprint(f"An error occurred: {err}. Please try again, or set up cron manually.")
            return


def config_other():
    while True:
        print_space()
        tprint("Current settings are:")
        tprint(f"1. Match Resubmissions: {CONFIGURATION['Preferences']['MatchResubmissions']}")
        i8 = input("\nEnter the number of the setting you wish to update, or press enter to continue: ")
        if i8 == "1":
            tprint("Would you like to match resubmissions?")
            i9 = input("\nEnter 'y' to enable resubmission matching or 'n' to disable it: ")
            if i9 == "y" or i9 == "Y":
                CONFIGURATION['Preferences']['MatchResubmissions'] = True
                tprint("Resubmission matching enabled.")
            elif i9 == "n" or i9 == "N":
                CONFIGURATION['Preferences']['MatchResubmissions'] = False
                tprint("Resubmission matching disabled.")
            else:
                tprint("\nInvalid choice. Please enter 'y' or 'n'.")
        elif i8 == "":
            return
        else:
            tprint("\nInvalid choice. Please enter a number corresponding to one of the settings.")


def save_and_exit():
    print_space()
    tprint("Saving configuration...")
    try:
        with open("configuration.json", "w") as config_file:
            json.dump(CONFIGURATION, config_file, indent=4)
        tprint("Your preferences have been saved! Exiting now.")
    except:
        tprint("An error occurred while saving. Your preferences were not saved. Please try again.")
    exit()


# Run the setup tool
try:
    if NEW_SETUP:
        print_space()
        tprint("Welcome to followXiv! Since it looks like this is your first time running the script, here is the interactive setup!\n\n\n")
        tprint("Please note that the configuration file will be saved as configuration.json.")
        tprint("If you would like to change any settings later, you can do so by running followXiv-setup.py again, or by editing the JSON file directly.")
        while True:
            i0 = input("\nPress Enter to continue with setup, or 'q' to quit: ")
            if i0 == 'q':
                print("Exiting setup.")
                exit()                
            else:
                break
        first_configure()
    else:
        tprint("Welcome to the followXiv interactive setup!\n\n")
        reconfigure()

except KeyboardInterrupt:
            tprint("\n\nKeyboard interrupt detected. Exiting setup without saving.")
            exit()
except Exception as err:
    print_space()
    tprint(f"\n\nAn error occurred: {err}")
    tprint("\n :( ")
    tprint("\nIf you don't think this error should have occurred, you can report it to <github.com/wynter-alford/followXiv/issues>")
    tprint("\nAttempting to save your preferences so far...")
    save_and_exit()