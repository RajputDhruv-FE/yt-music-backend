from fastapi import APIRouter
from yt_dlp import YoutubeDL

router = APIRouter()

@router.get("/stream/{video_id}")
async def get_stream(video_id: str):

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio",
        "quiet": True,
        "noplaylist": True,
    }

    try:

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                video_url,
                download=False
            )

        return {
            "stream_url": info["url"]
        }

    except Exception as e:

        print(e)

        return {
            "error": str(e)
        }