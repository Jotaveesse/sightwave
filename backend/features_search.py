from .package import spotify
from .package import track
import sys


def compare_features(features1, features2):
    total_diff = 0
    total_diff += abs(features1["acousticness"] - features2["acousticness"])
    total_diff += abs(features1["danceability"] - features2["danceability"])
    total_diff += abs(features1["energy"] - features2["energy"])
    total_diff += abs(features1["instrumentalness"] - features2["instrumentalness"])
    total_diff += abs(features1["liveness"] - features2["liveness"])
    total_diff += (
        abs(features1["loudness"] - features2["loudness"]) / 60
    )  # range is from -60 to 0
    total_diff += abs(features1["speechiness"] - features2["speechiness"])
    total_diff += (
        abs(features1["tempo"] - features2["tempo"]) / 120
    )  # range is from 60-180
    total_diff += (
        abs(features1["valence"] - features2["valence"]) * 4
    )  # extra weight for valence

    # using jaccard similarity to compare genres
    intersection = len(set(features1["genres"]).intersection(set(features2["genres"])))
    union = len(set(features1["genres"]).union(set(features2["genres"])))
    genre_diff = 1 - intersection / union

    total_diff += genre_diff

    return total_diff


def most_similar_tracks(main_features, tracks, amount=1):
    if "genres" not in main_features:
        tracks.append(main_features)

    tracks_features = spotify.get_tracks_features(tracks)
    genres = spotify.get_tracks_genres(tracks)

    for i, feature in enumerate(tracks_features):
        if feature:
            feature.update(genres[i])

    if "genres" not in main_features:
        main_features = tracks_features.pop()
        tracks.pop()
        genres.pop()

    features_tuple = list(zip(tracks, tracks_features))

    filtered_tracks = [(tr, feat) for tr, feat in features_tuple if feat is not None]

    sorted_tracks = sorted(
        filtered_tracks, key=lambda tup: compare_features(main_features, tup[1]), reverse=True
    )

    best_tracks = [tu[0] for tu in sorted_tracks][:amount]

    return best_tracks


def search_track_by_features(query, features=[], amount=1, pool=100):
    track_list = spotify.get_tracks(query, amount=pool)

    if len(track_list) == 0:
        return None
    else:
        tracks = most_similar_tracks(features, track_list, amount)
        found_tracks = []
        for tr in tracks:
            found_tracks.append(track.Track(id=tr["id"]))
        return found_tracks
