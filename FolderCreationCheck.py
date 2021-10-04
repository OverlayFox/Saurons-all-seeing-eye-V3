import datetime
import os
from tkinter import *
import random
from smb.SMBConnection import SMBConnection
import platform
import subprocess
import time

getdate = datetime.datetime
global folder_counter
global server_ip
global share
global name_last_created_folder

userID = "the_black_gate"
password = "SA_1600"
client_machine_name = input("Please enter the clients machine name: ")
server_name = "mordor"
domain_name = "mordor"
conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)


def allowed_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()  # saves the txt doc as a array
        counter = int(list_of_lines[
                          4])  # saves the 5th line of the text doc into the variable that was converted from a str to a int
        counter = counter + 1  # adds +1 to the readout variable
        list_of_lines[4] = str(counter) + "\n"  # saves that variable to the same line and converts it back to a str
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)  # saves the array back into the txt document
    if counter > 1:
        print(counter, " Folders allowed")
    else:
        print(counter, " Folder allowed")


def deleted_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()
        counter = int(list_of_lines[7])
        counter = counter + 1
        list_of_lines[7] = str(counter) + "\n"
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)
    if counter > 1:
        print(counter, " Folders deleted")
    else:
        print(counter, " Folder deleted")


def total_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()
        counter = int(list_of_lines[1])
        counter = counter + 1
        list_of_lines[1] = str(counter) + "\n"
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)
    if counter > 1:
        print(counter, " Folders created by user in total")
    else:
        print(counter, " Folder created by user in total")


def special_folder_counter():
    with open("folder_counter_txt.txt", "r") as f:
        list_of_lines = f.readlines()
        counter = int(list_of_lines[10])
        counter = counter + 1
        list_of_lines[10] = str(counter) + "\n"
    with open("folder_counter_txt.txt", "w") as f:
        f.writelines(list_of_lines)
    if counter > 1:
        print(counter, " special folders made")
    else:
        print(counter, " special folder made")


def path_check():
    global share

    i = 0
    share_name_list = []
    while i < len(conn.listShares()):
        share_name_list.append(conn.listShares()[i].name)
        i = i + 1

    share = input("Enter the name of the Share that is supposed to be checked: ")
    while True:
        if share in share_name_list:
            return
        else:
            share = input("Share does not exist, please enter one that does exist: ")


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


server_check()
conn.connect(server_ip, 445)
path_check()


def check():
    global name_last_created_folder

    folders = ["/00 Export", "/01 Footage", "/02 Fonts", "/03 Graphics", "/04 Premiere", "/05 AfterEffects",
               "/06 Photoshop"]
    folder_cycle = 0
    matched = re.match("[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9] - ", name_last_created_folder)
    bool(matched)
    if matched:
        while folder_cycle < 7:
            conn.createDirectory(share, name_last_created_folder + "/" + folders[folder_cycle])
            folder_cycle = folder_cycle + 1
        allowed_folder_counter()
        if random.randint(1, 1000) == 42:
            conn.createDirectory(share, name_last_created_folder + "/07 Furry Yiff")
            special_folder_counter()
    else:
        conn.deleteDirectory(share, name_last_created_folder)
        deleted_folder_counter()


counted_folders = len(conn.listPath(share, "/"))
while True:
    if len(conn.listPath(share, "/")) > counted_folders:
        print(len(conn.listPath(share, "/")))
        number_of_folders = len(conn.listPath(share, "/")) - 1
        name_last_created_folder = conn.listPath(share, "/")[number_of_folders].filename
        if name_last_created_folder != "New folder" and name_last_created_folder != "Neuer Ordner" and name_last_created_folder != "untitled folder":
            print("Folder " + name_last_created_folder + " was created at " + getdate.now().strftime("%H:%M:%S"))
            folder_name = conn.listPath(share, "/")[number_of_folders].filename
            total_folder_counter()
            check()
            counted_folders = len(conn.listPath(share, "/"))

    if len(conn.listPath(share, "/")) < counted_folders:
        counted_folders = len(conn.listPath(share, "/"))
