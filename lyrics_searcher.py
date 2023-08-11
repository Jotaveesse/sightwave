import requests
import json
import sys
import re
from track import Track

TRACK_SEARCH_URL = "http://api.musixmatch.com/ws/1.1/track.search"
SPOTIFY_REQUEST_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
LYRICS_FETCH_URL = "https://spotify-lyric-api.herokuapp.com/"

keys = None
access_token = None

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

def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": keys['spotify_client_id'],
        "client_secret": keys['spotify_client_secret']
    }

    try:
        response = requests.post(SPOTIFY_REQUEST_URL, data=data)

        if response.status_code == 200:
            response_data = response.json()
            return response_data["access_token"]
        else:
            print(f"Post request failed with status code: {response.status_code}")
            return None

    except Exception as e:
        print(e)
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
        "apikey": keys['musix_api_key'],
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
    global access_token

    spotify_search_params = {
        "q":f"track:{clean_query(title)} artist:{clean_query(artist)}",
        "type":"track",
        "limit":1
    }
    
    spotify_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(SPOTIFY_SEARCH_URL, params=spotify_search_params, headers=spotify_headers)

        if response.status_code == 200:
            track_data = json.loads(response.text)

            return track_data["tracks"]["items"][0]["id"]
        
        # 401 means token is invalid
        elif response.status_code == 401:
            print(f"Getting a new access token")

            access_token = get_access_token()

            spotify_headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            response_data = make_get_request(SPOTIFY_SEARCH_URL, spotify_search_params, spotify_headers)
            track_data = json.loads(response_data)

            return track_data["tracks"]["items"][0]["id"]
        
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"General error while trying to fetch id for '{title}' by '{artist}': {e}")
        return None
    
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
    global keys
    with open('keys.json') as file:
        keys = json.load(file)

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
