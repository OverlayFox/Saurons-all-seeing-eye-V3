import subprocess
import Compressor
import GUI
import FolderCreationCheck

subprocess.run("python3 GUI.py & python3 Compressor.py & FolderCreationCheck.py", shell=True)
