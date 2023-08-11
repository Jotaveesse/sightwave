from fastapi import FastAPI, Request
from typing import List, Optional
from lyrics_searcher import get_matching_tracks
from image_describer import get_image_description

from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/')
def test():
    return FileResponse("test.html")

@app.get('/api')
def main(url: Optional[str] = None, search_prompt: Optional[str] = None,  pool: Optional[int] = 3):
    description = "a big building in a city"
    tags = ['sky', 'outdoor', 'city', 'background', 'harbor', 'skyscraper']

    matched_track_by_desc = None
    matched_track_by_tags = None
    matched_track_by_both = None

    # ===========================================================================
    # SÓ DESCOMENTE SE REALMENTE PRECISAR PRA NAO GASTAR OS CREDITOS DA API
    # ===========================================================================
    if url:
        (description, tags) = get_image_description(url)
        matched_track_by_desc = get_matching_tracks(description, pool, False)
        matched_track_by_tags = get_matching_tracks(" ".join(tags), pool, False)
        matched_track_by_both = get_matching_tracks(f"{description} {' '.join(tags)})", pool, False)

    if search_prompt:
        try:
            matched_track_by_desc = get_matching_tracks(search_prompt, pool, False)
        except Exception as e:
            return {'error': str(e)}

    else:
        matched_track_by_desc = get_matching_tracks(description, pool, False)
        matched_track_by_tags = get_matching_tracks(" ".join(tags), pool, False)
        matched_track_by_both = get_matching_tracks(f"{description} {' '.join(tags)})", pool, False)

    #message = f"Image: {url} Text: {search_prompt}"

    tracks = [matched_track_by_desc, matched_track_by_tags, matched_track_by_both]
    data = {
        'tracks': tracks
        # 'matched_track_by_tags': matched_track_by_tags,
        # 'matched_track_by_both': matched_track_by_both
    }
    return data
