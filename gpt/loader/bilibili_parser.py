import json
from typing import Dict, NamedTuple
import requests

class VideoInfo(NamedTuple):
    bvid: str
    aid: int
    title: str
    tname: str
    desc: str
    owner: str
    stat: Dict
    dynamic: str
    transcript: str
    
    
def parse_get_info(video_info: Dict) -> VideoInfo:
    """parse bilibili get_info message"""
    subtitle = video_info.pop("subtitle")
    sub_list = subtitle["list"]
    raw_transcript = ""
    if sub_list:
        sub_url = sub_list[0]["subtitle_url"]
        result = requests.get(sub_url)
        raw_sub_titles = json.loads(result.content)["body"]
        raw_transcript = " ".join([c["content"] for c in raw_sub_titles])

    return VideoInfo(
        transcript=raw_transcript,
        bvid=video_info['bvid'],
        aid=video_info['aid'],
        title=video_info['title'],
        tname=video_info["tname"],
        desc=video_info["desc"],
        owner=video_info["owner"]["name"],
        dynamic=video_info["dynamic"],
        stat=video_info["stat"])