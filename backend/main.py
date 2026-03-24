from fastapi import FastAPI
from backend.services.parser import parse_syllabus
from backend.services.expander import expand_all
from backend.services.youtube import search_videos
from backend.utils.ranking import rank_videos

app = FastAPI()

cache = {}

@app.post("/generate-course")
def generate_course(data: dict):
    syllabus = data.get("syllabus")

    if syllabus in cache:
        return cache[syllabus]

    topics = parse_syllabus(syllabus)
    expanded = expand_all(topics)

    course = []

    for topic_data in expanded:
        topic = topic_data["name"]
        subtopics = topic_data["subtopics"][:4]

        # Overview video
        overview_videos = search_videos(f"{topic} full explanation")
        overview_videos = rank_videos(overview_videos, topic)
        overview = overview_videos[0] if overview_videos else None

        sub_data = []

        for sub in subtopics:
            videos = search_videos(f"{sub} explained")
            videos = rank_videos(videos, sub)

            sub_data.append({
                "name": sub,
                "video": videos[0] if videos else None
            })

        course.append({
            "topic": topic,
            "overview_video": overview,
            "subtopics": sub_data
        })

    result = {"course": course}
    cache[syllabus] = result

    return result