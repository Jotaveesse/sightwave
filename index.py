import fastapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.lyrics_search import search_track_by_lyrics
from backend.features_search import search_track_by_features
from backend.image_search import *
from typing import List, Optional
from pydantic import BaseModel

app = fastapi.FastAPI()

# makes all files in the dir frontend available on the /static/ path
#static_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/frontend")
class ImageRequest(BaseModel):
    image: str

@app.get('/')
def index():
    return FileResponse("frontend/index.html")


@app.get('/api/search/literal')
def getLiteral(url: str):
    return search_track_literal(url = url)

@app.get('/api/search/emotional')
def getEmotional(url: str):
    return search_track_emotional(url = url)

@app.get('/api/search/both')
def getBoth(url: str):
    return search_track_both(url = url)

@app.post('/api/search/literal')
def postLiteral(image:ImageRequest):
    return search_track_literal(base64=image.image)

@app.post('/api/search/emotional')
def postEmotional(image:ImageRequest):
    return search_track_emotional(base64=image.image)

@app.post('/api/search/both')
def postBoth(image: ImageRequest):
    return search_track_both(base64=image.image)

@app.get('/api/search/lyrics')
def by_lyrics(query: str):
    return search_track_by_lyrics(query)

@app.get('/api/search/features')
def by_features(query: str):
    return search_track_by_features(query)

app.mount("/", StaticFiles(directory="frontend"), name="static")