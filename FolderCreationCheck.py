import inotify.adapters
import re
import os
import tkinter
from tkinter import *

# defines variables
notifier = inotify.adapters.Inotify()
notifier.add_watch("/home/overlayfox/Documents/Test")
global folder_name
count_folder = 0
count_deleted = 0
count_allowed = 0
path = "/home/overlayfox/Documents/Test/"


# this checks the given path and looks for folders that don't follow the "0000_00_00 - " naming scheme.
# If they don't it deletes them, if it does it creates 7 sub folders in the new directory

def check():
    global count_deleted
    global path
    global count_allowed

    matched = re.match("[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9] - ", folder_name)
    is_match = bool(matched)
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
            print(count_allowed, " folders created")
        else:
            print(count_allowed, " folder created")
    else:
        os.rmdir(path + folder_name)
        count_deleted = count_deleted + 1
        if count_deleted > 1:
            print(count_deleted, " folders deleted")
        else:
            print(count_deleted, " folder deleted")


for event in notifier.event_gen():
    if event is not None:
        if "IN_CREATE" in event[1]:
            print("file '{0}' created in '{1}'".format(event[3], event[2]))
            folder_name = event[3]
            count_folder = count_folder + 1
            check()
