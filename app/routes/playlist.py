

from fastapi import APIRouter
from yt_dlp import YoutubeDL

router = APIRouter()

@router.get("/playlist")
async def get_playlist(url: str):

    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    songs = []

    for entry in info["entries"]:

        if not entry:
            continue

        songs.append({
            "id": entry.get("id"),
            "title": entry.get("title"),
            "thumbnail": f"https://i.ytimg.com/vi/{entry.get('id')}/hqdefault.jpg"
        })

    return {
        "playlist_title": info.get("title"),
        "songs": songs
    }