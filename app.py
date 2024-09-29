import streamlit as st

from player import player
from bot import get_music_recommendations

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
    st.session_state.music_recommendation = get_music_recommendations(theme_input)  # Store the result in session state

# Display the music recommendations in the sidebar
if st.session_state.music_recommendation:
    st.sidebar.write(st.session_state.music_recommendation)


#######################################################################
## EVERYTHING RELATED TO THE MAIN PAGE GOES HERE ##
#######################################################################

# Title for the main page
st.title("BERRY DISCO 🍇🕺🏽")
st.info("Welcome to Berry (Very) Disco! 🍇🕺🏽")

# Main page: Create your own disco
st.subheader("Create your own disco")
if st.button("Create Disco!"):
    st.success("Disco created! 🎉")
    st.info("You are now the DJ! 🎧🎶")

# Main page: Enter a code to join a disco
st.subheader("OR, Enter your 6-digit code to join the Disco!")
code_input = st.text_input("Code:")
if code_input:
    st.toast("Code accepted! 🎉")
    st.info("You are now in the Disco! 🍇🕺🏽")
