from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .image_search import *
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get('/api/search/emotional')
def getEmotional(url: str):
    return search_track_emotional(url = url)