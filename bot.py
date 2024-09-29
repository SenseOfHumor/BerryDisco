import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from youtube import get_music_youtube_urls_from_list  # Import your YouTube function

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

    # Get the YouTube URLs for the recommended music
    youtube_urls_json = get_music_youtube_urls_from_list(music_list)

    # Return the result as a JSON string
    return youtube_urls_json
