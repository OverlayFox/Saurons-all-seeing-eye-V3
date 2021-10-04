import lzma
import os
import py7zr
import datetime
import shutil
import time
import re
import subprocess
from smb.SMBConnection import SMBConnection

userID = "the_black_gate"
password = "SA_1600"
client_machine_name = "OverlayFox"
server_name = "mordor"
domain_name = "mordor"
conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)
global path_test
global compressor_time
global compressor_date
global user_compressor_date
global main_share
global archive_share
global share_name_list
global server_ip


# get data from user
def server_check():
    global server_ip

    server_ip = input("Please enter the Servers IP Address: ")
    while True:
        matched = re.match("192.168.[0-9][0-9].[0-9][0-9][0-9]", server_ip)
        bool(matched)
        if matched:
            command = ['ping', '-c', '1', server_ip]
            try:
                print("Pinging Server....")
                if subprocess.call(command) == 0:
                    print("Server was reached and is online")
                    return
            except IOError:
                server_ip = input("Please ensure the Server is online and reenter the IP Address: ")
            else:
                server_ip = input("Please ensure the Server is online and reenter the IP Address: ")
        else:
            server_ip = input("Please enter a IP Address the follows the pattern 192.168.000.000")


def main_path_definer():
    global main_share
    global share_name_list

    i = 0
    share_name_list = []
    while i < len(conn.listShares()):
        share_name_list.append(conn.listShares()[i].name)
        i = i + 1

    main_share = input("Enter the name of the uncompressed Share here: ")
    while True:
        if main_share in share_name_list:
            return
        else:
            main_share = input("Share does not exist, please enter one that does exist: ")


def archive_path_definer():
    global archive_share
    global main_share

    archive_share = input("Enter the compressed Share here: ")
    while True:
        if archive_share in share_name_list:
            if archive_share == main_share:
                print("Uncompressed Share and compressed Share cannot have the same destination")
                archive_share = input("Please enter a new compressed Share here: ")
            else:
                return
        else:
            archive_share = input("Please use an existing Share for the compressed Archive here: ")


def compressor_time_definer():
    global compressor_time

    compressor_time = input("Enter starting time in format HH:MM:SS: ")
    while True:
        matched = re.match("[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", compressor_time)
        bool(matched)
        if matched:
            return
        else:
            compressor_time = input("Follow the format HH:MM:SS for the starting time: ")


def compressor_date_definer():
    global compressor_date
    global user_compressor_date
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    user_compressor_date = input("Enter a weekday to execute compressor: ")
    while True:
        if user_compressor_date.lower() in weekdays:
            compressor_date = weekdays.index(user_compressor_date.lower())
            return
        else:
            user_compressor_date = input("Please enter a valid weekday from monday to friday: ")


compressor_time_definer()
compressor_date_definer()
server_check()
conn.connect(server_ip, 445)
main_path_definer()
archive_path_definer()
print("Compressor will be executed on " + user_compressor_date + " at " + compressor_time)
print("Files will be moved from " + main_share + " to " + archive_share)

# ----------------------------------------------------------------------------------------------------
# the actual compressor script

my_filter = [{"id": py7zr.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME}]  # defines the compressor for the 7z archive
getdate = datetime.datetime
weekday = getdate.today().weekday()
date = getdate.now()
date_converted = date.strftime("%H:%M:%S")


def get_size():
    total_size = 0
    for filename in conn.listPath(main_share, "/"):
        total_size = total_size + filename.filesize

    return total_size


def compressor():
    global my_filter
    global main_share
    global archive_share

    if not len(conn.listPath(main_share, "/")) <= 2:  # checks if the directory is empty or not
        print("Directory is empty")
    else:
        zip_file_name = date.strftime("%Y_%m_%d - compressedArchive")
        with py7zr.SevenZipFile(zip_file_name, 'w', filters=my_filter) as archive:  # if the directory is not empty it compresses all files into a 7z archive
            # archive.writeall(main_path, 'archive')
            conn.storeFile(archive_share, "/", archive)  # moves the archive to the set destination
        try:
            conn.deleteFiles(main_share, "/", delete_matching_folders=True)  # tries to delete the old files in the original share
        except OSError:
            'Files could not be deleted'


while True:
    if date_converted != compressor_time and weekday != compressor_date:  # checks if it is the user set date and time
        date = getdate.now()  # if not it checks the time every second and waits for the time to arrive
        date_converted = date.strftime("%H:%M:%S")
        time.sleep(1)
        if date_converted == "00:00:01":
            weekday = getdate.today().weekday()
    else:  # if the time arrived it runs the compressor class and loops again
        compressor()
