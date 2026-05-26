from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os

from whisper_ai import transcribe_video
from viral_detector import detect_viral_clips
from clipper import create_clip
from downloader import download_youtube_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


class YouTubeRequest(BaseModel):
    url: str


def generate_clips(video_path):
    segments = transcribe_video(video_path)

    if segments:
        viral_clips = detect_viral_clips(segments)
    else:
        viral_clips = [
            (0, 10),
            (10, 20),
            (20, 30),
        ]

    clips = []

    for index, (start, end) in enumerate(viral_clips):
        caption = ""

        if segments and index < len(segments):
            caption = segments[index]["text"]

        output_path = create_clip(
            video_path,
            start,
            end,
            caption
        )

        filename = os.path.basename(output_path)

        clips.append({
            "url": f"http://127.0.0.1:8000/outputs/{filename}"
        })

    return clips


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        file_path = "uploads/input.mp4"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        clips = generate_clips(file_path)

        return {
            "success": True,
            "clips": clips
        }

    except Exception as e:
        print("ERROR:", e)

        return {
            "success": False,
            "message": str(e),
            "clips": []
        }


@app.post("/youtube")
async def youtube_video(data: YouTubeRequest):
    try:
        file_path = download_youtube_video(data.url)

        clips = generate_clips(file_path)

        return {
            "success": True,
            "clips": clips
        }

    except Exception as e:
        print("YOUTUBE ERROR:", e)

        return {
            "success": False,
            "message": str(e),
            "clips": []
        }