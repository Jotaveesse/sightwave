import fastapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.lyrics_search import search_track_by_lyrics
from backend.features_search import search_track_by_features
from backend.image_search import search_track_by_image
from typing import List, Optional

app = fastapi.FastAPI()

# makes all files in the dir frontend available on the /static/ path
#static_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/frontend")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get('/')
def index():
    return FileResponse("frontend/index.html")

@app.get('/api/search/image')
def by_image(url: str):
    return search_track_by_image(url)

@app.get('/api/search/lyrics')
def by_lyrics(query: str):
    return search_track_by_lyrics(query)

@app.get('/api/search/features')
def by_features(query: str):
    return search_track_by_features(query)
