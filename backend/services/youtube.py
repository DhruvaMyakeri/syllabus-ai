from googleapiclient.discovery import build
import os

# Hardcoded API key as requested
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
youtube = build('youtube', 'v3', developerKey="")

video_cache = {}

def fetch_videos(query: str, max_results: int = 5) -> list:
    if query in video_cache:
        return video_cache[query]
        
    try:
        request = youtube.search().list(
            part="snippet",
            q=query + " tutorial lecture",
            type="video",
            maxResults=max_results,
            relevanceLanguage="en",
            videoEmbeddable="true"
        )
        response = request.execute()
        
        video_ids = [item['id']['videoId'] for item in response.get('items', [])]
        if not video_ids:
            return []
            
        stats_request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids)
        )
        stats_response = stats_request.execute()
        
        videos = []
        for item in stats_response.get('items', []):
            videos.append({
                'title': item['snippet']['title'],
                'video_id': item['id'],
                'channel': item['snippet']['channelTitle'],
                'views': int(item['statistics'].get('viewCount', 0)),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'comments': int(item['statistics'].get('commentCount', 0)),
                'duration': item['contentDetails']['duration'],
            })
            
        video_cache[query] = videos
        return videos
    except Exception as e:
        print(f"YouTube API Error fetching '{query}':", e)
        return []