import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")  # Store your YouTube API key in a .env file

# YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

def search_youtube(song_name):
    # Call the YouTube API to search for the song
    request = youtube.search().list(
        part="snippet",
        q=song_name,
        maxResults=1,  # We only want the top result
        type="video"   # Search for videos only
    )
    response = request.execute()

    # Extract video URL
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None  # No results found

def get_music_youtube_urls(music_list):
    # Loop through each song in the music list and get its YouTube URL
    for index, song in music_list.items():
        song_name = song['music_name']
        youtube_url = search_youtube(song_name)
        song['youtube_url'] = youtube_url  # Add the YouTube URL to the song data

    return music_list

# Example Input
music_list = {
    0: {"music_name": "Lost - Faime"},
    1: {"music_name": "Blinding Lights - The Weeknd"},
    2: {"music_name": "Watermelon Sugar - Harry Styles"},
    3: {"music_name": "By Your Side - Calvin Harris ft. Tom Grennan"},
    4: {"music_name": "Kings & Queens - Ava Max"},
    5: {"music_name": "Peaches - Justin Bieber ft. Daniel Caesar, Giveon"},
    6: {"music_name": "Floating on A Cloud - Monma, cocabona "},
    7: {"music_name": "Summer's Day [v2] - jinsang (Lofi)"},
    8: {"music_name": "Dance Monkey - Tones and I (EDM)"},
    9: {"music_name": "Higher Power - Coldplay"}
}

# Fetch YouTube URLs for each song
youtube_urls = get_music_youtube_urls(music_list)

# Output the result
import json
print(json.dumps(youtube_urls, indent=4))


