from PIL import Image, ImageDraw, ImageFont
import textwrap


def create_flowchart(points, output_file):

    img = Image.new(
        "RGB",
        (800, 600),
        "white"
    )

    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    y = 50

    for point in points:
        print("FLOWCHART POINT:", repr(point))
        print(repr(point))

        clean_point = point

        clean_point = clean_point.replace("\xa0", " ")
        clean_point = clean_point.replace("A", " ")

        wrapped_text = "\n".join(
        textwrap.wrap(clean_point, width=25)
)

        draw.rectangle(
            (150, y, 650, y + 100),
            outline="black",
            width=2
        )

        draw.text(
            (170, y + 15),
            wrapped_text,
            fill="black",
            font=font
        )

        if y < 400:

            draw.line(
                (400, y + 100, 400, y + 140),
                fill="black",
                width=3
            )

        y += 140

    img.save(output_file)