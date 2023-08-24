import requests
import json
import os
from lyrics_searcher import make_get_request, get_access_token
from dotenv import load_dotenv

load_dotenv("keys.env")

SPOTIFY_RECOM_URL = os.getenv("SPOTIFY_RECOM_URL")

access_token = None

def get_recommendations(
    genres,
    acousticness,
    danceability,
    energy,
    instrumentalness,
    liveness,
    loudness,
    speechiness,
    tempo,
    valence,
):
    global access_token

    spotify_search_params = {
        "limit": 3,
        "seed_genres": genres,
        "target_acousticness": acousticness,
        "target_danceability": danceability,
        "target_energy": energy,
        "target_instrumentalness": instrumentalness,
        "target_liveness": liveness,
        "target_loudness": loudness,
        "target_speechiness": speechiness,
        "target_tempo": tempo,
        "target_valence": valence,
    }

    spotify_headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(
            SPOTIFY_RECOM_URL, params=spotify_search_params, headers=spotify_headers
        )

        if response.status_code == 200:
            track_data = json.loads(response.text)

            return track_data["tracks"]["items"][0]["id"]

        # 401 means token is invalid
        elif response.status_code == 401:
            print(f"Getting a new access token")

            access_token = get_access_token()

            spotify_headers = {"Authorization": f"Bearer {access_token}"}

            response_data = make_get_request(
                SPOTIFY_RECOM_URL, spotify_search_params, spotify_headers
            )
            track_data = json.loads(response_data)

            return track_data["tracks"]

        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"General error while trying to fetch id for ")
        return None


if __name__ == "__main__":
    # source = https://www.doglife.com.br/site/assets/images/cao.png
    '''
    tracks = get_recommendations(
        genres=["acoustic", "chill", "indie", "pop", "folk"],
        acousticness=0.15,
        danceability=0.25,
        energy=0.6,
        instrumentalness=0.5,
        liveness=0.2,
        loudness=-25,
        speechiness=0.1,
        tempo=100,
        valence=0.8,
    )
    '''
    # source = https://t3.ftcdn.net/jpg/05/61/99/50/360_F_561995097_a0dHcJrC2lCdOj6CBp6xBeGYv0hCsMyM.jpg
    """
    tracks = get_recommendations(
        genres=['ambient', 'classical', 'instrumental', 'piano', 'soundtracks'],
        acousticness=0.4,  # Reflecting the rain and quiet surroundings
        danceability=0.3,  # Matching the determined stride
        energy=0.5,  # Conveying the sense of purpose
        instrumentalness=0.7,  # Reflecting the absence of human voices
        liveness=0.1,  # Capturing the stillness of the scene
        loudness=-40,  # Representing the quietness of rain and solitude
        speechiness=0.2,  # Indicating some minimal presence of speech
        tempo=70,  # Corresponding to a deliberate walking pace
        valence=0.3  # Reflecting the mix of determination and introspection
    )
    """

    # source = https://media.istockphoto.com/id/1138722351/pt/foto/new-york-city-traffic.jpg?s=612x612&w=0&k=20&c=kndH14Zqf7iOIzE8ZFbpNz1ZkQOGmqS7YZ_FZXg8Eio=
    tracks = get_recommendations(
        genres=['pop', 'electronic', 'dance', 'hip-hop', 'indie'],
        acousticness=0.1,  # Reflecting the urban environment's noise level
        danceability=0.7,  # Matching the lively and bustling scene
        energy=0.8,  # Conveying the high activity and movement
        instrumentalness=0.2,  # Reflecting the presence of various sounds
        liveness=0.9,  # Capturing the sense of a live and dynamic environment
        loudness=-20,  # Representing the urban cacophony
        speechiness=0.5,  # Indicating the presence of voices and sounds
        tempo=120,  # Corresponding to the brisk pace of city life
        valence=0.6  # Reflecting the mix of busyness and vibrancy
    )
    
    for track in tracks:
        print(f'https://open.spotify.com/track/{track["id"]}')