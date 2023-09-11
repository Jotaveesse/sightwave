from dotenv import load_dotenv

load_dotenv()

import fastapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.lyrics_search import search_track_by_lyrics
from backend.features_search import search_track_by_features
from backend.image_search import *
from pydantic import BaseModel

app = fastapi.FastAPI()


# estrutura do body dos caminhos de post
class ImageRequest(BaseModel):
    image: str


@app.get("/")
def index():
    return FileResponse("frontend/index.html")


# caminhos para envio de url
@app.get("/api/search/literal")
def getLiteral(url: str, amount: int):
    return search_track_literal(url=url, amount=amount)


@app.get("/api/search/emotional")
def getEmotional(url: str, amount: int):
    return search_track_emotional(url=url, amount=amount)


@app.get("/api/search/both")
def getBoth(url: str, amount: int):
    return search_track_both(url=url, amount=amount)


# caminhos pra upload de imagem
@app.post("/api/search/literal")
def postLiteral(image: ImageRequest, amount: int):
    return search_track_literal(base64=image.image, amount=amount)


@app.post("/api/search/emotional")
def postEmotional(image: ImageRequest, amount: int):
    return search_track_emotional(base64=image.image, amount=amount)


@app.post("/api/search/both")
def postBoth(image: ImageRequest, amount: int):
    return search_track_both(base64=image.image, amount=amount)


# caminhos para teste
@app.get("/api/search/lyrics")
def by_lyrics(query: str):
    return search_track_by_lyrics(query)


@app.get("/api/search/features")
def by_features(query: str):
    return search_track_by_features(query)


# makes all files in the dir frontend available on root path
app.mount("/", StaticFiles(directory="frontend"), name="static")
