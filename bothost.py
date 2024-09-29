import streamlit as st
import time
import json
from link import search_youtube  # Fetch YouTube links using search_youtube
import os
from dotenv import load_dotenv
from openai import OpenAI

# Function to embed a YouTube video with autoplay
def embed_autoplay_youtube(video_url):
    video_id = video_url.split("v=")[1]  # Extract video ID from URL
    video_html = f"""
        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/{video_id}?autoplay=1"
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """
    st.components.v1.html(video_html, height=315)

# The provided unchanged AI-powered music recommendation function
def get_music_recommendations(theme_input):
    """
    This function takes a party theme as input and returns a list of recommended songs with their corresponding YouTube URLs.

    Parameters:
        theme_input (str): The theme of the party entered by the user.

    Returns:
        str: A JSON formatted string containing the music recommendations and YouTube URLs.
    """
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPEN_AI_API")

    # Instantiate the OpenAI client
    client = OpenAI(api_key=api_key)

    # AI-powered music recommendation based on the theme_input
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps to find good and new music based on the hackathon theme."},
            {
                "role": "user",
                "content": f"""
                This is the hackathon theme: {theme_input}

                Consider the following:
                - If the user enters the theme of the party, the assistant should suggest 10 music based on the theme.
                - Suggestions should be newer music.
                - The assistant should suggest music that is popular and well-liked by the majority of people.
                - The assistant should provide a variety of music genres to cater to different preferences.
                - The assistant should try to blend some chill music 
                - The assistant should provide some lofi music
                - The assistant should provide some EDM music
                - The assistant should keep in mind that the music should not be explicit or offensive.

                Return the schedule in JSON format without any additional text:
                [
                    {{
                        "music_name": "name of the music"
                    }}
                ]
                """
            }
        ]
    )

    # Extract and process the response from OpenAI
    response_text = response.choices[0].message.content.strip()

    try:
        music_list = json.loads(response_text)
    except json.JSONDecodeError:
        return f"Failed to decode response as JSON. Raw output: {response_text}"

    # Fetch YouTube URLs for the recommended music using search_youtube
    for song in music_list:
        song_name = song["music_name"]
        try:
            link, duration = search_youtube(song_name)  # Fetch link and duration using search_youtube
            song["youtube_url"] = link  # Add YouTube URL to the song
            song["duration"] = duration  # Add duration to the song
        except Exception as e:
            return f"Error fetching YouTube link for {song_name}: {str(e)}"
    
    # Return the result as a JSON string
    return json.dumps(music_list)

# Set up session states
if "songs" not in st.session_state:
    st.session_state["songs"] = []

if "song_pointer" not in st.session_state:
    st.session_state.song_pointer = 0  # Pointer to track which song is currently playing

# Input for Hackathon theme
st.title("GROOVY by BERRY DISCO 🍇🕺🏽")
theme_input = st.text_input("Enter the theme for your hackathon:")

# Button to get song recommendations based on theme
if st.button("Get Music Recommendations"):
    if theme_input:
        # Use your AI recommendations function (unchanged)
        song_recommendations = get_music_recommendations(theme_input)
        st.session_state["songs"] = json.loads(song_recommendations)

        st.success("Music recommendations and links generated! 🎶")
    else:
        st.error("Please enter a theme for the hackathon!")

# Display song list and play the current song
if st.session_state["songs"]:
    st.subheader("Recommended Songs")
    for song in st.session_state["songs"]:
        st.write(f"- {song['music_name']}")

    # Prepare YouTube links and durations
    link_array = [song['youtube_url'] for song in st.session_state["songs"]]
    duration_array = [song['duration'] for song in st.session_state["songs"]]

    # Play the current song and set up autoplay for the next one
    if link_array:
        current_song = link_array[st.session_state.song_pointer]
        current_duration = duration_array[st.session_state.song_pointer]

        st.write(f"Now playing: {st.session_state['songs'][st.session_state.song_pointer]['music_name']}")
        embed_autoplay_youtube(current_song)

        # Automatically play the next song after the current one finishes
        time.sleep(current_duration)

        # Move pointer to next song or loop back
        if st.session_state.song_pointer < len(link_array) - 1:
            st.session_state.song_pointer += 1
        else:
            st.session_state.song_pointer = 0

        st.experimental_rerun()  # Re-run to update the player
