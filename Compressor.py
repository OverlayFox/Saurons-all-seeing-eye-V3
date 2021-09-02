import lzma
import os
import py7zr
import datetime
import shutil
import time
import tkinter

compressor_time = "11:18:00"
compressor_date = "5"
main_path = "/home/overlayfox/Documents"
archive_path = "/home/overlayfox/Documents"

my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME}]                     #defines the compressor for the 7z archive
getdate = datetime.datetime
weekday = getdate.today().weekday()
date = getdate.now()
date_converted = date.strftime("%H:%M:%S")
zip_file_name = date.strftime("%Y_%m_%d - compressedArchive")


def compressor():
    if not os.listdir(main_path):                                                                 #checks if the directory is empty or not
        print("Directory is empty")
    else:
        with py7zr.SevenZipFile(zip_file_name, 'w', filters=my_filter) as archive:                #if the directory is not empty it compresses all files into a 7z archive
            archive.writeall(main_path, 'archive')
            shutil.move(zip_file_name, archive_path) #moves the archive to the set destination


def getweekday():
    global weekday

    weekday = getdate.today().weekday()


def automated_compressor():
    global date_converted
    global date

    while True:
        if date_converted != compressor_time and weekday != compressor_date:                                          #checks if it is saturday at 1am
            date = getdate.now()                                                                     #if not it checks the time every second and waits for the time to arrive
            date_converted = date.strftime("%H:%M:%S")
            time.sleep(1)
            print(date_converted)
            if date_converted == "00:00:01":
                getweekday()
                print(weekday)
        else:                                                                                        #if the time arrived it runs the compressor class and loops again
            compressor()
