import streamlit as st

import streamlit as st
from streamlit_calendar import calendar
from openai import OpenAI
from ics import Calendar, Event
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import pytz

from googleapiclient.discovery import build

from youtube import get_music_youtube_urls_from_list




# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPEN_AI_API")

# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

# AI-Powered Scheduling
theme_input = st.text_area("Enter the theme of the party and I will suggest music based on the theme.")

if st.button("GROOVE"):
    current_date = datetime.now().strftime("%Y-%m-%d")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps to find good and new music based on the hackathon theme."},
            {
                "role": "user",
                "content": f"""
                This is the hackathon theme: {theme_input}

                Consider the following:
                - If the user enteres the theme of the party, the assistant should suggest 10 music based on the theme.
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

    response_text = response.choices[0].message.content.strip()

    try:
        music_list = json.loads(response_text)
    except json.JSONDecodeError:
        st.error("Failed to decode response as JSON. Here is the raw output:")
        st.text(response_text)
        st.stop()
        
    # st.write(music_list)


    # Get the YouTube URLs for the music
    youtube_urls_json = get_music_youtube_urls_from_list(music_list)
    st.write(youtube_urls_json)


