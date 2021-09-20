import datetime
import os
from tkinter import *
import inotify.adapters

getdate = datetime.datetime
notifier = inotify.adapters.Inotify()
global path
global folder_name
global folder_counter


def allowed_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()  # saves the txt doc as a array
        counter = int(list_of_lines[
                          4])  # saves the 5th line of the text doc into the variable that was converted from a str to a int
        counter = counter + 1  # adds +1 to the readout variable
        list_of_lines[4] = str(counter) + "\n"  # saves that variable to the same line and converts it back to a str
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)  # saves the array back into the txt document
    if counter > 1:
        print(counter, " Folders allowed")
    else:
        print(counter, " Folder allowed")


def deleted_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()
        counter = int(list_of_lines[7])
        counter = counter + 1
        list_of_lines[7] = str(counter) + "\n"
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)
    if counter > 1:
        print(counter, " Folders deleted")
    else:
        print(counter, " Folder deleted")


def total_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()
        counter = int(list_of_lines[1])
        counter = counter + 1
        list_of_lines[1] = str(counter) + "\n"
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)
    if counter > 1:
        print(counter, " Folders created by user in total")
    else:
        print(counter, " Folder created by user in total")


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


def check():
    global path

    folders = ["/00 Export", "/01 Footage", "/02 Fonts", "/03 Graphics", "/04 Premiere", "/05 AfterEffects", "/06 Photoshop"]
    folder_cycle = 0
    matched = re.match("[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9] - ", folder_name)
    bool(matched)
    if matched:
        while folder_cycle < 7:
            os.makedirs(path + folder_name + folders[folder_cycle])
            folder_cycle = folder_cycle + 1
        allowed_folder_counter()
    else:
        os.rmdir(path + folder_name)
        deleted_folder_counter()


for event in notifier.event_gen():
    if event is not None:
        if "IN_CREATE" in event[1]:
            print("Folder '{0}' was created at ".format(event[3], event[2]) + getdate.now().strftime("%H:%M:%S"))
            folder_name = event[3]
            total_folder_counter()
            check()
