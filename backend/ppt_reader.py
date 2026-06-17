from pptx import Presentation


def extract_ppt_slides(path):

    prs = Presentation(path)

    slides_data = []

    for slide in prs.slides:

        texts = []

        for shape in slide.shapes:

            if hasattr(shape, "text"):

                text = shape.text.strip()

                if text:
                    texts.append(text)

        # longest text = actual content
        texts.sort(key=len, reverse=True)

        slide_text = "\n".join(texts)

        slides_data.append(slide_text)

    return slides_data