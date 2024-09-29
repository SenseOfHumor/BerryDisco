import streamlit as st

def player(video_url):
    """
    This function takes a YouTube video URL and plays it using Streamlit's video player.
    
    Parameters:
        video_url (str): The URL of the YouTube video to play.
    """
    
    if video_url:
        st.video(video_url)
    else:
        st.warning("No video URL found to play.")
