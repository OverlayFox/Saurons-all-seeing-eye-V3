import inotify.adapters
import re
import os

notifier = inotify.adapters.Inotify()
notifier.add_watch("/home/overlayfox/Documents/Test")
global foldername


def check():
    matched = re.match("[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9] - ", foldername)
    is_match = bool(matched)
    if matched:
        print("Fine")
    else:
        path = "/home/overlayfox/Documents/Test/"+foldername
        os.rmdir(path)
        print("Folder delted")



for event in notifier.event_gen():
    if event is not None:
        if "IN_CREATE" in event[1]:
            print("file '{0}' created in '{1}'".format(event[3], event[2]))
            foldername = event[3]
            print(foldername)
            check()
