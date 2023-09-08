import json
from  .lyrics_search import search_track_by_lyrics
from  .image_describer import get_image_description
from .features_search import search_track_by_features
from .gpt import get_image_feats

from .package import spotify, track

def search_track_literal(url=None, base64=None, pool=5):
    caption = "a big building in a city"
    tags = ['sky', 'outdoor', 'city', 'background', 'harbor', 'skyscraper']

    result = get_image_description(url, base64)

    caption = result['captionResult']['text']
    tags= [tag['name'] for tag in result['tagsResult']['values']]

    query =' '.join(tags)
    print(query)
    matched_track = search_track_by_lyrics(query, pool, False)

    return matched_track

def search_track_emotional(url=None, base64=None):
    feats = {'genres': ['afrobeat'], 'acousticness': 0.2, 'danceability': 0.5, 'energy': 0.7, 'instrumentalness': 0.1, 'liveness': 0.3, 'loudness': -10, 'speechiness': 0.2, 'tempo': 120, 'valence': 0.6}
    result = get_image_description(url, base64)
    print(result)
    feats = get_image_feats(json.dumps(result))
    print(feats)
    track_id = spotify.get_recommendations(feats, 1)[0]['id']
    found_track = track.Track(id=track_id)

    return found_track

def search_track_both(url=None, base64=None):
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

    result = get_image_description(url, base64)

    caption = result['captionResult']['text']
    tags= [tag['name'] for tag in result['tagsResult']['values']]
    query =' '.join(tags)

    print(result)
    feats = get_image_feats(json.dumps(result))
    print(feats)

    found_track = search_track_by_features(query ,feats, 150)

    return found_track