from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from clipper import create_clip

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

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        file_path = "uploads/input.mp4"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        clips = []

        timestamps = [
            (0, 10),
            (10, 20),
            (20, 30),
        ]

        for start, end in timestamps:
            output_path = create_clip(file_path, start, end)
            filename = os.path.basename(output_path)

            clips.append({
                "url": f"http://127.0.0.1:8000/outputs/{filename}"
            })

        return {
            "success": True,
            "clips": clips
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "success": False,
            "message": str(e),
            "clips": []
        }