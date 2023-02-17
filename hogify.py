import json
import shutil
import os
import random
import requests

# Assets directory; if it does not exist, gathers resources from online
assets_dir = "assets"
# Location in which to download and release the feral hogs
your_homestead = ""
# Local hog photo directory in assets directory
hogsty = "hogpics"
# Local names file in assets directory
roster = "names.json"
# Remote location of hog photos
remote_hogsty = "https://api.github.com/repos/tanner-caffrey/hogify/contents/assets/hogpics"
# Remote location of names
remote_names = "https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.json"


# Enable stdout feedback
feedback = True
# More print statements
verbose = False and feedback
# A perhaps unuseful amount of verbage
very_verbose = False and verbose
# Forces the use of remote name and hog photo lists
force_remote = False


# Wrangles the local hogs in your area or goes on an expedition to git for them
def get_hogs(local_hogs_in_your_area: bool):
    if local_hogs_in_your_area:
        return get_local_hogs()
    return download_hogs()

# free hog pics in your area
# Downloads hogs from github to local memory
def download_hogs():
    if verbose: print("Wrangling remote hogs.")
    r = requests.get(remote_hogsty)
    hog_data = r.json()
    hog_urls = [(hog["name"], hog["download_url"]) for hog in hog_data]
    hogs = {hog[0]: requests.get(hog[1]).content for hog in hog_urls}  # uh oh can a list contain that many entire hogs
    return hogs

# Gets the local hogs in your area if they exist
def get_local_hogs():
    if verbose: print("Getting local hogs.")
    pics_path = os.path.join(assets_dir,hogsty)
    pics = [f for f in os.listdir(pics_path) if "hog" in f and "py" not in f]
    return pics

# Gets list of names based on if local config exists
def get_names(local_hogs_in_your_area: bool):
    if local_hogs_in_your_area:
        return get_local_names()
    return download_names()

# Gets list of names from git
def download_names():
    if verbose: print("Downloading names.")
    r = requests.get(remote_names)
    names = list(r.json())
    return names

# Gets list of names from config folder
def get_local_names():
    if verbose: print("Getting local names.")
    names_path = os.path.join(assets_dir,roster)
    f = open(names_path)
    names = list(json.load(f))
    return names

# Either copies local hogs or writes the locally stored hogs to the homestead
def download_feral_hog(local_hogs_in_your_area: bool, name: str, hogs):
    if local_hogs_in_your_area:
        if very_verbose: print("Copying hog!!")
        pic = os.path.join(assets_dir,hogsty,random.choice(hogs))
        pic_ext = "."+pic.split('.')[1]
        destination = os.path.join(your_homestead,name+pic_ext)
        shutil.copy(pic,destination)
    else:
        if very_verbose: print("Writing hog!!")
        hog = random.choice(list(hogs.keys()))
        pic_ext = "."+hog.split('.')[1] # split hog
        destination = os.path.join(your_homestead,name+pic_ext)
        with open(destination, 'wb') as handler:
            handler.write(hogs.get(hog)) # write that hog!!


# downloads 30-50 feral hogs to your homestead
def main():
    local_hogs_in_your_area = True if os.path.exists(assets_dir) and not force_remote else False

    if feedback and local_hogs_in_your_area: print("Local hogs in your area. 👀") # 👀

    hogs = get_hogs(local_hogs_in_your_area)
    names = get_names(local_hogs_in_your_area)

    # how many hogs?
    number_of_feral_hogs = random.randint(30,50)

    if feedback: print("Downloading",number_of_feral_hogs,"feral hogs.") # ohgod oh fjuck

    for n in range(number_of_feral_hogs):
        name = random.choice(names)
        download_feral_hog(local_hogs_in_your_area, name, hogs)


if __name__ == "__main__":
    main()