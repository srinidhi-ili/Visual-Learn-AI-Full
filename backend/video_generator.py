from moviepy import (
    ImageClip,
    AudioFileClip,
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)
def create_video(
    image_path,
    audio_path,
    output_path,
    subtitle_text=""
):

    audio = AudioFileClip(audio_path)

    image = (
        ImageClip(image_path)
        .resized(height=480)   # Faster than 720
        .with_duration(audio.duration)
    )

    words = subtitle_text.split()

    chunk_size = 40   # More words per subtitle

    subtitle_clips = []

    total_chunks = max(
        1,
        (len(words) + chunk_size - 1) // chunk_size
    )

    chunk_duration = audio.duration / total_chunks

    for i in range(total_chunks):

        chunk_text = " ".join(
            words[
                i * chunk_size:
                (i + 1) * chunk_size
            ]
        )

        clip = (
    TextClip(
        text=chunk_text,
        font_size=12,
        color="white",
        method="caption",
        size=(400, None)
    )
    .with_start(i * chunk_duration)
    .with_duration(chunk_duration)
    .with_position(("center", image.h - 120))
)

        subtitle_clips.append(clip)

    video = CompositeVideoClip(
        [image] + subtitle_clips
    ).with_audio(audio)

    video.write_videofile(
        output_path,
        fps=12,                # Faster
        codec="libx264",
        preset="ultrafast",
        threads=4
    )

    audio.close()
    video.close()

    return output_path
def merge_videos(
    video_files,
    output_file
):

    clips = []

    for video in video_files:
        clips.append(
                   VideoFileClip(video)
        )

    final_video = concatenate_videoclips(
        clips,
        method="compose"
    )

    final_video.write_videofile(
        output_file,
        fps=12,
        codec="libx264",
        preset="ultrafast",
        threads=4
    )

    for clip in clips:
        clip.close()

    final_video.close()

    return output_file