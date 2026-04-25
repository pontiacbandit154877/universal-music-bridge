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
        case "album":
            return tidal_search_album(query)
        case "artist":
            return tidal_search_artist(query)
        case "compilation":
            return tidal_search_compilation(query)
        case "song":
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
        'include': type,
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

def tidal_search_album(query):
    print(f"Searching for album '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'albums')

    top_album = max(results, key=lambda x: x['attributes'].get('popularity', 0))

    print(f"Top Result: {top_album['attributes']['title']}")
    print(f"Score: {top_album['attributes']['popularity']}")

    return results, top_album


def tidal_search_song(query):
    print(f"Searching for song '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'tracks')

    top_song = max(results, key=lambda x: x['attributes'].get('popularity', 0))

    return results, top_song

def tidal_search_artist(query):
    print(f"Searching for artist '{query}'")

    results = tidal_search(query, "INCLUDE", 'US', 'artists')

    top_artist = max(results, key=lambda x: x['attributes'].get('popularity', 0))

    return results, top_artist

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

    return valid_eps, top_ep




