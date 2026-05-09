import yt_dlp
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
import asyncio

executor = ThreadPoolExecutor(max_workers=3)

async def _run_blocking(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: fn(*args, **kwargs))

async def extract_playlist_metadata(url: str) -> Dict[str, Any]:
    if not url or "playlist" not in url and "list=" not in url:
        raise ValueError("Invalid playlist URL")

    def _extract(u: str):
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "ignoreerrors": True,
            "extract_flat": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(u, download=False)
            return info

    info = await _run_blocking(_extract, url)
    # Normalize playlist and entries
    playlist_title = info.get("title") if info else None
    playlist_thumbnail = info.get("thumbnails", [{}])[-1].get("url") if info and info.get("thumbnails") else None
    entries = info.get("entries") if info else []
    songs = []
    for e in entries or []:
        if not e:
            continue
        # skip if video is private or unavailable
        if e.get("_type") == "url" and e.get("ie_key") == "Youtube":
            # entry may be a compact dict
            video_id = e.get("id") or e.get("url")
        else:
            video_id = e.get("id")
        if not video_id:
            continue
        title = e.get("title") or "Unknown Title"
        thumbnail = None
        if e.get("thumbnails"):
            thumbnail = e.get("thumbnails")[-1].get("url")
        duration = e.get("duration")
        channel = None
        uploader = e.get("uploader") or e.get("channel")
        if uploader:
            channel = uploader
        songs.append({
            "id": video_id,
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration or 0,
            "channel": channel or "",
        })

    return {
        "title": playlist_title,
        "thumbnail": playlist_thumbnail,
        "total": len(songs),
        "songs": songs,
    }

async def get_stream_url_for_video(video_id: str) -> str:
    if not video_id:
        raise ValueError("Missing video id")

    def _extract(vid: str):
        # Use yt_dlp to retrieve direct audio format URL without downloading
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "bestaudio/best",
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
            # formats list may contain audio entries with a direct url
            formats = info.get("formats") or []
            # prefer audio-only formats
            audio_formats = [f for f in formats if f.get("acodec") and f.get("url")]
            if not audio_formats:
                # fallback to any format with url
                audio_formats = [f for f in formats if f.get("url")]
            # choose best by tbr or bitrate
            def score(f):
                return (f.get("tbr") or f.get("abr") or 0)
            best = max(audio_formats, key=score) if audio_formats else None
            if not best:
                raise ValueError("No streamable audio format found")
            return best.get("url")

    url = await _run_blocking(_extract, video_id)
    if not url:
        raise ValueError("Failed to generate stream URL")
    return url
