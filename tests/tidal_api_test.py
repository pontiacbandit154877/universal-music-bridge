from tidal_api import tidal_api
from tidal_api import tidal_init

tidal_init()

album_list = tidal_api(category="album", query="I LAY DOWN MY LIFE FOR YOU")
single_list = tidal_api(category="single", query="Lift Yourself")
song_list = tidal_api(category="song", query="loop it and leave it")
artist_list = tidal_api(category="artist", query="JPEGMAFIA")
compilation_list = tidal_api(category="compilation", query="We Live in a Society")

print("Printing Albums...")
for album in album_list:
    print(f"ID: {album.id}")
    print(f"Title: {album.name}")
    print(f"Duration: {album.duration} seconds")
    print(f"Artist: {album.artist.name}")
    print(f"Tracks: {album.num_tracks}\n")

print("Printing Singles...")
for single in single_list:
    print(f"ID: {single.id}")
    print(f"Title: {single.name}")
    print(f"Duration: {single.duration} seconds")
    print(f"Artist: {single.artist.name}")
    print(f"Tracks: {single.num_tracks}\n")

print("Printing Songs...")
for song in song_list:
    print(f"ID: {song.id}")
    print(f"Title: {song.name}")
    print(f"Duration: {song.duration} seconds")
    print(f"Artist: {song.artist.name}\n")

print("Printing Artists...")
for artist in artist_list:
    print(f"ID: {artist.id}")
    print(f"Name: {artist.name}\n")

print("Printing Compilations...")
for compilation in compilation_list:
    print(f"ID: {compilation.id}")
    print(f"Title: {compilation.name}")
    print(f"Duration: {compilation.duration} seconds")
    print(f"Artist: {compilation.artist.name}")
    print(f"Tracks: {compilation.num_tracks}\n")
