from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.parser import parse_syllabus
from services.youtube import fetch_videos
from utils.ranking import rank_videos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    syllabusText: str

@app.post("/generate-course")
def generate_course(req: GenerateRequest):
    if not req.syllabusText.strip():
        raise HTTPException(status_code=400, detail="Syllabus text is required.")
        
    # 1. Parse syllabus using Gemini
    try:
        structured_data = parse_syllabus(req.syllabusText)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    result_data = []
    used_video_ids = set()
    
    # 2. For each topic fetch and rank videos
    for topic_item in structured_data:
        topic_name = topic_item.get("topic")
        subtopics = topic_item.get("subtopics", [])
        
        if not topic_name:
            continue
            
        topic_videos = fetch_videos(topic_name, max_results=10)
        topic_videos = rank_videos(topic_videos, topic_name)
        
        overview_video = None
        for vid in topic_videos:
            if vid['video_id'] not in used_video_ids:
                overview_video = vid
                used_video_ids.add(vid['video_id'])
                break
                
        subtopic_results = []
        for sub in subtopics:
            sub_query = f"{topic_name} {sub}"
            sub_videos = fetch_videos(sub_query, max_results=5)
            sub_videos = rank_videos(sub_videos, sub_query)
            
            sub_best_video = None
            for vid in sub_videos:
                if vid['video_id'] not in used_video_ids:
                    sub_best_video = vid
                    used_video_ids.add(vid['video_id'])
                    break
                    
            if sub_best_video:
                subtopic_results.append({
                    "subtopic": sub,
                    "video": sub_best_video
                })
        
        result_data.append({
            "topic": topic_name,
            "overview_video": overview_video,
            "subtopics": subtopic_results
        })
        
    return result_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)