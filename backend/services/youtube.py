from googleapiclient.discovery import build

def get_youtube():
    return build("youtube", "v3", developerKey="AIzaSyAJCVp2PUdNhzJzUiIJZRWes_LPWYmvHwU")


def search_videos(query):
    youtube = get_youtube()

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=3,
        type="video"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    stats_response = youtube.videos().list(
        part="statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()

    stats_map = {item["id"]: item for item in stats_response["items"]}

    videos = []

    for item in search_response["items"]:
        vid = item["id"]["videoId"]
        stats = stats_map.get(vid, {})

        videos.append({
            "title": item["snippet"]["title"],
            "video_id": vid,
            "channel": item["snippet"]["channelTitle"],
            "views": int(stats.get("statistics", {}).get("viewCount", 0)),
            "likes": int(stats.get("statistics", {}).get("likeCount", 0)),
            "comments": int(stats.get("statistics", {}).get("commentCount", 0)),
            "duration": stats.get("contentDetails", {}).get("duration", "")
        })

    return videos