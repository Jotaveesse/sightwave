from .package import requester, spotify, track
from dotenv import load_dotenv
import json
import re
import os

MUSIX_API_KEY = os.environ["MUSIX_API_KEY"]
TRACK_SEARCH_URL = os.environ["TRACK_SEARCH_URL"]
LYRICS_FETCH_URL = os.environ["LYRICS_FETCH_URL"]

def get_tracks_from_lyrics(query, track_amount=5, with_timestamp=True):
    search_params = {
        "apikey": MUSIX_API_KEY,
        "q_lyrics": query,
        "page_size": track_amount,
        "page": "1",
        "quorum_factor": "0.5",  # controls how fuzzy the search is, lower is stricter
        "s_track_rating": "desc",
        "f_has_richsync": 1 if with_timestamp else 0
        # "q_artist": "joy parade"
    }

    try:
        response_data = requester.make_get_request(TRACK_SEARCH_URL, search_params)
        tracks = json.loads(response_data)["message"]["body"]["track_list"]

        # list of tuples of (tile, artist)
        tracks_data = [
            (track["track"]["track_name"], track["track"]["artist_name"])
            for track in tracks
        ]

        return tracks_data
    except Exception as e:
        print(e)
        return (None, None)


def get_lyrics_from_id(id):
    try:
        response_data = requester.make_get_request(LYRICS_FETCH_URL, {"trackid": id})
        lyrics_data = json.loads(response_data)

        return lyrics_data["lines"]
    except Exception as e:
        print(e)
        return None


def search_track_by_lyrics(query, amount=1, pool_size=5, with_timestamp=False):
    # removes special characters
    cleaned_query = re.sub(r"[^\w\s]", " ", query)

    tracks_found = get_tracks_from_lyrics(cleaned_query, pool_size, with_timestamp)

    if len(tracks_found) == 0:
        return None

    valid_tracks = []
    # creates a new Track object for each track found
    for tr in tracks_found:
        tr = track.Track(cleaned_query, title=tr[0], artist=tr[1])

        id = spotify.get_track_id(tr.title, tr.artist)
        # only saves Track if it can find its id
        if id != None:
            tr.id = id
            valid_tracks.append(tr)

    if len(valid_tracks) == 0:
        return None

    tracks_with_timestamps = []
    for tr in valid_tracks:
        timestamp = get_lyrics_from_id(tr.id)

        # only saves Track if it can find its timestamped lyrics
        if timestamp != None:
            tr.set_timestamp(timestamp)
            tracks_with_timestamps.append(tr)

    if len(tracks_with_timestamps) == 0:
        return None

    # sorts tracks by similarity
    sorted_tracks = sorted(tracks_with_timestamps, key=lambda lyric: lyric.similarity, reverse = True)
    # returns only the tracsk which match the query the most
    most_similar = sorted_tracks[:amount]

    return most_similar