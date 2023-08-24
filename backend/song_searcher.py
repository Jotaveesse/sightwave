import sys
import spotipy
from dotenv import load_dotenv

load_dotenv()

auth_manager = spotipy.oauth2.SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)


def get_tracks(query, amount=50):
    tracks = []
    searches_left = amount

    batch_size = 50

    # max of 50 tracks per request, so we make multiple requests if we need  more than 50
    while searches_left > 0:
        current_batch_size = min(batch_size, searches_left)
        results = spotify.search(q=f"{query}", type="track", limit=current_batch_size)

        tracks += results["tracks"]["items"]

        searches_left -= current_batch_size

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


def compare_features(features1, features2):
    total_diff = 0
    total_diff += abs(features1["acousticness"] - features2["acousticness"])
    total_diff += abs(features1["danceability"] - features2["danceability"])
    total_diff += abs(features1["energy"] - features2["energy"])
    total_diff += abs(features1["instrumentalness"] - features2["instrumentalness"])
    total_diff += abs(features1["liveness"] - features2["liveness"])
    total_diff += abs(features1["loudness"] - features2["loudness"]) / 60   # range is from -60 to 0
    total_diff += abs(features1["speechiness"] - features2["speechiness"])
    total_diff += abs(features1["tempo"] - features2["tempo"]) / 120            # range is from 60-180
    total_diff += abs(features1["valence"] - features2["valence"]) * 3         # extra weight for valence

    # using jaccard similarity to compare genres
    intersection = len(set(features1['genres']).intersection(set(features2['genres'])))
    union = len(set(features1['genres']).union(set(features2['genres'])))
    genre_diff = 1- intersection / union

    total_diff += genre_diff

    return total_diff


def most_similar_track(main_features, tracks):
    if "genres" not in main_features:
        tracks.append(main_features)

    tracks_features = get_tracks_features(tracks)
    genres = get_tracks_genres(tracks)

    for i, feature in enumerate(tracks_features):
        feature.update(genres[i])

    if "genres" not in main_features:
        main_features = tracks_features.pop()
        tracks.pop()
        genres.pop()

    most_similar = None
    lowest_diff = float("inf")

    for i, features in enumerate(tracks_features):
        diff = compare_features(main_features, features)
        if diff < lowest_diff:
            lowest_diff = diff
            most_similar = tracks[i]
        
    print(lowest_diff)
    return most_similar


def search_song(query, features=[]):
    features = {
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

    track_list = get_tracks(f'{query} {" ".join(features["genres"])}', amount=200)

    if len(track_list) == 0:
        print("no songs found for that query")
    else:
        print(most_similar_track(features, track_list)["external_urls"]["spotify"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python song_searcher.py <query>")
        search_song("smiling dog laying down")
    else:
        query = sys.argv[1]
        search_song(query)
