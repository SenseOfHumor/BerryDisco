# import streamlit as st
# from db import create_event, get_songs, add_song_to_event, get_event_name, container  # Import functions from db.py
# from link import search_youtube
# #from player import player
# import time


# # Function to embed a YouTube video with autoplay
# def embed_autoplay_youtube(video_url):
#     # Extract the video ID from the URL (assuming a standard YouTube link)
#     video_id = video_url.split("v=")[1]

#     # Create the HTML code for embedding the video with autoplay
#     video_html = f"""
#         <iframe width="560" height="315"
#         src="https://www.youtube.com/embed/{video_id}?autoplay=1"
#         frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
#     """

#     # Use Streamlit's HTML component to display the video
#     st.components.v1.html(video_html, height=315)



# # Set up initial states
# if "event_id" not in st.session_state:
#     st.session_state["event_id"] = None

# if "event_name" not in st.session_state:
#     st.session_state["event_name"] = None

# if "songs" not in st.session_state:
#     st.session_state["songs"] = []

# if "song_pointer" not in st.session_state:
#     st.session_state.song_pointer = 0  # Pointer to track which song is currently playing

# if 'song_links' not in st.session_state:
#     st.session_state['song_links'] = {}  # Dictionary to store songs and their YouTube links

# if 'song_durations' not in st.session_state:
#     st.session_state['song_durations'] = {}  # Dictionary to store song durations in seconds

# #######################################################################
# ## EVERYTHING RELATED TO THE SIDEBAR GOES HERE ##
# #######################################################################
# st.sidebar.title("THE PLAYLIST 🎶")

# # Show the list of songs for the event in the sidebar
# if st.session_state["event_id"]:
#     st.sidebar.subheader(f"Songs for {st.session_state['event_name']}:")
#     if st.session_state["songs"]:
#         for song in st.session_state["songs"]:
#             st.sidebar.write(f"- {song}")
#     else:
#         st.sidebar.write("No songs added yet.")

# #######################################################################
# ## EVERYTHING RELATED TO THE MAIN PAGE GOES HERE ##
# #######################################################################
# st.title("BERRY DISCO 🍇🕺🏽")
# st.info("Welcome to Berry (Very) Disco! 🍇🕺🏽")

# st.subheader("Create your own disco")

# # Text input field for event name
# event_name = st.text_input("Enter the event name:", "Berry Disco")

# # Button to create a new disco (event)
# if st.button("Create Disco!"):
#     # Call the create_event function from db.py to create a new event
#     event_id = create_event(container, event_name)  # Assuming container is set up in db.py

#     # Save the event_id and event_name in session state
#     st.session_state["event_id"] = event_id
#     st.session_state["event_name"] = event_name
    
#     # Retrieve the songs for this event and update the session state
#     st.session_state["songs"] = get_songs(container, event_id)
    
#     # Display the event ID and name
#     st.success(f"Disco created! 🎉 Event ID: {event_id}")
#     st.info(f"You are now the DJ of '{event_name}'! 🎧🎶")
#     st.caption(f"Here is your event ID: {event_id}. Share this with your friends to join the Disco!")

# st.subheader("Enter your 6-digit code to join the Disco!")
# code = st.text_input("Code:")

# if code and len(code) == 6:  # Ensure the code is exactly 6 digits
#     # Fetch the event name by the provided code (event_id)
#     event_name = get_event_name(container, code)
    
#     if event_name:
#         st.session_state["event_id"] = code
#         st.session_state["event_name"] = event_name
        
#         # Retrieve the existing songs for this event
#         st.session_state["songs"] = get_songs(container, code)
        
#         st.toast("Code accepted! 🎉")
#         st.info(f"You have joined the Disco: {event_name} 🍇🕺🏽")

#         # Adding song text input
#         new_song = st.text_input("Add a song to the Disco")
#         if st.button("Add Song"):
#             if new_song:
#                 # Add the new song to the event
#                 add_song_to_event(container, code, new_song)
#                 st.session_state["songs"].append(new_song)  # Update session state with the new song
#                 st.success(f"Added song: {new_song} to {event_name}")
#             else:
#                 st.warning("Please enter a valid song name.")

#         ## Fetch YouTube link and duration for each song
#         for song in st.session_state["songs"]:
#             if song not in st.session_state['song_links']:
#                 # Fetch the YouTube link and duration for the song if not already cached
#                 try:
#                     link, duration = search_youtube(song)
#                     st.session_state['song_links'][song] = link  # Cache the link in session state
#                     st.session_state['song_durations'][song] = duration  # Cache the duration in session state
#                 except Exception as e:
#                     st.error(f"Error fetching YouTube link for {song}: {str(e)}")
#                     continue

#         # Prepare the list of YouTube links for the player
#         link_array = list(st.session_state['song_links'].values())
#         duration_array = list(st.session_state['song_durations'].values())

#         # Play the current song and set up auto-play for the next one
#         current_song = link_array[st.session_state.song_pointer]
#         current_duration = duration_array[st.session_state.song_pointer]

#         st.write(f"Now playing: {st.session_state['songs'][st.session_state.song_pointer]}")
#         embed_autoplay_youtube(current_song)

#         # Automatically press 'Next' after the song duration ends
#         time.sleep(current_duration)
#         if st.session_state.song_pointer < len(link_array) - 1:
#             st.session_state.song_pointer += 1  # Move to the next song
#         else:
#             st.session_state.song_pointer = 0  # Loop back to the first song

#         st.experimental_rerun()  # Re-run the app to update the player


import streamlit as st
from db import create_event, get_songs, add_song_to_event, get_event_name, container  # Import functions from db.py
from link import search_youtube
import time


# Function to embed a YouTube video with autoplay
def embed_autoplay_youtube(video_url):
    # Extract the video ID from the URL (assuming a standard YouTube link)
    video_id = video_url.split("v=")[1]

    # Create the HTML code for embedding the video with autoplay
    video_html = f"""
        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/{video_id}?autoplay=1"
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """

    # Use Streamlit's HTML component to display the video
    st.components.v1.html(video_html, height=315)


# Set up initial states
if "event_id" not in st.session_state:
    st.session_state["event_id"] = None

if "event_name" not in st.session_state:
    st.session_state["event_name"] = None

if "songs" not in st.session_state:
    st.session_state["songs"] = []

if "song_pointer" not in st.session_state:
    st.session_state.song_pointer = 0  # Pointer to track which song is currently playing

if 'song_links' not in st.session_state:
    st.session_state['song_links'] = {}  # Dictionary to store songs and their YouTube links

if 'song_durations' not in st.session_state:
    st.session_state['song_durations'] = {}  # Dictionary to store song durations in seconds

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

        # Input for the hackathon theme instead of adding songs
        hackathon_theme = st.text_input("Enter the hackathon theme:")

        ## Fetch YouTube link and duration for each song
        for song in st.session_state["songs"]:
            if song not in st.session_state['song_links']:
                # Fetch the YouTube link and duration for the song if not already cached
                try:
                    link, duration = search_youtube(song)
                    st.session_state['song_links'][song] = link  # Cache the link in session state
                    st.session_state['song_durations'][song] = duration  # Cache the duration in session state
                except Exception as e:
                    st.error(f"Error fetching YouTube link for {song}: {str(e)}")
                    continue

        # Prepare the list of YouTube links for the player
        link_array = list(st.session_state['song_links'].values())
        duration_array = list(st.session_state['song_durations'].values())

        # Play the current song and set up auto-play for the next one
        current_song = link_array[st.session_state.song_pointer]
        current_duration = duration_array[st.session_state.song_pointer]

        st.write(f"Now playing: {st.session_state['songs'][st.session_state.song_pointer]}")
        embed_autoplay_youtube(current_song)

        # Automatically press 'Next' after the song duration ends
        time.sleep(current_duration)

        # Check if the pointer has reached the end, if yes, loop back to the first song
        if st.session_state.song_pointer < len(link_array) - 1:
            st.session_state.song_pointer += 1  # Move to the next song
        else:
            st.session_state.song_pointer = 0  # Loop back to the first song

        st.experimental_rerun()  # Re-run the app to update the player
