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
from dataclasses import dataclass
import requests


@dataclass
class LocalConfig:
    """Local configuration"""
    assets_dir: str = "assets"
    hogsty:     str = "hogpics"
    roster:     str = "names.json"

@dataclass
class RemoteConfig:
    """Remote configuration"""
    hogsty:  str ="https://api.github.com/repos/tanner-caffrey/hogify/contents/assets/hogpics"
    roster:   str ="https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.json"

@dataclass
class RunConfig:
    """Runtime configuration"""
    spoof: bool = True
    debug: bool = True
    remote: bool = False
    your_yard: str = ""

@dataclass
class Config:
    """Hogify configuration"""
    local: LocalConfig = LocalConfig()
    remote: RemoteConfig = RemoteConfig()
    runtime: RunConfig = RunConfig()

class Hogify:
    """Hogify"""
            
    def __init__(self, config = Config()):
        self.config = config
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.StreamHandler())

    def get_hogs(self, local_hogs_in_your_area: bool):
        """Wrangles the local hogs in your area or goes on an expedition to git for them"""
        if local_hogs_in_your_area:
            return self.get_local_hogs()
        return self.download_hogs()

    # free hog pics in your area
    def download_hogs(self):
        """Downloads hogs from github to local memory"""
        self.log.info("Wrangling remote hogs.")
        resp = requests.get(self.config.remote.hogsty)
        hog_data = resp.json()
        hog_urls = [(hog["name"], hog["download_url"]) for hog in hog_data]
        hogs = {hog[0]: requests.get(hog[1]).content for hog in hog_urls}  # uh oh can a list contain that many entire hogs
        return hogs

    def get_local_hogs(self):
        """Gets the local hogs in your area if they exist"""
        self.log.info("Getting local hogs.")
        pics_path = os.path.join(self.config.local.assets_dir,self.config.local.hogsty)
        pics = [f for f in os.listdir(pics_path) if "hog" in f and "py" not in f]
        return pics

    def get_names(self,local_hogs_in_your_area: bool):
        """Gets list of names based on if local config exists"""
        if local_hogs_in_your_area:
            return self.get_local_names()
        return self.download_names()

    def download_names(self):
        """Gets list of names from git"""
        self.log.info("Downloading names.")
        resp = requests.get(self.config.remote.roster)
        names = list(resp.json())
        return names

    def get_local_names(self):
        """Gets list of names from config folder"""
        self.log.info("Getting local names.")
        names_path = os.path.join(self.config.local.assets_dir,self.config.local.roster)
        with open(names_path) as f:
            return list(json.load(f))

    def download_feral_hog(self,local_hogs_in_your_area: bool, name: str, hogs):
        """Either copies local hogs or writes the locally stored hogs to the yard"""
        if self.config.runtime.spoof:
            self.log.debug("Theoretically releasing hog! Say hola to %s!", name)
            return
        if local_hogs_in_your_area:
            self.log.debug("Copying hog!! Say hello to %s!", name)
            pic = os.path.join(self.config.local.assets_dir,self.config.local.hogsty,random.choice(hogs))
            pic_ext = "."+pic.split('.')[1]
            destination = os.path.join(self.config.runtime.your_yard,name+pic_ext)
            shutil.copy(pic,destination)
        else:
            self.log.debug("Writing hog!! Say hello to %s!", name)
            hog = random.choice(list(hogs.keys()))
            pic_ext = "."+hog.split('.')[1] # split hog
            destination = os.path.join(self.config.runtime.your_yard,name+pic_ext)
            with open(destination, 'wb') as handler:
                handler.write(hogs.get(hog)) # write!! that!! hog!!

    def run(self, number_of_feral_hogs):
        """downloads 30-50 feral hogs to your yard"""

        local_hogs_in_your_area = os.path.exists(self.config.local.assets_dir) and not self.config.runtime.remote

        if local_hogs_in_your_area: 
            self.log.info("Local hogs in your area. 👀") # 👀

        hogs = self.get_hogs(local_hogs_in_your_area)
        names = self.get_names(local_hogs_in_your_area)

        self.log.info("Downloading %d feral hog%s.", number_of_feral_hogs, 's'*(number_of_feral_hogs>1)) # ohgod oh fjuck

        for _ in range(number_of_feral_hogs):
            name = random.choice(names)
            self.download_feral_hog(local_hogs_in_your_area, name, hogs)


def process_arguments():
    """Processes the flags and arguments for the running of hogify"""
    parser = argparse.ArgumentParser(
                    prog = 'hogify',
                    description = 'Releases 30-50 feral hogs into your system.',
                    epilog = 'good luck')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Enable verbose logging.')
    parser.add_argument('-r', '--remote',
                        dest='force_remote',
                        action='store_true',
                        help='Force using remote assets.')
    parser.add_argument('-d', '--debug',
                        dest='debug_mode',
                        action='store_true',
                        help='Enable debug mode')
    parser.add_argument('-n',
                        type=check_positive,
                        default=random.randint(30,50),
                        dest='number_of_feral_hogs',
                        metavar='N',
                        help='Number of feral hogs to release.')
    args = parser.parse_args()
    return args

def check_positive(value):
    """Checks for a positive value for argument parsing"""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%(value)d is an invalid positive int value")
    return ivalue

def main():
    """Run"""
    # Process arguments
    args = process_arguments()

    hogify = Hogify()

    # Set logging level
    if args.debug_mode:
        hogify.log.setLevel(logging.DEBUG)
        hogify.log.debug("Debug mode ON.")
    elif args.verbose:
        hogify.log.setLevel(logging.INFO)

    hogify.run(args.number_of_feral_hogs)


# run those hogs
if __name__ == "__main__":
    main()
