import json
from .lyrics_search import get_lyrics_from_id, search_track_by_lyrics
from .image_describer import get_image_description
from .features_search import search_track_by_features
from .gpt import get_image_feats

from .package import spotify, track

TEST_FEATS = {
        "genres": ["hip-hop"],
        "acousticness": 0.2,
        "danceability": 0.5,
        "energy": 0.7,
        "instrumentalness": 0.1,
        "liveness": 0.3,
        "loudness": -10,
        "speechiness": 0.2,
        "tempo": 120,
        "valence": 0.6,
    }
TEST_CAPTION = "a big building in a city"
TEST_TAGS = ["sky", "outdoor", "city", "background", "harbor", "skyscraper"]


def search_track_literal(url=None, base64=None, amount=1, pool_size=5):
    result = get_image_description(url, base64)
    print(result)

    caption = result["captionResult"]["text"]
    tags = [tag["name"] for tag in result["tagsResult"]["values"]]

    query = " ".join(tags)[:64]

    track_list = spotify.get_tracks(query, amount=amount)
    matched_tracks=[track.Track(id = tr['id']) for tr in track_list]

    for tr in matched_tracks:
        lyrics = get_lyrics_from_id(tr.id)

        if lyrics is not None:
            tr.set_timestamp(lyrics)

    #matched_tracks = search_track_by_lyrics(query, amount, pool_size, True)
    return matched_tracks


def search_track_emotional(url=None, base64=None, amount=1):
    result = get_image_description(url, base64)
    print(result)
    feats = get_image_feats(json.dumps(result))
    print(feats)
    recoms = spotify.get_recommendations(feats, amount)
    found_track_ids = [recom["id"] for recom in recoms]

    found_tracks = []
    # gets the lyrics of each track
    for track_id in found_track_ids:
        tr = track.Track(id=track_id)
        lyrics = get_lyrics_from_id(tr.id)

        if lyrics is not None:
            tr.set_timestamp(lyrics)

        found_tracks.append(tr)

    return found_tracks


def search_track_both(url=None, base64=None, amount=1):
    result = get_image_description(url, base64)

    caption = result["captionResult"]["text"]
    tags = [tag["name"] for tag in result["tagsResult"]["values"]]
    query = " ".join(tags)[:64]

    print(result)
    feats = get_image_feats(json.dumps(result))
    print(feats)

    found_tracks = search_track_by_features(query, feats, amount, 200)

    # gets the lyrics of each track
    for tr in found_tracks:
        lyrics = get_lyrics_from_id(tr.id)

        if lyrics is not None:
            tr.set_timestamp(lyrics)

    return found_tracks
