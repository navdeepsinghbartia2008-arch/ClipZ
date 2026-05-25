import whisper
import subprocess

model = whisper.load_model("base")


def has_audio(video_path):
    command = [
        "ffprobe",
        "-i",
        video_path,
        "-show_streams",
        "-select_streams",
        "a",
        "-loglevel",
        "error"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout != ""


def transcribe_video(video_path):

    # If video has no audio
    if not has_audio(video_path):
        print("No audio found in video")

        return [
            {
                "start": 0,
                "end": 15,
                "text": "Silent video"
            }
        ]

    result = model.transcribe(video_path)

    return result["segments"]