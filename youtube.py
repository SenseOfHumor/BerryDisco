import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json

def get_music_youtube_urls_from_list(music_list):
    """
    This function takes a list of music names and fetches their corresponding YouTube URLs using the YouTube API.
    
    Parameters:
        music_list (list): A list of dictionaries where each dictionary contains the song name in 'music_name'.
        
    Returns:
        str: JSON formatted string with 'youtube_url' key added for each song.
    """

    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")  # Store your YouTube API key in a .env file

    # YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    # Function to search for a song on YouTube and return the first video URL
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

    # Loop through each song in the music list and get its YouTube URL
    for song in music_list:
        song_name = song['music_name']
        youtube_url = search_youtube(song_name)
        song['youtube_url'] = youtube_url  # Add the YouTube URL to the song data

    # Return the updated music list in JSON format
    return json.dumps(music_list, indent=4)
