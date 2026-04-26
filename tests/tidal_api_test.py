from api_modules.tidal_api import tidal_init, tidal_api

tidal_init()

top_album = tidal_api(category="albums", query="I LAY DOWN MY LIFE FOR YOU")

top_song = tidal_api(category="songs", query="loop it and leave it")
top_artist = tidal_api(category="artists", query="JPEGMAFIA")
top_compilation = tidal_api(category="compilations", query="We Live in a Society")

print("Printing Albums...")

print(top_album)

print("Printing Songs...")

print(top_song)

print("Printing Artists...")

print(top_artist)

print("Printing Compilation...")

print(top_compilation)