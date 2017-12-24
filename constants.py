_scopes = ["playlist-read-private", "playlist-read-collaborative", "playlist-modify-public", "playlist-modify-private",
          "streaming", "user-read-playback-state", "user-modify-playback-state", "user-read-currently-playing"]

def scopes():
    return " ".join(_scopes)


client_id = "a8923bf64c6248e8b85a6955aee53ee0"
client_secret = "a85eda2c21894adf8ae3c826808c4a4a"
redirect_uri = "http://127.0.0.1:5000/callback"

class strings:
    title = "RealShuffle"
    logged_in_as = "Logged in as {}"
    log_out = "Log out"
    not_logged_in = "Not Logged in"
    log_in = "Log in"
    close_tab = "You can close this tab"