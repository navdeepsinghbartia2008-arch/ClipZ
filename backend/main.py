from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os

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
    clips = []

    timestamps = [
        (0, 10),
        (10, 20),
        (20, 30)
    ]

    for start, end in timestamps:
        output_path = create_clip(video_path, start, end)

        filename = os.path.basename(output_path)

        clips.append({
            "url": f"https://clipz-backend.onrender.com/outputs/{filename}"
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