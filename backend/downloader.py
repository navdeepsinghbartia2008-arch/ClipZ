import yt_dlp
import os

def download_youtube_video(url):
    os.makedirs("uploads", exist_ok=True)

    output_path = "uploads/youtube_video.%(ext)s"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_path,
        "quiet": False,
        "noplaylist": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        },
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "uploads/youtube_video.mp4"