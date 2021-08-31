import subprocess
import tkinter
import Compressor
top = tkinter.Tk()


def test():
    print("Hello World")


B = tkinter.Button(top, text="Print Something", command=test)

B.pack()
top.mainloop()
