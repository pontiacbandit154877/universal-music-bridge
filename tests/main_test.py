import main

tidal_song_results, youtube_song_results, spotify_song_results = main.search_apis('loop it and leave it', ['songs'], ['tidal', 'youtube', 'spotify'])
tidal_album_results, youtube_album_results, spotify_album_results = main.search_apis('I LAY DOWN MY LIFE FOR YOU', ['albums'], ['tidal', 'youtube', 'spotify'])


print("\nPrinting Tidal Song Results...")
print(tidal_song_results)
print("\nPrinting Youtube Results...")
print(youtube_song_results)
print("\nPrinting Spotify Results...")
print(spotify_song_results)

print("\nPrinting Tidal Album Results...")
print(tidal_album_results)
print("\nPrinting Youtube Album Results...")
print(youtube_album_results)
print("\nPrinting Spotify Album Results...")
print(spotify_album_results)