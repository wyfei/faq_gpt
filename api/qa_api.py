from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from gpt import qa_answer, summary_bilibili_video, StreamRequest, idle_ask
import re
from config import Config
import json
import requests
import secrets
from gpt.call_back import ChatOpenAIStreamingResponse, Sender
from typing import Awaitable, Callable

router = APIRouter()

cfg = Config()

@router.post("/star")
async def request_handler_star(query: StreamRequest):
    message = query.message
    intent = nlu_decide(message=message)
    if intent == 'ask_summary':
        bvid_url = re.search(r"https://www.bilibili.com/video/BV[a-zA-Z0-9]+", message)
        if bvid_url is not None:
            return summary_bilibili_video(bvid_url.group())
        else:
            bvid = re.search(r"BV[a-zA-Z0-9]+", message)
            return summary_bilibili_video(bvid.group())
    elif intent == 'greet' or intent == 'goodbye' or intent == 'ask_date' or intent == 'ask_time':
        rasa_result = rasa_webhook_execute(message)
        return ChatOpenAIStreamingResponse(send_message(rasa_result), media_type="text/event-stream")  
    elif intent == 'ask_question':
        return qa_answer(query)
    else:
        return idle_ask(message)

def nlu_decide(message: str) -> str:
    url=cfg.rasa_nlu_api
    request_data = {"text": message}
    json_result = post(url, request_data)
    return json_result["intent"]["name"]

def rasa_webhook_execute(message: str) -> str:
    url=cfg.rasa_rest_api
    sender = secrets.token_urlsafe(16)
    data = {
        "sender": sender,
        "message": message
    }
    result = post(url, data)
    return result[0]["text"]
    
def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    r = json.loads(r.text)
    return r

def send_message(message: str) -> Callable[[Sender], Awaitable[None]]:
    async def generate(send: Sender):
        await send(f"data: {message}\n\n")

    return generate
