import base64
import os
import json
from pathlib import Path

import requests
import tidalapi as tidal

from dotenv import load_dotenv, set_key
from datetime import datetime
from datetime import timedelta

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

session = tidal.Session()

TIDAL_API_ID = os.getenv('TIDAL_API_ID')
TIDAL_API_SECRET = os.getenv('TIDAL_API_SECRET')
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
    if ACCESS_TOKEN and ACCESS_TOKEN != "None" and EXPIRY_TIME_UNFORMATTED and EXPIRY_TIME_UNFORMATTED != "None":
        try:
            expiry = datetime.strptime(EXPIRY_TIME_UNFORMATTED, "%Y-%m-%d %H:%M:%S.%f")

            if datetime.now() < expiry:
                session.access_token = ACCESS_TOKEN
                session.token_type = TOKEN_TYPE
                session.request_session.headers.update({"Authorization": f"{TOKEN_TYPE} {ACCESS_TOKEN}"})

                return True

        except Exception as e:
            print(f"Token reload failed: {e}")

    return create_session()


def create_session():
    auth_str = f"{TIDAL_API_ID}:{TIDAL_API_SECRET}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {"Authorization": f"Basic {encoded_auth}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post("https://auth.tidal.com/v1/oauth2/token", headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()

        session.access_token = token_data['access_token']
        session.token_type = token_data['token_type']

        session.request_session.headers.update({
            "Authorization": f"{session.token_type} {session.access_token}"
        })

        session.expiry_time = datetime.now() + timedelta(seconds=token_data.get('expires_in', 86400))

        save_session_to_env()
        return True
    else:
        print(f"Failed to get app token: {response.text}")
        return False

def tidal_init():
    print(f"Login Status: {load_session_from_env()}")
    session.country_code="US"

def tidal_api(category, query):
    match category:
        case "albums":
            return tidal_search_album(query)
        case "artists":
            return tidal_search_artist(query)
        case "compilations":
            return tidal_search_compilation(query)
        case "songs":
            return tidal_search_song(query)
    return None

def tidal_search(query, explicitFilter, countryCode, type):
    query_formatted = query.replace(" ", "%20")

    headers = {
        'accept': 'application/vnd.api+json',
        "Authorization": f"Bearer {session.access_token}"
    }

    params = {
        'explicitFilter': explicitFilter,
        'countryCode': countryCode,
        'include': f"{type},artists",
    }

    response = requests.get(
        f'https://openapi.tidal.com/v2/searchResults/{query_formatted}',
        params=params,
        headers=headers,
    )

    print(f"Requesting URL: {response.url}")

    if response.status_code == 200:
        response_json = response.json()
        results = response_json["included"]
        print(results)

        return results
    else:
        print(f"Search Failed: {response.status_code} - {response.text}")
        return []


def get_artist_info(item_id, item_type="albums"):
    headers = {
        'accept': 'application/vnd.api+json',
        "Authorization": f"Bearer {session.access_token}"
    }
    params = {'include': 'artists', 'countryCode': 'US'}

    # dynamically inject 'albums' or 'tracks' into the URL
    url = f'https://openapi.tidal.com/v2/{item_type}/{item_id}/relationships/artists'
    response = requests.get(url, params=params, headers=headers)

    artist_info = {"name": "Unknown Artist", "link": "No Link Available"}

    if response.status_code == 200:
        print(f"Artist lookup for {item_type} succeeded.")
        res_json = response.json()
        included = res_json.get("included", [])

        for item in included:
            if item.get('type') == 'artists':
                attr = item.get('attributes', {})
                artist_info["name"] = attr.get('name', 'Unknown Artist')

                links = attr.get('externalLinks', [])

                if links:
                    artist_info["link"] = links[0].get('href')
                return artist_info

    print(f"Artist lookup for {item_type} failed.")
    return artist_info


def clean_result(item, type, artist_info=None):
    # Accepted parameters for type are: 'album', 'song', 'artist', 'compilation'
    attr = item.get('attributes', {})
    item_id = item.get('id')

    artist_name = "Unknown Artist"
    artist_link = "No Link Available"

    if artist_info:
        artist_name = artist_info.get("name", "Unknown Artist")
        artist_link = artist_info.get("link", "No Link Available")

    # tidal url structure
    if type == 'song':
        link = f"https://tidal.com/track/{item_id}"
    elif type in ['album', 'compilation']:
        link = f"https://tidal.com/album/{item_id}"
    elif type == 'artist':
        link = f"https://tidal.com/artist/{item_id}"
    else:
        link = "No Link Available"

    images = attr.get('imageLinks', [])
    thumbnail = images[0].get('href') if images else None

    clean_dict = {
        "link": link,
        "thumbnail": thumbnail,
        "source": "Tidal API",
        "explicit": attr.get('explicit')
    }

    match type:
        case 'album' | 'compilation':
            clean_dict.update({
                "type": type,
                "title": attr.get('title'),
                "track_count": attr.get('numberOfItems'),
                "duration": attr.get('duration'),
                "release_date": attr.get('releaseDate'),
                "artist": artist_name,
                "artist_link": artist_link
            })
            return clean_dict

        case 'song':
            clean_dict.update({
                "type": type,
                "title": attr.get('title'),
                "release_date": attr.get('releaseDate'),
                "artist": artist_name,
                "artist_link": artist_link
            })
            return clean_dict

        case 'artist':
            clean_dict.update({
                "type": "artist",
                "title": attr.get('name'),
            })
            return clean_dict

    return None

def tidal_search_album(query):
    print(f"Searching for album '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'albums')

    album_items = [item for item in results if item['type'] == 'albums']

    top_album = max(album_items, key=lambda x: x['attributes'].get('popularity', 0))

    top_album_id = top_album.get('id')
    artist_info = get_artist_info(top_album_id)

    cleaned_top_album = clean_result(top_album, 'album', artist_info)

    return cleaned_top_album


def tidal_search_song(query):
    print(f"Searching for song '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'tracks')

    track_items = [item for item in results if item.get('type') == 'tracks']

    if not track_items:
        print(f"No tracks found for '{query}'.")
        return None

    top_song = max(track_items, key=lambda x: x['attributes'].get('popularity', 0))

    # Get the track ID and fetch the artist info specifically for this track
    top_song_id = top_song.get('id')
    artist_info = get_artist_info(top_song_id, "tracks")

    # Pass the artist_info into clean_result
    cleaned_top_song = clean_result(top_song, 'song', artist_info)

    return cleaned_top_song

def tidal_search_artist(query):
    print(f"Searching for artist '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'artists')

    top_artist = max(results, key=lambda x: x['attributes'].get('popularity', 0))

    cleaned_top_artist = clean_result(top_artist, 'artist')

    return cleaned_top_artist

def tidal_search_compilation(query):
    print(f"Searching for EPs: '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'albums')

    if not results:
        return [], None

    valid_eps = []

    for item in results:
        if item.get('type') in ['albums', 'compilations']:
            attr = item.get('attributes', {})

            album_type = attr.get('albumType')

            num_tracks = attr.get('numberOfItems', 0)

            if album_type == 'EP' or (3 <= num_tracks <= 6):
                valid_eps.append(item)

    if not valid_eps:
        print(f"No EPs found for '{query}'.")
        return [], None

    top_ep = max(valid_eps, key=lambda x: x['attributes'].get('popularity', 0), default=None)

    top_ep_id = top_ep.get('id')
    artist_info = get_artist_info(top_ep_id)

    cleaned_top_ep = clean_result(top_ep, 'compilation', artist_info)

    return cleaned_top_ep