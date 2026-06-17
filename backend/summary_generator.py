def generate_summary(text):

    import re

    text = text.replace("\x0b", " ")

    sentences = re.split(r'[.!?]', text)

    points = []

    keywords = [
        "is",
        "are",
        "can",
        "used",
        "helps",
        "provides",
        "includes",
        "allows",
        "important",
        "benefits"
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 20:
            continue

        if any(word in sentence.lower() for word in keywords):

            if ":" in sentence:
                sentence = sentence.split(":")[0]

            sentence = " ".join(sentence.split()[:15])

            points.append("• " + sentence)

        if len(points) >= 3:
            break

    if not points:

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) > 20:

                points.append("• " + sentence[:80])

            if len(points) >= 3:
                break

    return "\n".join(points)
    print("SUMMARY POINTS:")
    for p in points:

        print(repr(p))
