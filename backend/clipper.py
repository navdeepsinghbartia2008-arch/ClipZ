from moviepy.editor import VideoFileClip
import cv2
import os
import uuid
import textwrap

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_W = 1080
TARGET_H = 1920


def detect_face_center(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        if len(faces) == 0:
            return frame.shape[1] // 2

        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

        return x + w // 2

    except Exception:
        return frame.shape[1] // 2


def draw_caption(frame, caption):
    if not caption:
        return frame

    frame = frame.copy()
    caption = caption.strip().upper()

    words = caption.split()
    lines = []
    current = ""

    for word in words:
        if len(current + " " + word) < 18:
            current += " " + word
        else:
            lines.append(current.strip())
            current = word

    if current:
        lines.append(current.strip())

    lines = lines[:3]

    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.7
    thickness = 4

    start_y = TARGET_H - 520

    highlight_words = {
        "AMAZING",
        "CRAZY",
        "WOW",
        "INSANE",
        "SHOCKING",
        "SECRET",
        "VIRAL",
        "BEST",
        "NEVER",
        "STOP",
        "BRO",
        "MONEY",
        "AI",
        "FAST",
        "NEW",
    }

    for line_index, line in enumerate(lines):
        y = start_y + line_index * 105

        words = line.split()
        total_width = 0
        word_sizes = []

        for word in words:
            size = cv2.getTextSize(word, font, font_scale, thickness)[0]
            word_sizes.append((word, size))
            total_width += size[0] + 24

        x = (TARGET_W - total_width) // 2

        for word, size in word_sizes:
            is_highlight = word in highlight_words

            color = (0, 255, 255) if is_highlight else (255, 255, 255)

            cv2.putText(
                frame,
                word,
                (x, y),
                font,
                font_scale,
                (0, 0, 0),
                thickness + 8,
                cv2.LINE_AA,
            )

            cv2.putText(
                frame,
                word,
                (x + 3, y + 3),
                font,
                font_scale,
                (255, 0, 180),
                thickness + 3,
                cv2.LINE_AA,
            )

            cv2.putText(
                frame,
                word,
                (x, y),
                font,
                font_scale,
                color,
                thickness,
                cv2.LINE_AA,
            )

            x += size[0] + 28

    return frame


def create_clip(video_path, start, end, caption=""):
    video = VideoFileClip(video_path)

    duration = video.duration

    start = max(0, min(start, duration - 1))
    end = max(start + 1, min(end, duration))

    clip = video.subclip(start, end)

    sample_frame = clip.get_frame(clip.duration / 2)
    face_center_x = detect_face_center(sample_frame)

    def process_frame(frame):
        h, w, _ = frame.shape

        crop_w = int(h * 9 / 16)

        if crop_w > w:
            crop_w = w

        x1 = int(face_center_x - crop_w / 2)
        x1 = max(0, min(x1, w - crop_w))
        x2 = x1 + crop_w

        cropped = frame[:, x1:x2]

        resized = cv2.resize(
            cropped,
            (TARGET_W, TARGET_H),
            interpolation=cv2.INTER_AREA
        )

        resized = draw_caption(resized, caption)

        return resized

    final_clip = clip.fl_image(process_frame)

    filename = f"clip_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)

    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30
    )

    clip.close()
    video.close()
    final_clip.close()

    return output_path