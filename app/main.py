from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import playlist, stream

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://yt-music-frontend-gules.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    playlist.router,
    tags=["playlist"]
)

app.include_router(
    stream.router,
    tags=["stream"]
)

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }