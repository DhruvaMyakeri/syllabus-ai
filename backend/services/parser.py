import re

def normalize_text(text):
    # unify separators
    text = text.replace(";", ",")
    text = text.replace(":", ",")
    text = text.replace(".", ",")

    # remove weird spacing
    text = re.sub(r"\s+", " ", text)

    return text


def clean_topic(t):
    t = t.strip()

    # remove "Unit 1", etc.
    t = re.sub(r"unit\s*\d+", "", t, flags=re.IGNORECASE)

    # fix spacing like "SelectiveRepeat"
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

        topics.append(part)

    # remove duplicates while preserving order
    seen = set()
    final = []

    for t in topics:
        if t.lower() not in seen:
            seen.add(t.lower())
            final.append(t)

    return final