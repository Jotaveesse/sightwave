import requests
import json
import sys
import re
import os
import spotipy
from .track import Track
from dotenv import load_dotenv

load_dotenv()

CACHE_LOCATION =  os.getenv("CACHE_LOCATION")

auth_manager = spotipy.oauth2.SpotifyClientCredentials(
    cache_handler=spotipy.CacheFileHandler(cache_path=CACHE_LOCATION)
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

MUSIX_API_KEY = os.getenv("MUSIX_API_KEY")
TRACK_SEARCH_URL =  os.getenv("TRACK_SEARCH_URL")
LYRICS_FETCH_URL = os.getenv("LYRICS_FETCH_URL")

def make_get_request(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Get request failed with status code: {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def clean_query(query):
    index = query.find("feat")
    if index != -1:
        query = query[:index]
    
    query = query[:64] # limits the string to a max of 64 characters
    query = re.sub(r'[^\w\s]', ' ', query) # removes special characters
    return query

def get_tracks_from_lyrics(query, track_amount = 5, with_timestamp = True):
    search_params = {
        "apikey": MUSIX_API_KEY,
        "q_lyrics": query,
        "page_size": track_amount,
        "page": "1",
        "quorum_factor": "0.5", # controls how fuzzy the search is, lower is stricter
        "s_track_rating": "desc",
        "f_has_richsync": 1 if with_timestamp else 0
        #"q_artist": "joy parade"
    }

    try:
        response_data = make_get_request(TRACK_SEARCH_URL, search_params)
        tracks = json.loads(response_data)['message']['body']['track_list']

        # list of tuples of (tile, artist)
        tracks_data = [(track['track']['track_name'], track['track']['artist_name']) for track in tracks]

        return tracks_data
    except Exception as e:
        print(e)
        return (None, None)

def get_track_id(title, artist):
    results = spotify.search(q=f"track:{clean_query(title)} artist:{clean_query(artist)}", type='track', limit='1')
    return results["tracks"]["items"][0]["id"]
    
def get_lyrics_from_id(id):
    lyrics_params = {
        "trackid": id
    }
    
    try:
        response_data = make_get_request(LYRICS_FETCH_URL, lyrics_params)
        lyrics_data = json.loads(response_data)

        return lyrics_data['lines']
    except Exception as e:
        print(e)
        return None

def get_matching_tracks(query, search_amount = 5 , with_timestamp=True):
    # removes special characters
    cleaned_query = re.sub(r'[^\w\s]', ' ', query)

    tracks_found = get_tracks_from_lyrics(cleaned_query, search_amount, with_timestamp)

    if len(tracks_found) == 0:
        return None    

    lyrics_with_ids = []
    # creates a new Track object for each track found
    for track in tracks_found:
        lyric = Track(cleaned_query, title=track[0], artist=track[1])
        
        id = get_track_id(lyric.title, lyric.artist)
        # only saves Track if it can find its id
        if id != None:
            lyric.id = id
            lyrics_with_ids.append(lyric)

        #print(f'Track: {track[0]}')

    if len(lyrics_with_ids) == 0:
        return None
    
    lyrics_with_timestamps = []
    for lyric in lyrics_with_ids:
        timestamp = get_lyrics_from_id(lyric.id)

        # only saves Track if it can find its timestamped lyrics
        if timestamp != None:
            lyric.set_timestamp(timestamp)
            lyrics_with_timestamps.append(lyric)

    if len(lyrics_with_timestamps) == 0:
        return None
    
    # returns only the track which matches the query the most
    most_similar = max(lyrics_with_timestamps, key=lambda lyric: lyric.similarity)
    return most_similar

def main(query):
    matched_track = get_matching_tracks(query, 5, False)
    print(matched_track)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lyrics_searcher.py <query>")
        main("a fan sitting on a desk")
    else:
        query = sys.argv[1]
        main(query)
