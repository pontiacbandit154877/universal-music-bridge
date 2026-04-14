import json
from ytmusicapi import YTMusic

yt = YTMusic()

def youtube_api(search_query, category):


    clean_data_list = []


    if category == "albums":

        search_result = yt.search(search_query, filter=category, limit = 4)
        for album in search_result:

            if search_query.lower() in album['title'].lower():
                browse_id = album['browseId']
                link = f"https://music.youtube.com/browse/{browse_id}"

                clean_dict = {
                    "type" : "Album",
                    "title": album['title'],
                    "artist": album['artists'][0]['name'],
                    "link": link,
                    "thumbnail": album['thumbnails'],
                    "source": "YouTube Music"
                }
                clean_data_list.append(clean_dict)
            return(clean_data_list)


    elif category == "songs":

        search_result = yt.search(search_query, filter=category, limit = 4)
        for song in search_result:

            if search_query.lower() in  song['title'].lower():

                video_id = song['videoId']
                link = f"https://music.youtube.com/watch?v={video_id}"
                clean_dict = {
                    "type": "Song",
                    "title": song['title'],
                    "artist": song['artists'][0]['name'],
                    "link": link,
                    "thumbnail": song['thumbnails'],
                    "source": "YouTube Music"
                }
                clean_data_list.append(clean_dict)
        return(clean_data_list)


    elif category == "artists":

        search_result = yt.search(search_query, filter=category, limit = 4)
        for artist in search_result:

             if search_query.lower() in artist['artist'].lower():
                artist_id = artist['browseId']

                link = f"https://music.youtube.com/channel/{artist_id}"
                clean_dict = {
                    "type": "artist",
                    "title": artist['artist'],
                    "artist": artist['artist'],
                    "link": link,
                    "thumbnail": artist['thumbnails'],
                    "source": "YouTube Music"
                }
                clean_data_list.append(clean_dict)
        return(clean_data_list)


    elif category == "singles":

        search_result = yt.search(search_query, filter='songs', limit = 4)

        for song in search_result:
            album_id  = song['album']['id']
            album_info = yt.get_album(album_id)
            track_count = album_info.get('trackCount')
            if track_count <= 6:

                video_id = song['videoId']
                link = f"https://music.youtube.com/watch?v={video_id}"
                clean_dict = {
                    "type": "Song",
                    "title": song['title'],
                    "artist": song['artists'][0]['name'],
                    "link": link,
                    "thumbnail": song['thumbnails'],
                    "source": "YouTube Music"
                }
                clean_data_list.append(clean_dict)
        return(clean_data_list)




    #the user has to enter the name of the artist at least
    elif category == "compilations":

        search_result = yt.search(search_query, filter = 'albums', limit = 4)

        compilation_keywords = ['greatest hits', 'best of', 'essential', 'collection']

        for album in search_result:
            is_comp = any(word in album['title'].lower() for word in compilation_keywords) or album['artists'][0]['name'].lower() == "various artists"

            matches_query = search_query.lower() in album['title'].lower() or  search_query.lower() in album['artists'][0]['name'].lower() or album['title'].lower() in search_query.lower() or album['artists'][0]['name'].lower() in search_query.lower()

            if is_comp and matches_query:
                browse_id = album['browseId']
                link = f"https://music.youtube.com/browse/{browse_id}"
                clean_dict = {
                    "type": "Compilation",
                    "title": album['title'],
                    "artist": album['artists'][0]['name'],
                    "link": link,
                    "thumbnail": album['thumbnails'],
                    "source": "YouTube Music"
                }
                clean_data_list.append(clean_dict)
        return(clean_data_list)
print("for song")
l1 = youtube_api("Take on me", 'songs')
print(l1)
print("for album")
l2 = youtube_api("hit me hard and soft", 'albums')
print(l2)
print("for artist")
l3 = youtube_api("MC Hammer", 'artists')
print(l3)
print("for singles")
l4 = youtube_api("Lovely", 'singles')
print(l4)
print("for compilation")
l5 = youtube_api("Essentials of Billy Joel", 'compilations')
print(l5)

