import lzma
import py7zr

my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}]

with py7zr.SevenZipFile('target.7z', 'w', filters=my_filter) as archive:
    archive.writeall("/home/overlayfox/Documents/Test")



