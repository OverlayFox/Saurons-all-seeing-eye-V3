import lzma
import py7zr
import datetime
import shutil
import time


my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME}]
weekday = datetime.datetime.today().weekday()
date = datetime.datetime.now()
date_converted = date.strftime("%H:%M:%S")


while date_converted != "12:19:30" and weekday != "3":
    weekday = datetime.datetime.today().weekday()
    date = datetime.datetime.now()
    date_converted = date.strftime("%H:%M:%S")
    time.sleep(1)
    print(date_converted)
    print(weekday)
else:
    with py7zr.SevenZipFile('target.7z', 'w', filters=my_filter) as archive:
        archive.writeall('/home/overlayfox/Documents/Test', 'base')
        shutil.move("target.7z", "/home/overlayfox/Documents")



