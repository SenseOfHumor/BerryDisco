import streamlit as st

from player import player

# ## calling the music function from player.py
# music_array = ["https://www.youtube.com/watch?v=3AtDnEC4zak",
#                "https://www.youtube.com/watch?v=p-BnzNKPSYc",
#                "https://www.youtube.com/watch?v=h5EofwRzit0",
#                "https://www.youtube.com/watch?v=62i7zHtmsTA"]
# player (music_array)


#######################################################################
## EVERYTHING RELATED TO THE SIDEBAR GOES HERE ##
#######################################################################

st.sidebar.title("THE PLAYLIST  🎶")



#######################################################################
## EVERYTHING RELATED TO THE MAIN PAGE GOES HERE ##
#######################################################################
st.title("BERRY DISCO 🍇🕺🏽")
st.info("Welcome to Berry (Very) Disco! 🍇🕺🏽")

st.subheader("Create your own disco")
if st.button("Create Disco!"):
    st.success("Disco created! 🎉")
    st.info("You are now the DJ! 🎧🎶")

st.subheader("OR, Enter your 6-digit code to join the Disco!")
if st.text_input("Code:"):
    st.toast("Code accepted! 🎉")
    st.info("You are now in the Disco! 🍇🕺🏽")

    

