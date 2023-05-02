from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from gpt import qa_answer, StreamRequest

router = APIRouter()

@router.post("/star")
async def request_handler(query: StreamRequest):
    return qa_answer(query)