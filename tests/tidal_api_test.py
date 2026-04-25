from api_modules.tidal_api import tidal_init, tidal_api

tidal_init()

album_list, top_album = tidal_api(category="album", query="I LAY DOWN MY LIFE FOR YOU")

single_list, top_single = tidal_api(category="single", query="Lift Yourself")
## song_list = tidal_api(category="song", query="loop it and leave it")
## artist_list = tidal_api(category="artist", query="JPEGMAFIA")
## compilation_list = tidal_api(category="compilation", query="We Live in a Society")

print("Printing Albums...")
for album in album_list:
    attr = album.get('attributes', {})
    print(f"ID: {album['id']}")
    print(f"Title: {attr.get('title')}")
    print(f"Duration: {attr.get('duration')}")
    print(f"Tracks: {attr.get('numberOfItems')}\n")

print("Top Album:")
attr = top_album.get('attributes', {})
print(f"ID: {top_album['id']}")
print(f"Title: {attr.get('title')}")

print("Printing Singles...")
for single in single_list:
    attr = single.get('attributes', {})
    print(f"ID: {single['id']}")
    print(f"Title: {attr.get('title')}")
    print(f"Duration: {attr.get('duration')}")
    print(f"Tracks: {attr.get('numberOfItems')}\n")

print("Top Single:")
attr = top_single.get('attributes', {})
print(f"ID: {top_single['id']}")
print(f"Title: {attr.get('title')}")

print("Printing Songs...")
for song in song_list:
    attr = song.get('attributes', {})
    print(f"ID: {song['id']}")
    print(f"Title: {attr.get('title')}\n")

print("Printing Artists...")
for artist in artist_list:
    attr = artist.get('attributes', {})
    print(f"ID: {artist['id']}")
    print(f"Name: {attr.get('name')}\n")