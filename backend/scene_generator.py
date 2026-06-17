from video_generator import create_video, merge_videos

import requests
from urllib.parse import quote
from text_to_speech import text_to_speech

from video_generator import create_video
from summary_generator import generate_summary
from flowchart_generator import create_flowchart
print("SCENE_GENERATOR LOADED")

PEXELS_API_KEY = ""


def get_image(keyword):

    url = f"https://api.pexels.com/v1/search?query={quote(keyword)}&per_page=1"

    headers = {
        "Authorization": PEXELS_API_KEY
    }
    print("CALLING PEXELS...")

    response = requests.get(url, headers=headers)
    print("PEXELS RESPONSE RECEIVED")

    data = response.json()

    print("KEYWORD:", keyword)
    print("RESULT:", data)

    if data.get("photos"):
        return data["photos"][0]["src"]["medium"]

    return "https://picsum.photos/600/400"


def generate_scenes(text):
    import glob
    import os
    import time

    for file in glob.glob("scene_*.jpg"):
        os.remove(file)

    for file in glob.glob("scene_*.mp4"):

        os.remove(file)

    for file in glob.glob("audio/scene_*.mp3"):

        os.remove(file)

    slides = [
        slide.strip()
        for slide in text.split("===SLIDE===")
        if slide.strip()
    ]
    print("TOTAL SLIDES FOUND:", len(slides))

    scenes = []
    video_files = []
    for i, slide in enumerate(slides):

        import re

        clean_slide = slide.replace("\x0b", "\n")

        lines = [
    line.strip()
    for line in re.split(r'[\n\r]+', clean_slide)
    if line.strip()
]

        print("LINES:", lines)

        if not lines:
           continue

        if len(lines) >= 2:
         

         title = lines[0]
         subtitle = " ".join(lines[1:])

        else:

         title = f"Scene {i+1}"
         subtitle = lines[0]

        print("SCENE:", i + 1)
        print("TITLE:", title)
        print("SUBTITLE:", subtitle)

        keyword = (title + " " + subtitle)[:100]

        summary_text = generate_summary("\n".join(lines))
        

        points = []

        for line in summary_text.split("\n"):
           

            line = line.replace("•", "").strip()

            if line:
                points.append(line)
        print("SUMMARY:")
        print(summary_text)

        print("SUMMARY TEXT:")
        print(summary_text)
        print("SUMMARY REPR:")
        print(repr(summary_text))

        voice_text = summary_text
        print("VOICE TEXT FULL:")
        print(repr(voice_text))

        print("VOICE TEXT:")
        print(voice_text)

        import time

        start = time.time()

        audio_file = text_to_speech(
    voice_text,
    f"scene_{i+1}.mp3"
)

        print("TTS TIME:", time.time() - start)

        video_file = f"scene_{i+1}.mp4"

        image_file = f"scene_{i+1}.jpg"

        create_flowchart(
    points,
    image_file
)

        image_url = image_file

        start = time.time()

        create_video(
    image_file,
    audio_file,
    video_file,
    voice_text
)

        print("VIDEO TIME:", time.time() - start)

        scene = {
    "scene": i + 1,
    "title": title,
    "subtitle": subtitle,
    "full_content": slide,

        "voice_text": voice_text,
        "audio_file": audio_file,
        "image_prompt": f"Educational illustration of {title}",
        "keyword": keyword,
        "image_url": image_url
    }
        print("FINAL SCENE DATA")
        print("TITLE =", title)
        print("SUBTITLE =", subtitle[:100])

        scenes.append(scene)
        video_files.append(video_file)

    if len(video_files) > 0:

        merge_videos(
        video_files,
        "final_video.mp4"
    )

    return scenes
   