import signal
import threading
import tkinter
from tkinter import *
from tkinter import filedialog
import Compressor
import FolderCreationCheck

date = "Null"
window = tkinter.Tk()
window.title("The all seeing eye")

#Date Converter
if Compressor.compressor_date == "0":
    date = "Monday"
if Compressor.compressor_date == "1":
    date = "Tuesday"
if Compressor.compressor_date == "2":
    date = "Wednesday"
if Compressor.compressor_date == "3":
    date = "Thursday"
if Compressor.compressor_date == "4":
    date = "Friday"
if Compressor.compressor_date == "5":
    date = "Saturday"
if Compressor.compressor_date == "6":
    date = "Sunday"


tkinter.Label(window, text="Current time for the Compressor:").grid(row=1)
tkinter.Label(window, text="            ").grid(row=1, column=1)
tkinter.Label(window, text=Compressor.compressor_time).grid(row=1, column=2)
tkinter.Label(window, text=date).grid(row=1, column=3)

tkinter.Label(window, text="Processed Folders:").grid(sticky="w", row=2, column=0)
tkinter.Label(window, text="            ").grid(row=2, column=1)
#tkinter.Label(window, text=FolderCreationCheck.count_folder).grid(row=2, column=2)


window.geometry("400x200")
window.mainloop()
