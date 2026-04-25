from api_modules.tidal_api import tidal_init, tidal_api

tidal_init()

album_list, top_album = tidal_api(category="album", query="I LAY DOWN MY LIFE FOR YOU")

song_list, top_song = tidal_api(category="song", query="loop it and leave it")
artist_list, top_artist = tidal_api(category="artist", query="JPEGMAFIA")
compilation_list, top_compilation = tidal_api(category="compilation", query="We Live in a Society")

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

print("Top Artist:")
attr = top_artist.get('attributes', {})
print(f"ID: {top_artist['id']}")
print(f"Name: {attr.get('name')}")

print("Printing Compilation...")
for compilation in compilation_list:
    attr = compilation.get('attributes', {})
    print(f"ID: {compilation['id']}")
    print(f"Title: {attr.get('title')}")
    print(f"Duration: {attr.get('duration')}")
    print(f"Tracks: {attr.get('numberOfItems')}\n")

print("Top Compilation:")
attr = top_compilation.get('attributes', {})
print(f"ID: {top_compilation['id']}")
print(f"Title: {attr['title']}")
print(f"Duration: {attr['duration']}")
print(f"Tracks: {attr['numberOfItems']}\n")