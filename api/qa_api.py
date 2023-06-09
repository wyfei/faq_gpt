from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from gpt import qa_answer, summary_bilibili_video, idle_ask
import re
from config import Config
import json
import requests
import secrets
from gpt.call_back import ChatOpenAIStreamingResponse, Sender
from typing import Awaitable, Callable
from pydantic import BaseModel

router = APIRouter()

cfg = Config()

sender = secrets.token_urlsafe(16)
    

class StreamRequest(BaseModel):
    """Request body for streaming."""
    message: str
    recipient_id: int
    
def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg)
        except ValueError:
            return False
        return True
    else:
        return False

@router.post("/star")
async def request_handler_star(query: StreamRequest):
    message = query.message
    recipientId = query.recipient_id
    # intent = nlu_decide(message=message)
    # if intent == 'ask_summary':
    #     bvid_url = re.search(r"https://www.bilibili.com/video/BV[a-zA-Z0-9]+", message)
    #     if bvid_url is not None:
    #         return summary_bilibili_video(bvid_url.group())
    #     else:
    #         bvid = re.search(r"BV[a-zA-Z0-9]+", message)
    #         return summary_bilibili_video(bvid.group())
    # elif intent == 'greet' or intent == 'goodbye' or intent == 'ask_date' or intent == 'ask_time':
    #     rasa_result = rasa_webhook_execute(message)
    #     return ChatOpenAIStreamingResponse(send_message(rasa_result), media_type="text/event-stream")  
    # elif intent == 'ask_question':
    #     return qa_answer(query)
    # else:
    #     return idle_ask(message)
    
    rasa_result = rasa_webhook_execute(message, recipientId)
    if(check_json_format(rasa_result)):
        result_json = json.loads(rasa_result)
        typ = result_json["type"]
        mes = result_json["message"]
        if typ == "question":
            return qa_answer(mes)
        elif typ == "summary":
            bvid_url = re.search(r"https://www.bilibili.com/video/BV[a-zA-Z0-9]+", mes)
            if bvid_url is not None:
                return summary_bilibili_video(bvid_url.group())
            else:
                bvid = re.search(r"BV[a-zA-Z0-9]+", mes)
                return summary_bilibili_video(bvid.group())
        elif typ == "chitchat":
            return idle_ask(mes)
        else:
            return ChatOpenAIStreamingResponse(send_message(mes), media_type="text/event-stream")  
    else:
        return ChatOpenAIStreamingResponse(send_message(rasa_result), media_type="text/event-stream")  
    

def nlu_decide(message: str) -> str:
    url=cfg.rasa_nlu_api
    request_data = {"text": message}
    json_result = post(url, request_data)
    return json_result["intent"]["name"]

def rasa_webhook_execute(message: str, recipientId: int) -> str:
    url=cfg.rasa_rest_api
    send_id = sender
    # if recipientId:
    #     send_id = str(recipientId)
        
    data = {
        "sender": send_id,
        "message": message
    }
    result = post(url, data)
    
    if len(result) == 0:
        return "系统繁忙，请稍后再试！"
    return result[0]["text"]
    
def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    r = json.loads(r.text)
    return r

def send_message(message: str) -> Callable[[Sender], Awaitable[None]]:
    async def generate(send: Sender):
        for mes in message.split("\n"):
            await send(f"data: {mes}\n\n\n")

    return generate
