import re

def normalize_text(text):
    text = text.replace(";", ",")
    text = text.replace(":", ",")
    text = text.replace(".", ",")

    text = re.sub(r"\s+", " ", text)
    return text


def clean_topic(t):
    t = t.strip()

    # remove unit labels
    t = re.sub(r"unit\s*\d+", "", t, flags=re.IGNORECASE)

    # split camel case
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)

    return t.strip()


def parse_syllabus(text):
    text = normalize_text(text)
    parts = text.split(",")

    topics = []

    for part in parts:
        part = clean_topic(part)

        if len(part) < 4:
            continue

        # split weird merged topics
        if "?" in part:
            topics.extend([p.strip() for p in part.split("?") if p.strip()])
        else:
            topics.append(part)

    # remove duplicates
    seen = set()
    final = []

    for t in topics:
        if t.lower() not in seen:
            seen.add(t.lower())
            final.append(t)

    return final