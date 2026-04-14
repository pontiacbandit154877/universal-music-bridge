import json
from ytmusicapi import YTMusic

yt = YTMusic()

def youtube_api(search_query, category):
    if category == "albums":

        search_result = yt.search(search_query, filter=category)
        for album in search_result:


            if search_query.lower() in album['title'].lower():
                print(album)
                browse_id = album['browseId']
                album_link = f"https://music.youtube.com/browse/{browse_id}"
                print(album_link)

    elif category == "songs":

        search_result = yt.search(search_query, filter=category, limit = 4)
        for song in search_result:

            if search_query.lower() in  song['title'].lower():
                print(song)
                video_id = song['videoId']
                link = f"https://music.youtube.com/watch?v={video_id}"
                print(link)


    elif category == "artists":

        search_result = yt.search(search_query, filter=category, limit = 4)
        for artist in search_result:

             if search_query.lower() in artist['artist'].lower():
                print(artist)
                artist_id = artist['browseId']

                link = f"https://music.youtube.com/channel/{artist_id}"
                print(link)

    elif category == "singles":

        search_result = yt.search(search_query, filter='songs', limit = 4)

        for song in search_result:
            album_id  = song['album']['id']
            album_info = yt.get_album(album_id)
            track_count = album_info.get('trackCount')
            print(track_count)
            if track_count <= 6:
                print(song)
                video_id = song['videoId']
                link = f"https://music.youtube.com/watch?v={video_id}"
                print(link)



    #the user has to enter the name of the artist at least
    elif category == "compilations":

        search_result = yt.search(search_query, filter = 'albums', limit = 4)

        compilation_keywords = ['greatest hits', 'best of', 'essential', 'collection']

        for album in search_result:
            is_comp = any(word in album['title'].lower() for word in compilation_keywords) or album['artists'][0]['name'].lower() == "various artists"

            matches_query = search_query.lower() in album['title'].lower() or  search_query.lower() in album['artists'][0]['name'].lower() or album['title'].lower() in search_query.lower() or album['artists'][0]['name'].lower() in search_query.lower()

            if is_comp and matches_query:
                print(album)
                browse_id = album['browseId']
                link = f"https://music.youtube.com/browse/{browse_id}"
                print(link)
print("for song")
youtube_api("Take on me", 'songs')
print("for album")
youtube_api("hit me hard and soft", 'albums')
print("for artist")
youtube_api("MC Hammer", 'artists')
print("for singles")
youtube_api("Lovely", 'singles')
print("for compilation")
youtube_api("Essentials of Billy Joel", 'compilations')

