import streamlit as st


def player(video_urls):
    # List of YouTube video URLs
    # video_urls = [
    #     "https://www.youtube.com/watch?v=3AtDnEC4zak",  # Ed Sheeran - Shape of You
    #     "https://www.youtube.com/watch?v=p-BnzNKPSYc",  # Avicii - Wake Me Up
    #     "https://www.youtube.com/watch?v=h5EofwRzit0"   # Daft Punk - Get Lucky
    # ]

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
            if st.session_state.video_index < len(video_urls) - 1:
                st.session_state.video_index += 1

    # Get the updated current video index
    current_index = st.session_state.video_index

    # Display the current video
    st.video(video_urls[current_index])


# music_array = ["https://www.youtube.com/watch?v=3AtDnEC4zak",
#                "https://www.youtube.com/watch?v=p-BnzNKPSYc",
#                "https://www.youtube.com/watch?v=h5EofwRzit0",
#                "https://www.youtube.com/watch?v=62i7zHtmsTA"]
# player (music_array)
