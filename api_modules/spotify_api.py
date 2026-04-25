import json
from dotenv import load_dotenv
from pathlib import Path
import os
import base64
from requests import post, get

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'

load_dotenv(dotenv_path=env_path)


client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token():
    authorization_string = client_id + ":" + client_secret
    authorization_string_bytes = authorization_string.encode("utf-8")
    authorization_string_base64 = str(base64.b64encode(authorization_string_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + authorization_string_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type" : 'client_credentials'
    }

    result = post(url, headers= headers, data= data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_authorization_header(token):
    return {"Authorization" : "Bearer " + token}

def spotify_search(search_query, category):
    clean_data_list = []
    token = get_token()
    header = get_authorization_header(token)
    url = "https://api.spotify.com/v1/search"

    type_map = {
        "songs": "track",
        "artists": "artist",
        "albums": "album",
        "singles": "album",
        "compilations": "album"
    }

    if category == "artists":

        query = f"?q={search_query}&type=artist&limit=4"
        query_url = url + query
        result = get(query_url, headers=header)
        json_result = json.loads(result.content)['artists']['items']

        for artist in json_result:


            if artist['name'].lower() in search_query.lower():

                clean_dict = {
                    "type": "artist",
                    "title": artist['name'],
                    "artist": artist['name'],
                    "link": artist['external_urls']['spotify'],
                    "thumbnail": artist['images'],
                    "source": "Spotify"
                }

                clean_data_list.append(clean_dict)
        return clean_data_list

    elif category == "songs":

        query = f"?q={search_query}&type=track&limit=4"
        query_url = url + query
        result = get(query_url, headers=header)
        json_result = json.loads(result.content)['tracks']['items']


        for song in json_result:

            if  search_query.lower() in  song['name'].lower():
               clean_dict = {
                    "type": "song",
                    "title": song['name'],
                    "artist": song['artists'][0]['name'],
                    "link": song['external_urls']['spotify'],
                    "thumbnail": song['album']['images'],
                    "source": "Spotify"
                }
               clean_data_list.append(clean_dict)
        return clean_data_list


    elif category == "albums":

        query = f"?q={search_query}&type=album&limit=4"
        query_url = url + query
        result = get(query_url, headers=header)
        json_result = json.loads(result.content)['albums']['items']


        for album in json_result:

            if  search_query.lower() in  album['name'].lower():
               clean_dict = {
                    "type": "song",
                    "title": album['name'],
                    "artist": album['artists'][0]['name'],
                    "link": album['external_urls']['spotify'],
                    "thumbnail": album['images'],
                    "source": "Spotify"
                }
               clean_data_list.append(clean_dict)
        return clean_data_list


    elif category == "singles":

        query = f"?q={search_query}&type=album&limit=4"
        query_url = url + query
        result = get(query_url, headers=header)
        json_result = json.loads(result.content)['albums']['items']

        for album in json_result:
            is_match = search_query.lower() in album['name'].lower()
            is_single = album['album_type'].lower() == "single"

            if is_match and is_single:
                clean_dict = {
                    "type": "single",
                    "title": album['name'],
                    "artist": album['artists'][0]['name'],
                    "link": album['external_urls']['spotify'],
                    "thumbnail": album['images'],
                    "source": "Spotify"
                }
                clean_data_list.append(clean_dict)
        return clean_data_list


    elif category == "compilations":

        query = f"?q={search_query}&type=album&limit=4"
        query_url = url + query
        result = get(query_url, headers=header)
        json_result = json.loads(result.content)['albums']['items']
        comp_keywords = ['greatest hits', 'best of', 'essential', 'collection']


        for album in json_result:

            is_match = search_query.lower() in album['name'].lower()

            is_official_comp = album['album_type'] == 'compilation'
            has_keyword = any(word in album['name'].lower() for word in comp_keywords)

            if is_match or has_keyword or is_official_comp:
                clean_dict = {
                    "type": "compilation",
                    "title": album['name'],
                    "artist": album['artists'][0]['name'],
                    "link": album['external_urls']['spotify'],
                    "thumbnail": album['images'],
                    "source": "Spotify"
                }
                clean_data_list.append(clean_dict)
        return clean_data_list




