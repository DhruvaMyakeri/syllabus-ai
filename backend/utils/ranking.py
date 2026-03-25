import math
import re

def parse_duration_seconds(duration_str: str) -> int:
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds

def score_video(video: dict, query: str) -> float:
    # 1. Title relevance
    title_lower = video['title'].lower()
    query_terms = query.lower().split()
    relevance_score = sum(1 for term in query_terms if term in title_lower) / max(len(query_terms), 1)
    
    # 2. Views (log scale)
    views = video.get('views', 0)
    view_score = math.log10(views + 1)
    
    # 3. Likes/Views ratio
    likes = video.get('likes', 0)
    like_ratio = likes / max(views, 1)
    
    # 4. Comments
    comments = video.get('comments', 0)
    comment_score = math.log10(comments + 1)
    
    # 5. Duration bonus (prefer 5-20 min)
    duration_sec = parse_duration_seconds(video.get('duration', ''))
    duration_min = duration_sec / 60
    
    if 5 <= duration_min <= 20:
        duration_bonus = 2.0
    elif 20 < duration_min <= 60:
        duration_bonus = 1.0
    else:
        duration_bonus = 0.0
        
    final_score = (relevance_score * 5.0) + view_score + (like_ratio * 100) + (comment_score * 0.5) + duration_bonus
    video['score'] = final_score
    return final_score

def rank_videos(videos: list, query: str) -> list:
    for vid in videos:
        score_video(vid, query)
    
    # Sort descending based on computed score
    ranked = sorted(videos, key=lambda x: x.get('score', 0), reverse=True)
    return ranked