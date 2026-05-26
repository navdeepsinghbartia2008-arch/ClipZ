import whisper
from moviepy.editor import VideoFileClip

model = whisper.load_model("tiny")

def transcribe_video(video_path):
    try:
        video = VideoFileClip(video_path)

        if video.audio is None:
            print("No audio found")
            return []

        audio_path = "uploads/temp_audio.wav"
        video.audio.write_audiofile(audio_path)

        result = model.transcribe(audio_path)
        return result["segments"]

    except Exception as e:
        print("Whisper error:", e)
        return []