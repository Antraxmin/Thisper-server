import json
import subprocess
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from service.video_comments import get_video_comments
import re

router = APIRouter()

class YoutubeLink(BaseModel):
    link: str

@router.post("/")
async def system_connect(link: YoutubeLink):
    if link.link.startswith('https://www.youtube.com/'):
        video_id_match = re.search(r"(?<=\?v=)([^\s&]+)", link.link)  
        if video_id_match:
            video_id = video_id_match.group(1) 
            get_video_comments(video_id) 
            subprocess.run(['python3', 'comments_analysis.py', 'youtube_data.json'])

            with open("youtube_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                results = data["result"]
            
        response = {
            "message": "유효한 유튜브 링크입니다 ", 
            "data": results
        }
        return response

    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 유튜브 링크입니다.")
