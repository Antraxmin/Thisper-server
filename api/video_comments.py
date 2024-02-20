import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os

load_dotenv()

def get_video_comments(video_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_title = video_response['items'][0]['snippet']['title']
    video_description = video_response['items'][0]['snippet']['description']

    comment_response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=20,
        order='relevance'  
    ).execute()

    comments = []
    for item in comment_response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        author = comment['authorDisplayName']
        like_count = comment['likeCount']
        comment_data = {
            'author': author,
            'like_count': like_count,
            'text': comment['textDisplay']
        }
        comments.append(comment_data)

    comments_sorted = sorted(comments, key=lambda x: x['like_count'], reverse=True)

    data = {
        'video_title': video_title,
        'video_description': video_description,
        'comments': comments_sorted
    }

    with open('youtube_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)