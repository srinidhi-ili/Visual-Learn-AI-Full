from gtts import gTTS
import os

def text_to_speech(text, filename):

    os.makedirs("audio", exist_ok=True)

    filepath = os.path.join("audio", filename)

    gTTS(
        text=text,
        lang="en",
        slow=False
    ).save(filepath)

    return filepath