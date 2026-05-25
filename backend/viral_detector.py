def detect_viral_clips(segments):
    clips = []

    if len(segments) == 0:
        return clips

    for segment in segments:
        start = segment["start"]
        end = segment["end"]

        # make 15 sec clips
        clip_end = start + 15

        if clip_end > end:
            clip_end = end

        clips.append((start, clip_end))

        # max 5 clips
        if len(clips) >= 5:
            break

    return clips