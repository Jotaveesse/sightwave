from . import requester as req
import os
import spotipy
from dotenv import load_dotenv
load_dotenv()

CACHE_LOCATION =  os.environ["CACHE_LOCATION"]

auth_manager = spotipy.oauth2.SpotifyClientCredentials(
    cache_handler=spotipy.CacheFileHandler(cache_path=CACHE_LOCATION)
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

def get_recommendations(features, limit=3):
    
    results = spotify.recommendations(
        seed_genres=features['genres'],
        limit=limit,
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

def get_tracks(query, amount=50):
    tracks = []
    searches_done = 0

    batch_size = 50

    # max of 50 tracks per request, so we make multiple requests if we need  more than 50
    while searches_done < amount:
        current_batch_size = min(batch_size, amount-searches_done)
        results = spotify.search(q=f"{query}", type="track", limit=current_batch_size, offset=searches_done)

        tracks += results["tracks"]["items"]

        searches_done += current_batch_size

    return tracks


def get_tracks_features(tracks):
    all_features = []

    batch_size = 100
    num_batches = (len(tracks) + batch_size - 1) // batch_size

    # max of 100 tracks per request, so we make multiple requests if we need  more than 100
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        batch_tracks = tracks[start_idx:end_idx]

        # if it's a list of track objects
        if isinstance(batch_tracks[0], dict):
            track_ids = [track["id"] for track in batch_tracks]
            batch_results = spotify.audio_features(track_ids)
        # if it's a list of ids
        elif isinstance(batch_tracks[0], str):
            batch_results = spotify.audio_features(batch_tracks)

        all_features.extend(batch_results)

    return all_features


def get_tracks_genres(tracks):
    all_genres = []

    batch_size = 50
    num_batches = (len(tracks) + batch_size - 1) // batch_size

    # max of 50 tracks per request, so we make multiple requests if we need  more than 50
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        batch_tracks = tracks[start_idx:end_idx]

        # genres can only be found in the artists' data
        artists = [track["artists"][0]["id"] for track in batch_tracks]
        results = spotify.artists(artists)
        genres = [{"genres": artist["genres"]} for artist in results["artists"]]

        all_genres.extend(genres)

    return all_genres

def get_track_id(title, artist):
    query = f"track:{req.clean_query(title)} artist:{req.clean_query(artist)}"
    results = spotify.search(q=query, type='track', limit='1')
    return results["tracks"]["items"][0]["id"]