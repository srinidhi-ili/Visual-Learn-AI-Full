def generate_summary(text):

    import re

    text = text.replace("\x0b", " ")

    lines = [
        line.strip()
        for line in re.split(r'[\n\r]+', text)
        if line.strip()
    ]

    points = []

    for line in lines:

        if len(line) < 15:
            continue

        line = line.replace("•", "")

        words = line.split()

        if len(words) > 30:
            line = " ".join(words[:30])

        points.append("• " + line)

        if len(points) >= 4:
            break

    if not points:

        points.append("• No content found")

    return "\n".join(points)