import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")  # Store your YouTube API key in a .env file

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

def search_youtube(song_name):
    """
    This function takes a song name and fetches its corresponding YouTube URL using the YouTube API.
    
    Parameters:
        song_name (str): The name of the song to search for on YouTube.
        
    Returns:
        str: The YouTube URL of the song or an error message.
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

        # Extract video URL
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return "No results found for the song."
    
    except HttpError as e:
        if e.resp.status == 403 and "quotaExceeded" in str(e):
            return "Error: Quota exceeded for YouTube API."
        return f"Error occurred: {e}"

def main():
    """
    Main function to handle user input and display the YouTube URL.
    """
    while True:
        # Get the song name from the user
        song_name = input("Enter the name of the song (or type 'exit' to quit): ")

        if song_name.lower() == 'exit':
            print("Exiting the program.")
            break

        # Search for the song on YouTube
        youtube_url = search_youtube(song_name)

        # Print the result
        print(f"Link: {youtube_url}\n")

if __name__ == "__main__":
    main()
