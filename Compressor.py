import lzma
import os
import py7zr
import datetime
import shutil
import time
import re

global main_path
global archive_path
global path_test
global compressor_time
global compressor_date
global user_compressor_date


# get data from user

def main_path_definer():
    global main_path

    main_path = input("Enter the uncompressed Archive Path here: ")
    while True:
        if os.path.exists(main_path):
            return
        else:
            main_path = input("Please use an existing Path for the uncompressed Archive Path here: ")


def archive_path_definer():
    global archive_path
    global main_path

    archive_path = input("Enter the compressed Archive Path here: ")
    while True:
        if os.path.exists(archive_path):
            if main_path == archive_path:
                print("Uncompressed Archive and compressed Archive cannot have the same destination")
                archive_path = input("Please enter a new compressed Archive Path here: ")
            else:
                return
        else:
            archive_path = input("Please use an existing Path for the compressed Archive Path here: ")


def compressor_time_definer():
    global compressor_time

    compressor_time = input("Enter starting time in format HH:MM:SS: ")
    while True:
        matched = re.match("[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", compressor_time)
        bool(matched)
        if matched:
            return
        else:
            compressor_time = input("Follow the format HH:MM:SS for the starting time: ")


def compressor_date_definer():
    global compressor_date
    global user_compressor_date
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    user_compressor_date = input("Enter a weekday to execute compressor: ")
    while True:
        if user_compressor_date.lower() in weekdays:
            compressor_date = weekdays.index(user_compressor_date.lower())
            return
        else:
            user_compressor_date = input("Please enter a valid weekday from monday to friday: ")


compressor_time_definer()
compressor_date_definer()
main_path_definer()
archive_path_definer()
print("Compressor will be executed on " + user_compressor_date + " at " + compressor_time)

# ----------------------------------------------------------------------------------------------------
# the actual compressor script

my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME}]  # defines the compressor for the 7z archive
getdate = datetime.datetime
weekday = getdate.today().weekday()
date = getdate.now()
date_converted = date.strftime("%H:%M:%S")
zip_file_name = date.strftime("%Y_%m_%d - compressedArchive")


def get_size():
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(main_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def getweekday():
    global weekday

    weekday = getdate.today().weekday()


def compressor():
    global my_filter

    if not os.listdir(main_path):  # checks if the directory is empty or not
        print("Directory is empty")
    else:
        if not get_size() >= shutil.disk_usage(archive_path)[2]:  # checks if there is enough space for the compression
            with py7zr.SevenZipFile(zip_file_name, 'w', filters=my_filter) as archive:  # if the directory is not empty it compresses all files into a 7z archive
                archive.writeall(main_path, 'archive')
            shutil.move(zip_file_name, archive_path)  # moves the archive to the set destination
            for files in os.listdir(main_path):
                deletion_path = os.path.join(main_path, files)
                try:
                    shutil.rmtree(deletion_path)
                except OSError:
                    os.remove(deletion_path)
        else:
            print("Not enough space available to compress the archive.")


while True:
    if date_converted != compressor_time and weekday != compressor_date:  # checks if it is the user set date and time
        date = getdate.now()  # if not it checks the time every second and waits for the time to arrive
        date_converted = date.strftime("%H:%M:%S")
        time.sleep(1)
        if date_converted == "00:00:01":
            getweekday()
    else:  # if the time arrived it runs the compressor class and loops again
        compressor()
