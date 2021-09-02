import signal
import threading
import tkinter
from tkinter import *
from tkinter import filedialog
import Compressor

window = tkinter.Tk()
window.title("The all seeing eye")


def fun1():
    Compressor.automated_compressor()


def start_compressor():
    Compressor.loop_ender = True
    t = threading.Thread(target=fun1)
    t.start()


def stop_compressor():
    Compressor.loop_ender = False

def browse_button():
    filename = filedialog.askdirectory()
    Compressor.main_path = filename
    print(filename)


tkinter.Label(window, text="Archive:").grid(row=0)

tkinter.Label(window, text="Compressed Archive:").grid(row=1)
t1 = tkinter.Label(window, text=Compressor.main_path_definition).grid(row=1, column=1)
browsebutton = tkinter.Button(window, text="Browse", command=browse_button).grid(row=1, column=2)

bt1 = tkinter.Button(window, text="Start", height=1, width=2, command=start_compressor).grid(row=2, column=2)
bt2 = tkinter.Button(window, text="Kill", height=1, width=2, command=stop_compressor).grid(row=2, column=1)

window.geometry("400x200")
window.mainloop()
