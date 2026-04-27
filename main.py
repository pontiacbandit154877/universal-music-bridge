from api_modules import spotify_api
from api_modules.tidal_api import tidal_api, tidal_init
from api_modules.youtube_api import youtube_api
from api_modules.spotify_api import spotify_search

tidal_init()

def search_apis(query, types, apis):
    # Accepted types are: 'albums', 'singles', 'songs', 'compilations', 'artists'
    # Accepted apis are: 'tidal', 'youtube', 'spotify'
    print(f"Searching for {types} {query} on {apis}")
    tidal_results = []
    youtube_results = []
    spotify_results = []

    for api in apis:
        match api:
            case "tidal":
                for type in types:
                    results = tidal_api(query, type)
                    tidal_results.append(results)
            case "youtube":
                for type in types:
                    results = youtube_api(query, type)
                    youtube_results.append(results)
            case "spotify":
                for type in types:
                    results = spotify_search(query, type)
                    spotify_results.append(results)

    return tidal_results, youtube_results, spotify_results