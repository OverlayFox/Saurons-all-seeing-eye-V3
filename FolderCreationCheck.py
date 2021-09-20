import datetime
import os
from tkinter import *

import inotify.adapters

getdate = datetime.datetime

# defines variables
notifier = inotify.adapters.Inotify()
global path
global folder_name
global folder_counter
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
    global folder_counter

    folders = ["/00 Export", "/01 Footage", "/02 Fonts", "/03 Graphics", "/04 Premiere", "/05 AfterEffects", "/06 Photoshop"]
    folder_counter = 0
    matched = re.match("[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9] - ", folder_name)
    bool(matched)
    if matched:
        while folder_counter < 7:
            os.makedirs(path + folder_name + folders[folder_counter])
            folder_counter = folder_counter + 1
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
