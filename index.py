import os
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
from backend.lyrics_searcher import get_matching_tracks
from backend.image_describer import get_image_description
from backend.song_searcher import search_song

app = fastapi.FastAPI()

print('loaded correctly')
# makes all files in the dir frontend available on the /static/ path
#static_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/frontend")
print('got path correctly')

#app.mount("/static", StaticFiles(directory="frontend"), name="static")
print('mounted correctly')

@app.get('/')
def index():
    return FileResponse("frontend/index.html")

@app.get('/api')
def api(url: Optional[str] = None, search_prompt: Optional[str] = None,  pool: Optional[int] = 3):
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

@app.get('/search_song')
def search_song_api(query: Optional[str] = None):
    return search_song(query)
