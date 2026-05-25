import whisper
from moviepy.editor import VideoFileClip

model = whisper.load_model("base")

def transcribe_video(video_path):
    try:
        video = VideoFileClip(video_path)

        # Check if audio exists
        if video.audio is None:
            print("No audio found in video")
            return []

        audio_path = "temp_audio.wav"

        # Extract audio
        video.audio.write_audiofile(audio_path)

        # Transcribe
        result = model.transcribe(audio_path)

        return result["segments"]

    except Exception as e:
        print("Whisper Error:", e)
        return []