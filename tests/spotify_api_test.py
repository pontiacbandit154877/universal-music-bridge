from api_modules.spotify_api import spotify_search



print("for artist:")
l1 = spotify_search("Britney Spears", "artists")
print(l1)
print("for song")
l2 = spotify_search("Hello", "songs")
print(l2)
print("for album")
l3 = spotify_search("hit me hard and soft", 'albums')
print(l3)
print("for singles")
l4 = spotify_search("Flowers", 'singles')
print(l4)
print("for compilations")
l5 = spotify_search("Queen", 'compilations')
print(l5)