from .package import spotify
import sys

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

    tracks_features = spotify.get_tracks_features(tracks)
    genres = spotify.get_tracks_genres(tracks)

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

def search_track_by_features(query, features=[]):
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

    track_list = spotify.get_tracks(f'{query} {" ".join(features["genres"])}', amount=200)

    if len(track_list) == 0:
        return(None)
    else:
        return(most_similar_track(features, track_list)["external_urls"]["spotify"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python song_searcher.py <query>")
        search_track_by_features("a happy dog laying down")
    else:
        query = sys.argv[1]
        search_track_by_features(query)
