import streamlit as st

def player(songs):
    # Initialize session state to keep track of the current video index
    if 'video_index' not in st.session_state:
        st.session_state.video_index = 0

    # Handle button clicks before rendering the video
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            if st.session_state.video_index > 0:
                st.session_state.video_index -= 1

    with col2:
        if st.button("Next"):
            if st.session_state.video_index < len(songs) - 1:
                st.session_state.video_index += 1

    # Get the updated current video index
    current_index = st.session_state.video_index

    # Display the current song name
    st.write(f"Now playing: {songs[current_index]}")

    # Assuming the song names are valid YouTube URLs
    st.video(songs[current_index])


# Example usage (when you get the songs list from your Cosmos DB)
# music_array = ["https://www.youtube.com/watch?v=3AtDnEC4zak",
#                "https://www.youtube.com/watch?v=p-BnzNKPSYc",
#                "https://www.youtube.com/watch?v=h5EofwRzit0",
#                "https://www.youtube.com/watch?v=62i7zHtmsTA"]

# player(music_array)
