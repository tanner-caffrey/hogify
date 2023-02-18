"""
File:           hogify.py
Author:         Tanner Caffrey
Description:    Releases 30-50 feral hogs into your system.
"""

import argparse
import json
import logging
import os
import random
import shutil
import requests


# Assets directory; if it does not exist, gathers resources from online
ASSETS_DIR = "assets"
# Location in which to download and release the feral hogs
YOUR_YARD = ""
# Local hog photo directory in assets directory
HOGSTY = "hogpics"
# Local names file in assets directory
ROSTER = "names.json"
# Remote location of hog photos
REMOTE_HOGSTY = "https://api.github.com/repos/tanner-caffrey/hogify/contents/assets/hogpics"
# Remote location of names
REMOTE_NAMES = "https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.json"

# Enable to turn off writing data
DEBUG=True

# Forces the use of remote name and hog photo lists
FORCE_REMOTE = True

# Set logging level based on verbosity
log = logging.getLogger("hogify.log")

def get_hogs(local_hogs_in_your_area: bool):
    """Wrangles the local hogs in your area or goes on an expedition to git for them"""
    if local_hogs_in_your_area:
        return get_local_hogs()
    return download_hogs()

# free hog pics in your area
def download_hogs():
    """Downloads hogs from github to local memory"""
    log.info("Wrangling remote hogs.")
    r = requests.get(REMOTE_HOGSTY)
    hog_data = r.json()
    hog_urls = [(hog["name"], hog["download_url"]) for hog in hog_data]
    hogs = {hog[0]: requests.get(hog[1]).content for hog in hog_urls}  # uh oh can a list contain that many entire hogs
    return hogs

def get_local_hogs():
    """Gets the local hogs in your area if they exist"""
    log.info("Getting local hogs.")
    pics_path = os.path.join(ASSETS_DIR,HOGSTY)
    pics = [f for f in os.listdir(pics_path) if "hog" in f and "py" not in f]
    return pics

def get_names(local_hogs_in_your_area: bool):
    """Gets list of names based on if local config exists"""
    if local_hogs_in_your_area:
        return get_local_names()
    return download_names()

def download_names():
    """Gets list of names from git"""
    log.debug("Downloading names.")
    r = requests.get(REMOTE_NAMES)
    names = list(r.json())
    return names

def get_local_names():
    """Gets list of names from config folder"""
    log.debug("Getting local names.")
    names_path = os.path.join(ASSETS_DIR,ROSTER)
    with open(names_path) as f:
        return list(json.load(f))

def download_feral_hog(local_hogs_in_your_area: bool, name: str, hogs):
    """Either copies local hogs or writes the locally stored hogs to the yard"""
    if DEBUG:
        log.log(5, "Theoretically releasing hog! Say hola to %(name)s!")
        return
    if local_hogs_in_your_area:
        log.log(5, "Copying hog!! Say hello to %(name)s!")
        pic = os.path.join(ASSETS_DIR,HOGSTY,random.choice(hogs))
        pic_ext = "."+pic.split('.')[1]
        destination = os.path.join(YOUR_YARD,name+pic_ext)
        shutil.copy(pic,destination)
    else:
        log.log(5, "Writing hog!! Say hello to %(name)s!")
        hog = random.choice(list(hogs.keys()))
        pic_ext = "."+hog.split('.')[1] # split hog
        destination = os.path.join(YOUR_YARD,name+pic_ext)
        with open(destination, 'wb') as handler:
            handler.write(hogs.get(hog)) # write!! that!! hog!!

def process_arguments():
    """Processes the flags and arguments for the running of hogify"""
    parser = argparse.ArgumentParser(
                    prog = 'hogify',
                    description = 'Releases 30-50 feral hogs into your system.',
                    epilog = 'good luck')
    parser.add_argument('filename')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Enable verbose logging.')
    parser.add_argument('-vv', '--very_verbose', '--vverbose', '--veryverbose', '--veryVerbose',
                        dest='very_verbose',
                        action='store_true',
                        help='Enable very verbose logging.')
    parser.add_argument('-l', '--logging',
                        dest='feedback',
                        action='store_true',
                        help='Enable logging.')
    parser.add_argument('-r', '--remote',
                        dest='force_remote',
                        action='store_true',
                        help='Force using remote assets.')     
    parser.add_argument('-d', '--debug',
                        dest='debug_mode',
                        action='store_true',
                        help='Enable debug mode')
    parser.add_argument('-n',
                        type=int, 
                        default=random.randint(30,50), 
                        dest='number_of_feral_hogs',
                        help='Number of feral hogs to release.')
    return parser.parse_args()

def main():
    """downloads 30-50 feral hogs to your yard"""

    # Process arguments
    args = process_arguments()

    # Set logging level
    if args.very_verbose:
        log.setLevel(5)
    elif args.verbose:
        log.setLevel(10)
    elif args.feedback:
        log.setLevel(20)
    else:
        log.setLevel(40)
    log.log(40 * DEBUG, "Debug mode ON.")

    # Set flags
    FORCE_REMOTE = args.force_remote
    DEBUG = args.debug



    local_hogs_in_your_area = os.path.exists(ASSETS_DIR) and not FORCE_REMOTE

    if local_hogs_in_your_area: 
        log.info("Local hogs in your area. 👀") # 👀

    hogs = get_hogs(local_hogs_in_your_area)
    names = get_names(local_hogs_in_your_area)

    # how many hogs?
    number_of_feral_hogs = args.number_of_feral_hogs

    log.info("Downloading %(number_of_feral_hogs)d feral hogs.") # ohgod oh fjuck

    for _ in range(number_of_feral_hogs):
        name = random.choice(names)
        download_feral_hog(local_hogs_in_your_area, name, hogs)


if __name__ == "__main__":
    main()