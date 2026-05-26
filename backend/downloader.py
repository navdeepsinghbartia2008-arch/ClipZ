import yt_dlp
import os

def download_youtube_video(url):
    os.makedirs("uploads", exist_ok=True)

    output_path = "uploads/youtube_video.mp4"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_path,
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path