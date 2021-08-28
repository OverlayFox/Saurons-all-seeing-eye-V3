import lzma
import os
import py7zr
import datetime
import shutil
import time

my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME}]
getdate = datetime.datetime
weekday = getdate.today().weekday()
date = getdate.now()
date_converted = date.strftime("%H:%M:%S")
main_path = "/home/overlayfox/Documents/Test"
zip_file_name = date.strftime("%Y_%m_%d - compressedArchive")


def compressor():
    if not os.listdir(main_path):
        print("Directory is empty")
    else:
        with py7zr.SevenZipFile(zip_file_name, 'w', filters=my_filter) as archive:
            archive.writeall(main_path, 'archive')
            shutil.move(zip_file_name, "/home/overlayfox/Documents")


def getweekday():
    global weekday

    weekday = getdate.today().weekday()


while True:
    if date_converted != "11:18:00" and weekday != "4":
        date = getdate.now()
        date_converted = date.strftime("%H:%M:%S")
        time.sleep(1)
        print(date_converted)
        if date_converted == "00:00:01":
            getweekday()
            print(weekday)
    else:
        compressor()
