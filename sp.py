import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up the credentials
client_id = '275cc3fac2494416800523700557049e'  # Replace with your client ID
client_secret = '472901ec1ee54190a34afb5a64eb9d52'  # Replace with your client secret

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def search_song(song_name):
    # Search for a song by name
    result = sp.search(q=song_name, type='track', limit=2)
    
    if result['tracks']['items']:
        song = result['tracks']['items'][0]
        song_info = {
            'name': song['name'],
            'artist': song['artists'][0]['name'],
            'album': song['album']['name'],
            'release_date': song['album']['release_date'],
            'url': song['external_urls']['spotify']
        }
        return song_info
    else:
        return None

# Example usage
song_name = input("Enter the name of the song you want to search: ")
song_info = search_song(song_name)

if song_info:
    print(f"Song: {song_info['name']}")
    print(f"Artist: {song_info['artist']}")
    print(f"Album: {song_info['album']}")
    print(f"Release Date: {song_info['release_date']}")
    print(f"Listen on Spotify: {song_info['url']}")
else:
    print("Song not found!")
