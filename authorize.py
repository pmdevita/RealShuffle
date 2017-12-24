import spotipy
from spotipy import oauth2
import constants as consts


def authorize(username):
    # Edited from spotipy source
    if username:
        cache_path = ".cache-" + username
    else:
        cache_path = None
    sp_oauth = oauth2.SpotifyOAuth(consts.client_id, consts.client_secret, consts.redirect_uri, scope=consts.scopes(),
                                   cache_path=cache_path)

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        # We need authorization
        import webbrowser
        from flask import Flask, request

        app = Flask(__name__)
        global code
        code = None

        def flaskquit():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @app.route("/callback")
        def callback():
            global code
            code = request.args["code"]
            flaskquit()
            return consts.strings.close_tab

        auth_url = sp_oauth.get_authorize_url()
        webbrowser.open_new_tab(auth_url)
        app.run()

        token_info = sp_oauth.get_access_token(code)

        if not username:
            # We couldn't cache before without the username, but now we can
            s = spotipy.Spotify(auth=token_info["access_token"])
            username = s.me()["id"]
            sp_oauth.cache_path = cache_path = ".cache-" + username
            sp_oauth._save_token_info(token_info)

    if token_info:
        return token_info["access_token"]
    else:
        raise Exception("We didn't get authorized")