import math
import re

def parse_duration(duration):
    minutes = re.search(r"(\d+)M", duration)
    seconds = re.search(r"(\d+)S", duration)

    total = 0
    if minutes:
        total += int(minutes.group(1)) * 60
    if seconds:
        total += int(seconds.group(1))

    return total


def score_video(video, query):
    score = 0

    title = video["title"].lower()
    query = query.lower()

    if query in title:
        score += 100

    score += math.log(video["views"] + 1) * 2

    if video["views"] > 0:
        score += (video["likes"] / video["views"]) * 200

    score += math.log(video["comments"] + 1) * 2

    duration = parse_duration(video["duration"])

    if 300 <= duration <= 1200:
        score += 30

    return score


def rank_videos(videos, query):
    for v in videos:
        v["score"] = score_video(v, query)

    return sorted(videos, key=lambda x: x["score"], reverse=True)