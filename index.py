from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from lyrics_searcher import get_matching_tracks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with your allowed origins
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def test():
    return 'foi'

@app.get('/api')
def main(url: Optional[str] = None, search_prompt: Optional[str] = None):
    description = "a big building in a city"
    tags = ['sky', 'outdoor', 'city', 'background', 'harbor', 'skyscraper']

    matched_track_by_desc = None

    # ===========================================================================
    # SÓ DESCOMENTE SE REALMENTE PRECISAR PRA NAO GASTAR OS CREDITOS DA API
    # ===========================================================================
    #if (url != None):
    #   (description, tags) = image_describer.get_image_description(url)
    #   matched_track_by_desc = get_matching_tracks(description, 4, False)
    #   matched_track_by_tags = get_matching_tracks(" ".join(tags), 4, False)
    #   matched_track_by_both = get_matching_tracks(f"{description} {' '.join(tags)})", 4, False)

    if search_prompt:
        try:
            matched_track_by_desc = get_matching_tracks(search_prompt, 1, False)
        except Exception as e:
            return {'error': str(e)}

    else:
        matched_track_by_desc = get_matching_tracks(description, 4, False)
        # matched_track_by_tags = get_matching_tracks(" ".join(tags), 4, False)
        # matched_track_by_both = get_matching_tracks(f"{description} {' '.join(tags)})", 4, False)

    message = f"Image: {url} Text: {search_prompt}"

    data = {
        'message': message,
        'matched_track_by_desc': matched_track_by_desc,
        # 'matched_track_by_tags': matched_track_by_tags,
        # 'matched_track_by_both': matched_track_by_both
    }
    return data
