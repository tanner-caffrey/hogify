import json
import shutil
import os
import random

conf_dir = "config"
your_homestead = ".."
hogsty = "hogpics"

# downloads 30-50 feral hogs to your homestead (default: parent of current directory)
def main():
    local_hogs_in_your_area = True if os.path.exists(conf_dir) else False
    if not local_hogs_in_your_area:
        pass
    names_path = os.path.join(conf_dir,"names.json")
    f = open(names_path)
    names = list(json.load(f))

    pics_path = os.path.join(conf_dir,hogsty)
    pics = [f for f in os.listdir(pics_path) if "hog" in f and "py" not in f]

    # how many hogs?
    number_of_feral_hogs = random.randint(30,50)

    print("Downloading",number_of_feral_hogs,"feral hogs.") # oh fuck

    for n in range(number_of_feral_hogs):
        name = random.choice(names)
        pic = os.path.join(pics_path,random.choice(pics))
        destination = os.path.join(your_homestead,name+"."+pic.split('.')[1])
        shutil.copy(pic,destination)

if __name__ == "__main__":
    main()