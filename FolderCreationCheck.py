import inotify.adapters
import re

notifier = inotify.adapters.Inotify()
notifier.add_watch("/home/overlayfox/Documents/Test")
global foldername


def check():
    matched = re.match("[0-9][0-9]+", foldername)
    is_match = bool(matched)
    if matched:
        print("Yes")
    else:
        print("No")



for event in notifier.event_gen():
    if event is not None:
        if "IN_CREATE" in event[1]:
            print("file '{0}' created in '{1}'".format(event[3], event[2]))
            foldername = event[3]
            print(foldername)
            check()
