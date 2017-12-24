from spotipy import Spotify
from authorize import authorize
from constants import strings
from pprint import pprint

from random import shuffle
import threading

import tkinter as tk
from tkinter import ttk
import os

global username
username = None
if os.path.isfile("lastuser"):
    with open("lastuser", "r") as f:
        username = f.readline()

global playlists
global spoofy
global logged_in
playlists = []
logged_in = False


def _login():   # The login button (also called for auto-login if user was logged in last time)
    global username
    global spoofy
    global logged_in
    global playlists

    username_submit.state(["disabled"])
    if logged_in:    # Logged in logging out
        print("logging out")
        username = None
        playlist_list.delete(0, playlist_list.size() - 1)
        playlists = []
        os.remove("lastuser")
        logged_in = False

    else:           # Logged out loggin in
        spoofy = Spotify(auth=authorize(username))
        user_id = spoofy.me()["id"]

        # Get who we are logged in as
        if username != user_id:
            username = user_id
            with open("lastuser", "w") as f:
                f.write(username)

        logged_in = True

    set_login_state()
    username_submit.state(["!disabled"])

def login():
    thread = threading.Thread(target=_login)
    thread.start()

def get_playlists():
    global playlists
    global spoofy
    print(playlists)
    user_id = spoofy.me()["id"]
    #pprint(spoofy.current_user_playlists()["items"])
    for playlist in spoofy.current_user_playlists()["items"]:
        # check if it is collaborative or if we own it
        if playlist["collaborative"] or playlist["owner"]["id"] == user_id:
            playlists.append([playlist["name"], playlist["id"]])

    str_playlists = ""
    for playlist in playlists:
        str_playlists = str_playlists + "\"" + playlist[0] + "\" "
    ui_playlists.set(str_playlists)

def _shuffle_playlist():
    global playlists
    global spoofy
    ui_progress.set(0)
    selected = playlist_list.curselection()[0]
    playlist = playlists[selected][1]
    total = spoofy.user_playlist_tracks(username, playlist)["total"]
    new_order = list(range(total))
    print(type(new_order))
    shuffle(new_order)
    for i in range(total):
        spoofy.user_playlist_reorder_tracks(username, playlist, i, new_order[i] + 1)
        ui_progress.set(round(i/total*100))
    print("Done!")
    ui_progress.set(0)

def shuffle_playlist():
    thread = threading.Thread(target=_shuffle_playlist)
    thread.start()

def set_login_state():
    if logged_in:
        ui_username.set(strings.logged_in_as.format(username))
        ui_login.set(strings.log_out)
        get_playlists()
    else:
        ui_username.set(strings.not_logged_in)
        ui_login.set(strings.log_in)


# UI configuration
root = tk.Tk()
root.title(strings.title)
root.resizable(False, False)
mainframe = ttk.Frame(root)

#username_frame = ttk.Frame(mainframe)
ui_username = tk.StringVar()
ui_login = tk.StringVar()
ui_playlists = tk.StringVar()


#username_box = ttk.Entry(username_frame, exportselection=0, textvariable=ui_username)
username_label = ttk.Label(mainframe, textvariable=ui_username)
username_submit = ttk.Button(mainframe, textvariable=ui_login, command=login)


playlist_list = tk.Listbox(mainframe, exportselection=0, listvariable=ui_playlists, selectmode=tk.SINGLE)
playlist_submit = ttk.Button(mainframe, text="Shuffle", command=shuffle_playlist)

ui_progress = tk.IntVar()
progressbar = ttk.Progressbar(mainframe, variable=ui_progress)


# Final main setup
# If we know the username, login
if username:
    _login()
else:   # else, set up UI strings and wait for the user to intiate
    set_login_state()

# Final UI build
progressbar.grid(row=4, column=0, sticky="WE")
#username_box.grid(row=0, column=0)
username_submit.grid(row=1, column=0)
username_label.grid(row=0, column=0)
#username_frame.grid(row=0, column=0)
playlist_list.grid(row=2, column=0)
playlist_submit.grid(row=3, column=0)
mainframe.grid(row=0, column=0)
root.mainloop()