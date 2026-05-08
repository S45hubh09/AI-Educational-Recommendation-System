from googleapiclient.discovery import build
import isodate   # ✅ ADDED

API_KEY = "AIzaSyBI-0TzsgI6FI59jqRarf8sWRLBCnisFug"
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_videos(topic):
    search_request = youtube.search().list(
        q=topic,
        part='snippet',
        type='video',
        maxResults=8
    )

    search_response = search_request.execute()

    videos = []

    for item in search_response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']

        Fixed_Words = [
            "tutorial",
            "course",
            "full course",
            "lecture",
            "lesson",
            "class",
            "training",
            "learn",
            "learning",
            "education",
            "educational",
            "explained",
            "explanation",
            "concept",
            "concepts",
            "basics",
            "beginner",
            "advanced",
            "guide",
            "step by step",
            "introduction",
            "crash course",
            "masterclass",
            "bootcamp",
            "demo",
            "walkthrough"
           ]
        title_lower = title.lower()

        if not any(word in title_lower for word in Fixed_Words):
            continue

        if "advanced" in topic.lower() and "beginner" in title_lower:
            continue

        # 🔥 EDIT HERE (add contentDetails)
        stats_request = youtube.videos().list(
            part='statistics,contentDetails',   # ✅ CHANGED
            id=video_id
        )
        stats_response = stats_request.execute()

        if len(stats_response['items']) == 0:
            continue

        video_data = stats_response['items'][0]

        stats = video_data['statistics']
        duration = video_data['contentDetails']['duration']   # ✅ ADDED

        # 🔥 convert duration
        duration_sec = isodate.parse_duration(duration).total_seconds()   # ✅ ADDED

        # ❌ filter shorts
        if duration_sec < 300:   # ✅ ADDED
            continue

        views = int(stats.get('viewCount', 0))
        likes = int(stats.get('likeCount', 0))

        comments_list = []

        try:
            comment_request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=5
            )
            comment_response = comment_request.execute()

            for comment in comment_response['items']:
                text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                comments_list.append(text)

        except:
            comments_list = []

        videos.append({
            "title": title,
            "video_id": video_id,
            "views": views,
            "likes": likes,
            "comments": comments_list
        })

    return videos