# Saurons-all-seeing-eye-V3

Made by OverlayFox
Python 3.8 Script
Made for Linux (this will not run on a Windows or MAC System)

Compressor:
This is a script that compressed the data in one directory into another at a specified date and then deletes the original Data.

Libraries needed:
-	lzma
-	os
-	py7zr
-	datetime
-	shutil
-	time
-	re

Operation:
This script will wait for the time specified by the user in the beginning.
When that date arrives, it will look if the directory is empty.
If so, it will wait again until the user set time arrives again.
If not, it will check how big all files are and how much space is left on the NAS.
If there is enough space it will start to compress the files.
Once it is done with that, it will move that archive to the second user defined destination
It will then delete the old files.
 

FolderCreationCheck:
This is a script that checks when a folder has been created, if it follows a specific name structure.
If so, it will create multiple subfolders in it.
If not, it will delete the folder

Libraries needed:
-	datetime
-	os
-	* from tkinter
-	inotify.adapters

Operation:
This Script will look for an event in a user specified folder, if a folder gets created and named, it will see if that folder follows the naming structure “0000_00_00 – [Random Text]’’
If it doesn’t, it will instantly delete that folder before the user can even do anything with it.
If it does, it will create 7 subfolders in the newly made folder with the structure
-	00 Export
-	01 Footage
-	02 Fonts
-	03 Graphics
-	04 Premiere
-	05 AfterEffects
-	06 Photoshop
The user can then freely change the folder to his heart’s content.

The script will also save and monitor how many folders have been created, deleted and allowed and will save that data in the text document “folder_counter_txt.txt”
