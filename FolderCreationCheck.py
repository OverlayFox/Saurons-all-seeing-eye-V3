import inotify.adapters
import os

notifier = inotify.adapters.Inotify()
notifier.add_watch("/home/overlayfox/Documents/Test")

for event in notifier.event_gen():
    if event is not None:
        if "IN_CREATE" in event[1]:
            print ("file '{0}' created in '{1}'".format(event[3], event [2]))