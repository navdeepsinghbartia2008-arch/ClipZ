from moviepy.editor import VideoFileClip
import os

os.makedirs("outputs", exist_ok=True)

def create_clip(video_path, start, end):
    output_path = f"outputs/clip_{int(start)}_{int(end)}.mp4"

    video = VideoFileClip(video_path)
    duration = video.duration

    start = max(0, min(start, duration - 1))
    end = max(start + 1, min(end, duration))

    clip = video.subclip(start, end)

    clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30
    )

    clip.close()
    video.close()

    return output_path