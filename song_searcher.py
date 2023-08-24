import sys
import spotipy
from dotenv import load_dotenv

load_dotenv()

auth_manager = spotipy.oauth2.SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)

def get_tracks(query):
    results = spotify.search(q=f'{query}', type='track', limit= 2)
    tracks = results['tracks']['items']
    
    return tracks

def get_tracks_features(tracks):
    #if its a list of track objects
    if isinstance(tracks[0], dict):
        track_ids = [track['id'] for track in tracks]
        results = spotify.audio_features(track_ids)
    #if its a list of ids
    elif isinstance(tracks[0], str):
        results = spotify.audio_features(tracks)
    
    return results

def get_tracks_genres(tracks):
    artists = [track['artists'][0]['id'] for track in tracks]
    results = spotify.artists(artists)
    genres = [{'genres':artist['genres']} for artist in results['artists']]

    return genres

def compare_features(features1, features2):
    total_diff = 0
    total_diff += abs(features1['acousticness'] - features2['acousticness'])
    total_diff += abs(features1['danceability'] - features2['danceability'])
    total_diff += abs(features1['energy'] - features2['energy'])
    total_diff += abs(features1['instrumentalness'] - features2['instrumentalness'])
    total_diff += abs(features1['liveness'] - features2['liveness'])
    total_diff += abs(features1['loudness'] - features2['loudness'])/60
    total_diff += abs(features1['speechiness'] - features2['speechiness'])
    total_diff += abs(features1['tempo'] - features2['tempo'])/120
    total_diff += abs(features1['valence'] - features2['valence'])

    short_features=[]
    long_features=[]

    if len(features1['genres'])<len(features2['genres']):
        short_features = features1
        long_features = features2
    else:
        short_features = features2
        long_features = features1
    
    for genre in short_features['genres']:
        if genre not in long_features['genres']:
            total_diff += 0.2
    
    return total_diff

def most_similar_track(main_features, tracks):
    if 'genres' not in main_features:
        tracks.append(main_features)
    
    tracks_features = get_tracks_features(tracks)
    genres = get_tracks_genres(tracks)

    for i, feature in enumerate(tracks_features):
        feature.update(genres[i])
    
    if 'genres' not in main_features:
        main_features = tracks_features.pop()
        tracks.pop()
        genres.pop()

    most_similar = None
    lowest_diff = float('inf')

    for i, features in enumerate(tracks_features):
        diff = compare_features(main_features, features)
        if diff < lowest_diff:
            lowest_diff = diff
            most_similar = tracks[i]
    
    print(lowest_diff)
    return most_similar

def search_song(query, features=[]):
    features = {'genres':['ambient', 'classical', 'instrumental', 'piano', 'soundtracks'],
                'acousticness':0.4,
                'danceability':0.3,
                'energy':0.5,
                'instrumentalness':0.7,
                'liveness':0.1,
                'loudness':-40,
                'speechiness':0.2,
                'tempo':70,
                'valence':0.3
                }

    track_list = get_tracks(query)

    if len(track_list) == 0:
        print('no songs found for that query')
    else:
        print(most_similar_track(features, track_list)['external_urls']['spotify'])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python song_searcher.py <query>")
        search_song("a fan sitting on a desk")
    else:
        query = sys.argv[1]
        search_song(query)
