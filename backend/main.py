from fastapi import FastAPI
from backend.services.parser import parse_syllabus
from backend.services.youtube import search_videos
from backend.utils.ranking import rank_videos
from backend.utils.filter import is_relevant

app = FastAPI()

cache = {}

@app.post("/generate-course")
def generate_course(data: dict):
    syllabus = data.get("syllabus")

    if syllabus in cache:
        return cache[syllabus]

    topics = parse_syllabus(syllabus)

    course = []

    for topic in topics:
        used_videos = set()

        # 🔥 overview
        videos = search_videos(topic)
        videos = rank_videos(videos, topic)

        videos = [v for v in videos if is_relevant(v, topic)]

        overview = videos[0] if videos else None

        subtopics = [
            f"{topic} basics",
            f"{topic} examples",
            f"{topic} problems",
            f"{topic} applications"
        ]

        sub_data = []

        for sub in subtopics:
            videos = search_videos(sub)
            videos = rank_videos(videos, sub)

            # 🔥 filter irrelevant
            videos = [v for v in videos if is_relevant(v, sub)]

            best_video = None

            for v in videos:
                if v["video_id"] not in used_videos:
                    best_video = v
                    used_videos.add(v["video_id"])
                    break

            sub_data.append({
                "name": sub,
                "video": best_video
            })

        course.append({
            "topic": topic,
            "overview_video": overview,
            "subtopics": sub_data
        })

    result = {"course": course}
    cache[syllabus] = result

    return result