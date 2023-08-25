import os
import spotipy
from dotenv import load_dotenv

load_dotenv()

CACHE_LOCATION =  os.getenv("CACHE_LOCATION")

auth_manager = spotipy.oauth2.SpotifyClientCredentials(
    cache_handler=spotipy.CacheFileHandler(cache_path=CACHE_LOCATION)
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

def get_recommendations(features):
    
    results = spotify.recommendations(
        seed_genres=features['genres'],
        limit=3,
        target_acousticness=features['acousticness'],
        target_danceability=features['danceability'],
        target_energy=features['energy'],
        target_instrumentalness=features['instrumentalness'],
        target_liveness=features['liveness'],
        target_loudness=features['loudness'],
        target_speechiness=features['speechiness'],
        target_tempo=features['tempo'],
        target_valence=features['valence']
    )

    return results['tracks']

if __name__ == "__main__":
    # source = https://www.doglife.com.br/site/assets/images/cao.png
    """
    feats = {
        'genres':["acoustic", "chill", "indie", "pop", "folk"],
        'acousticness':0.15,
        'danceability':0.25,
        'energy':0.6,
        'instrumentalness':0.5,
        'liveness':0.2,
        'loudness':-25,
        'speechiness':0.1,
        'tempo':100,
        'valence':0.8,
    }
    """
    # source = https://t3.ftcdn.net/jpg/05/61/99/50/360_F_561995097_a0dHcJrC2lCdOj6CBp6xBeGYv0hCsMyM.jpg
    """
    feats = {
        'genres':['ambient', 'classical', 'instrumental', 'piano', 'soundtracks'],
        'acousticness':0.4,  # Reflecting the rain and quiet surroundings
        'danceability':0.3,  # Matching the determined stride
        'energy':0.5,  # Conveying the sense of purpose
        'instrumentalness':0.7,  # Reflecting the absence of human voices
        'liveness':0.1,  # Capturing the stillness of the scene
        'loudness':-40,  # Representing the quietness of rain and solitude
        'speechiness':0.2,  # Indicating some minimal presence of speech
        'tempo':70,  # Corresponding to a deliberate walking pace
        'valence':0.3  # Reflecting the mix of determination and introspection
    }
    """

    # source = https://media.istockphoto.com/id/1138722351/pt/foto/new-york-city-traffic.jpg?s=612x612&w=0&k=20&c=kndH14Zqf7iOIzE8ZFbpNz1ZkQOGmqS7YZ_FZXg8Eio=
    feats = {
        'genres':["pop", "electronic", "dance", "hip-hop", "indie"],
        'acousticness':0.1,  # Reflecting the urban environment's noise level
        'danceability':0.7,  # Matching the lively and bustling scene
        'energy':0.8,  # Conveying the high activity and movement
        'instrumentalness':0.2,  # Reflecting the presence of various sounds
        'liveness':0.9,  # Capturing the sense of a live and dynamic environment
        'loudness':-20,  # Representing the urban cacophony
        'speechiness':0.5,  # Indicating the presence of voices and sounds
        'tempo':120,  # Corresponding to the brisk pace of city life
        'valence':0.6,  # Reflecting the mix of busyness and vibrancy
    }

    tracks = get_recommendations(feats)

    for track in tracks:
        print(f'https://open.spotify.com/track/{track["id"]}')
