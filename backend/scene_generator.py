import os
import glob
import re
import requests
import time
from urllib.parse import quote
from dotenv import load_dotenv
from text_to_speech import text_to_speech

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def get_image(keyword):

    url = f"https://api.pexels.com/v1/search?query={quote(keyword)}&per_page=1"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    response = requests.get(
    url,
    headers=headers,
    timeout=10
)

    if response.status_code != 200:
        return "https://picsum.photos/800/500"

    data = response.json()

    if data.get("photos"):
        return data["photos"][0]["src"]["large"]

    return "https://picsum.photos/800/500"


def generate_scenes(text):

    # Delete old audio
    for file in glob.glob("audio/scene_*.mp3"):
        try:
            os.remove(file)
        except:
            pass

    # Split slides
    slides = [
        s.strip()
        for s in text.split("===SLIDE===")
        if s.strip()
    ]

    scenes = []

    for i, slide in enumerate(slides):

        clean_slide = slide.replace("\x0b", "\n")

        lines = [
            line.strip()
            for line in re.split(r'[\n\r]+', clean_slide)
            if line.strip()
        ]

        if not lines:
            continue

        # Full slide content
        subtitle = " ".join(lines)

        # First 2 lines used for image search
        search_text = " ".join(lines)
        search_text = search_text[:400]

        print("IMAGE SEARCH:", search_text)

        start = time.time()
        image_url = get_image(search_text)
        print(f"Pexels took: {time.time() - start:.2f} seconds")

        # Show entire slide content
        summary_text = "\n".join(lines)

        if not summary_text.strip():
            summary_text = "Educational content from this slide."

        start = time.time()

        audio_file = text_to_speech(
    summary_text,
    f"scene_{i+1}.mp3"
)

        print(f"Audio took: {time.time() - start:.2f} seconds")

        scene = {
            "scene": i + 1,
            "subtitle": subtitle,
            "full_content": slide,
            "voice_text": summary_text,
            "audio_file": os.path.basename(audio_file),
            "image_url": image_url
        }

        scenes.append(scene)

    return scenes