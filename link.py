import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import isodate

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")  # Store your YouTube API key in a .env file

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

def search_youtube(song_name):
    """
    This function takes a song name and fetches its corresponding YouTube URL and duration using the YouTube API.
    
    Parameters:
        song_name (str): The name of the song to search for on YouTube.
        
    Returns:
        tuple: The YouTube URL of the song and its duration in seconds, or an error message.
    """
    try:
        # Call the YouTube API to search for the song
        request = youtube.search().list(
            part="snippet",
            q=song_name,
            maxResults=1,  # We only want the top result
            type="video"   # Search for videos only
        )
        response = request.execute()

        # Extract video URL and video ID
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Fetch the video details to get the duration
            video_details = youtube.videos().list(
                part="contentDetails",
                id=video_id
            ).execute()

            # Extract the duration in ISO 8601 format and convert to seconds
            duration_iso = video_details['items'][0]['contentDetails']['duration']
            duration_seconds = isodate.parse_duration(duration_iso).total_seconds()
            
            return video_url, duration_seconds  # Return video URL and duration in seconds
        else:
            return "No results found for the song.", 0
    
    except HttpError as e:
        if e.resp.status == 403 and "quotaExceeded" in str(e):
            return "Error: Quota exceeded for YouTube API.", 0
        return f"Error occurred: {e}", 0
