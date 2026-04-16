import os
import tidalapi as tidal

from dotenv import load_dotenv, set_key
from datetime import datetime

env_path = '.env'
load_dotenv(dotenv_path=env_path)

session = tidal.Session()

TOKEN = os.getenv("TIDAL_API_TOKEN")
TOKEN_TYPE = os.getenv("TIDAL_SESSION_TOKEN_TYPE")
ACCESS_TOKEN = os.getenv("TIDAL_SESSION_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("TIDAL_SESSION_REFRESH_TOKEN")
EXPIRY_TIME_UNFORMATTED = os.getenv("TIDAL_SESSION_EXPIRY_TIME")

def save_session_to_env():
    set_key(env_path, "TIDAL_SESSION_TOKEN_TYPE", str(session.token_type))
    set_key(env_path, "TIDAL_SESSION_ACCESS_TOKEN", str(session.access_token))
    set_key(env_path, "TIDAL_SESSION_REFRESH_TOKEN", str(session.refresh_token))
    set_key(env_path, "TIDAL_SESSION_EXPIRY_TIME", str(session.expiry_time))
    print("Session Saved!")

def load_session_from_env():
    if TOKEN_TYPE != "":
        try:
            expiry_time_formatted = datetime.strptime(EXPIRY_TIME_UNFORMATTED, "%Y-%m-%d %H:%M:%S.%f")
            session.load_oauth_session(TOKEN_TYPE, ACCESS_TOKEN, REFRESH_TOKEN, expiry_time_formatted)
            return True
        except Exception as e:
            print(f"Stored session invalid: {e}")
            session.login_oauth_simple(fn_print=print)
            save_session_to_env()
            return False
    else:
        session.login_oauth_simple(fn_print=print)
        save_session_to_env()
        return False

def tidal_init():
    print(f"Login Status: {load_session_from_env()}")

def tidal_api(category, query):
    match category:
        case "album":
            return tidal_search_album(query)
        case "single":
            return tidal_search_single(query)
        case "artist":
            return tidal_search_artist(query)
        case "compilation":
            return tidal_search_compilation(query)
        case "song":
            return tidal_search_song(query)
    return None

def tidal_search_album(query):
    print("Searching Album...")
    album_dict = session.search(query, models=[tidal.Album], limit=10)
    album_list = album_dict.get('albums')

    return album_list

def tidal_search_single(query):
    print("Searching Single...")
    single_dict = session.search(query, models=[tidal.Track], limit=10)
    single_list = single_dict.get('tracks')
    return_list = []

    for track in single_list:
        parent_album = session.album(track.album.id)

        if getattr(parent_album, 'type', None) == 'SINGLE' or parent_album.num_tracks == 1:
            return_list.append(parent_album)

    if len(return_list) > 0:
        return return_list
    return None

def tidal_search_song(query):
    print("Searching Song...")
    song_dict = session.search(query, models=[tidal.Track], limit=10)
    song_list = song_dict.get('tracks')

    return song_list

def tidal_search_artist(query):
    print("Searching Artist...")
    artist_dict = session.search(query, models=[tidal.Artist], limit=10)
    artist_list = artist_dict.get('artists')
    return artist_list

def tidal_search_compilation(query):
    print("Searching Compilation...")
    compilation_dict = session.search(query, models=[tidal.Album], limit=10)
    compilation_list = compilation_dict.get('albums')
    results_list = []

    for album in compilation_list:

        if album.type == 'EP':
            results_list.append(album)

    return results_list

