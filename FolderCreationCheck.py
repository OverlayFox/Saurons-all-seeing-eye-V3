import datetime
import os
from tkinter import *

import inotify.adapters

getdate = datetime.datetime

# defines variables
notifier = inotify.adapters.Inotify()
global path
global folder_name
count_folder = 0
count_deleted = 0
count_allowed = 0


def path_check():
    global path

    path = input("Enter the Path for the Directory to be checked: ") + "/"
    while True:
        if os.path.exists(path):
            return
        else:
            path = input("Please enter a valid Path for the Directory to be checked: ") + "/"


path_check()
notifier.add_watch(path)

# this checks the given path and looks for folders that don't follow the "0000_00_00 - " naming scheme.
# If they don't it deletes them, if it does it creates 7 sub folders in the new directory


def check():
    global count_deleted
    global path
    global count_allowed

    matched = re.match("[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9] - ", folder_name)
    bool(matched)
    if matched:
        os.makedirs(path + folder_name + "/00 Export")
        os.makedirs(path + folder_name + "/01 Footage")
        os.makedirs(path + folder_name + "/02 Fonts")
        os.makedirs(path + folder_name + "/03 Graphics")
        os.makedirs(path + folder_name + "/04 Premiere")
        os.makedirs(path + folder_name + "/05 AfterEffects")
        os.makedirs(path + folder_name + "/06 Photoshop")
        count_allowed = count_allowed + 1
        if count_allowed > 1:
            print(count_allowed, " Folders allowed")
        else:
            print(count_allowed, " Folder allowed")
    else:
        os.rmdir(path + folder_name)
        count_deleted = count_deleted + 1
        if count_deleted > 1:
            print(count_deleted, " Folders deleted")
        else:
            print(count_deleted, " Folder deleted")


for event in notifier.event_gen():
    if event is not None:
        if "IN_CREATE" in event[1]:
            print("Folder '{0}' was created at ".format(event[3], event[2]) + getdate.now().strftime("%H:%M:%S"))
            folder_name = event[3]
            count_folder = count_folder + 1
            if count_folder > 1:
                print(count_folder, " Folders created by user")
            else:
                print(count_folder, " Folder created by user")
            check()
