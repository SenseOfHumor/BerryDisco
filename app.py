import streamlit as st
from db import create_event, get_songs, add_song_to_event, get_event_name, container  # Import functions from db.py
from youtube import search_youtube
#from player import player

# Set up initial states
if "event_id" not in st.session_state:
    st.session_state["event_id"] = None

if "event_name" not in st.session_state:
    st.session_state["event_name"] = None

if "songs" not in st.session_state:
    st.session_state["songs"] = []

if "song_pointer" not in st.session_state:
    st.session_state.song_pointer = 0  # Pointer to track which song is currently playing

if 'youtube_links' not in st.session_state:
    st.session_state['youtube_links'] = {}  # To cache fetched YouTube links for songs

#######################################################################
## EVERYTHING RELATED TO THE SIDEBAR GOES HERE ##
#######################################################################
st.sidebar.title("THE PLAYLIST 🎶")

# Show the list of songs for the event in the sidebar
if st.session_state["event_id"]:
    st.sidebar.subheader(f"Songs for {st.session_state['event_name']}:")
    if st.session_state["songs"]:
        for song in st.session_state["songs"]:
            st.sidebar.write(f"- {song}")
    else:
        st.sidebar.write("No songs added yet.")

#######################################################################
## EVERYTHING RELATED TO THE MAIN PAGE GOES HERE ##
#######################################################################
st.title("BERRY DISCO 🍇🕺🏽")
st.info("Welcome to Berry (Very) Disco! 🍇🕺🏽")

st.subheader("Create your own disco")

# Text input field for event name
event_name = st.text_input("Enter the event name:", "Berry Disco")

# Button to create a new disco (event)
if st.button("Create Disco!"):
    # Call the create_event function from db.py to create a new event
    event_id = create_event(container, event_name)  # Assuming container is set up in db.py

    # Save the event_id and event_name in session state
    st.session_state["event_id"] = event_id
    st.session_state["event_name"] = event_name
    
    # Retrieve the songs for this event and update the session state
    st.session_state["songs"] = get_songs(container, event_id)
    
    # Display the event ID and name
    st.success(f"Disco created! 🎉 Event ID: {event_id}")
    st.info(f"You are now the DJ of '{event_name}'! 🎧🎶")
    st.caption(f"Here is your event ID: {event_id}. Share this with your friends to join the Disco!")

st.subheader("Enter your 6-digit code to join the Disco!")
code = st.text_input("Code:")

if code and len(code) == 6:  # Ensure the code is exactly 6 digits
    # Fetch the event name by the provided code (event_id)
    event_name = get_event_name(container, code)
    
    if event_name:
        st.session_state["event_id"] = code
        st.session_state["event_name"] = event_name
        
        # Retrieve the existing songs for this event
        st.session_state["songs"] = get_songs(container, code)
        
        st.toast("Code accepted! 🎉")
        st.info(f"You have joined the Disco: {event_name} 🍇🕺🏽")

        # Adding song text input
        new_song = st.text_input("Add a song to the Disco")
        if st.button("Add Song"):
            if new_song:
                # Add the new song to the event
                add_song_to_event(container, code, new_song)
                st.session_state["songs"].append(new_song)  # Update session state with the new song
                st.success(f"Added song: {new_song} to {event_name}")
            else:
                st.warning("Please enter a valid song name.")

        # turning the songs into an array of names
        music_array = []
        link_array = []
        for song in st.session_state["songs"]:
            music_array.append(song)
        #st.write(music_array)
        print(music_array)


        ## creating a new array of youtube links
        for track in music_array:
            link=search_youtube(track)
            link_array.append(link)
        st.write(link_array)
        
        # Display the player
        #player(link_array)


        
            


