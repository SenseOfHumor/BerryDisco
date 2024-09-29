import streamlit as st
import os

# Function to save song request to a text file
def save_song_request(song):
    file_path = "song_requests.txt"
    
    # If the file doesn't exist, create it
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("[]")  # Write an empty array format
    
    # Load the existing list of songs from the file
    with open(file_path, "r") as file:
        content = file.read().strip()
        if content:
            songs = eval(content)  # Use eval to load the array format from text
        else:
            songs = []
    
    # Append the new song to the list
    songs.append(song)
    
    # Save the updated list back to the file
    with open(file_path, "w") as file:
        file.write(str(songs))

# Function to read and return the playlist from the text file
def get_playlist():
    file_path = "song_requests.txt"
    
    # If the file doesn't exist or is empty, return an empty list
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r") as file:
        content = file.read().strip()
        if content:
            return eval(content)  # Use eval to interpret the array from the text
        else:
            return []

#######################################################################
## EVERYTHING RELATED TO THE SIDEBAR GOES HERE ##
#######################################################################

# Title for the sidebar
st.sidebar.title("THE PLAYLIST 🎶")

# Initialize session state for theme_input and music recommendation in the sidebar
if "theme_input" not in st.session_state:
    st.session_state.theme_input = ""

if "music_recommendation" not in st.session_state:
    st.session_state.music_recommendation = ""

# Input and button in the sidebar
theme_input = st.sidebar.text_input("Enter your theme here", st.session_state.theme_input)

if st.sidebar.button("Submit"):
    st.session_state.theme_input = theme_input  # Store the input in session state

# Button to show the playlist in the sidebar
if st.sidebar.button("Show Playlist"):
    playlist = get_playlist()
    if playlist:
        st.sidebar.subheader("Current Playlist:")
        for song in playlist:
            st.sidebar.write(f"- {song}")
    else:
        st.sidebar.write("No songs in the playlist yet.")

#######################################################################
## EVERYTHING RELATED TO THE MAIN PAGE GOES HERE ##
#######################################################################

# Title for the main page
st.title("BERRY DISCO 🍇🕺🏽")
st.info("Welcome to Berry (Very) Disco! 🍇🕺🏽")

# Main page: Enter your NJIT ID
st.subheader("Enter your NJIT ID to join the Disco!")

njit_id_input = st.text_input("Enter your NJIT ID:")

if njit_id_input:
    # Check if the input contains "njit.edu"
    if "njit.edu" in njit_id_input:
        # Update the page title
        st.title("Welcome to the event 🎉")
        
        # Allow the user to add music to the playlist
        song_request = st.text_input("Request a song to add to the playlist:")
        
        if st.button("Add Song"):
            if song_request:
                save_song_request(song_request)
                st.success(f"'{song_request}' has been added to the playlist! 🎶")
            else:
                st.warning("Please enter a song to add.")
    else:
        st.error("Invalid NJIT ID. Please use a valid NJIT email ID (e.g., yourname@njit.edu).")

