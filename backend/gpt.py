import json
import os
import openai
from .package import genres
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ["OPENAI_KEY"]
system_message=f'''I will give you some parameters and descriptions of an image and you have to return what values fit the image the most, keep in mind some captions can be wrong, especially if they have a low confidence and contradict other captions and tags. These are the attributes you have to evaluate:
    acousticness: 0 to 1
    danceability: 0 to 1
    energy: 0 to 1
    instrumentalness: 0 to 1
    liveness: 0 to 1
    loudness: -60 to 0
    speechiness: 0 to 1
    tempo: 60 to 180
    valence: 0 to 1
    genres: up to 5 genres from the list and only from this list, do not use other genres: 
    {str(genres.SIMPLE_GENRES)}
    do not put other genres in the response, only use those i specified
    respond only in this json format, no extra text, just the json:
    {{
        "genres": ["musicalgenre", "musicalgenre", "musicalgenre", "musicalgenre", "musicalgenre"],
        "acousticness": value,
        "danceability": value,
        "energy": value,
        "instrumentalness": value,
        "liveness": value,
        "loudness": value,
        "speechiness": value,
        "tempo": value,
        "valence": value
    }}'''

def get_image_feats(description):
    messages = [ {"role": "system", "content": 
                system_message} ]
    messages.append(
                {"role": "user", "content": description},
            )

    chat = openai.ChatCompletion.create(
                model="gpt-4", messages=messages)
    reply = chat.choices[0].message.content
    json_reply = json.loads(reply)

    json_reply['genres']  = [genre for genre in json_reply['genres'] if genre in genres.SIMPLE_GENRES]

    if len(json_reply['genres']) == 0:
        json_reply['genres']=['soundtracks']

    return json_reply