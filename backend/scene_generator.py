import os
import glob
import re
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from text_to_speech import text_to_speech
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
print("PEXELS KEY:", PEXELS_API_KEY)

def get_image(keyword):

    url = f"https://api.pexels.com/v1/search?query={quote(keyword)}&per_page=1"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    response = requests.get(
        url,
        headers=headers
    )


    if response.status_code != 200:

        return "https://picsum.photos/800/500"

    data = response.json()

    if data.get("photos"):

        image_url = data["photos"][0]["src"]["large"]

        

        return image_url

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

        # Title
        if len(lines) >= 2:
            title = lines[0]
            subtitle = " ".join(lines[1:])
        else:
            title = f"Scene {i+1}"
            subtitle = lines[0]
        search_text = subtitle[:50]

        image_url = get_image(search_text)

         # Generate learning points

        content_text = " ".join(lines[1:])

        # Split by sentences
        points = re.split(r'[.!?]+', content_text)

        points = [
            p.strip()
            for p in points
            if len(p.strip()) > 10
        ]

        # If only one huge paragraph,
        # split every 15 words
        if len(points) <= 1:

            words = content_text.split()

            points = []

            chunk_size = 15

            for j in range(0, len(words), chunk_size):

                chunk = " ".join(
                    words[j:j + chunk_size]
                )

                if chunk.strip():
                    points.append(chunk)

        # Final fallback
        if not points:
            points = [subtitle]

        
        #  Generate narration audio
        
        summary_text = "\n".join(
            ["• " + p for p in points]
        )

        if not summary_text.strip():
            summary_text = "Educational content from this slide."

        audio_file = text_to_speech(
            summary_text,
            f"scene_{i+1}.mp3"
        )

    
        # Create scene data
        
        
        scene = {
            "scene": i + 1,
            "title": title,
            "subtitle": subtitle,
            "full_content": slide,
            "voice_text": summary_text,
            "audio_file": os.path.basename(audio_file),
            "image_url": image_url
        }

        scenes.append(scene)

    return scenes