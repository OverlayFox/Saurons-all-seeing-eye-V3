import lzma
import py7zr
import os
import shutil

my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 7}]

with py7zr.SevenZipFile('target.7z', 'w', filters=my_filter) as archive:
    archive.writeall('/home/overlayfox/Documents/Test', 'base')
    shutil.move("target.7z", "/home/overlayfox/Documents")



