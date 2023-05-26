"""This is an example of how to use async langchain with fastapi and return a streaming response."""
import os
import uvicorn
from starlette.types import Send
from typing import Any, Optional, Awaitable, Callable, Iterator, Union
from fastapi import FastAPI
from langchain.schema import HumanMessage
from fastapi.responses import StreamingResponse
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import AsyncCallbackHandler,BaseCallbackHandler
from langchain.callbacks.manager import AsyncCallbackManager
from typing import Any, Dict, List
from langchain.schema import LLMResult
import asyncio
from .loader.sync import sync
Sender = Callable[[Union[str, bytes]], Awaitable[None]]


class EmptyIterator(Iterator[Union[str, bytes]]):
    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class AsyncStreamCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming, inheritance from AsyncCallbackHandler."""
    def __init__(self, send: Sender):
        super().__init__()
        self.send = send

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Rewrite on_llm_new_token to send token to client."""
        await self.send(f"data: {token}\n\n")

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when chain starts running."""
        print("zzzz....")
        await asyncio.sleep(0.3)
        class_name = serialized["name"]
        print("Hi! I just woke up. Your llm is starting")

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when chain ends running."""
        print("zzzz....")
        await asyncio.sleep(0.3)
        print("Hi! I just woke up. Your llm is ending")

class StreamCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming, inheritance from AsyncCallbackHandler."""
    def __init__(self, send: Sender):
        super().__init__()
        self.send = send

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Rewrite on_llm_new_token to send token to client."""
        sync(self.send(f"data: {token}\n\n"))

        
class ChatOpenAIStreamingResponse(StreamingResponse):
    """Streaming response for openai chat model, inheritance from StreamingResponse."""
    def __init__(
            self,
            generate: Callable[[Sender], Awaitable[None]],
            status_code: int = 200,
            media_type: Optional[str] = None,
    ) -> None:
        super().__init__(content=EmptyIterator(), status_code=status_code, media_type=media_type)
        self.generate = generate

    async def stream_response(self, send: Send) -> None:
        """Rewrite stream_response to send response to client."""
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        async def send_chunk(chunk: Union[str, bytes]):
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        # send body to client
        await self.generate(send_chunk)

        # send empty body to client to close connection
        await send({"type": "http.response.body", "body": b"", "more_body": False})


def send_message(message: str) -> Callable[[Sender], Awaitable[None]]:
    async def generate(send: Sender):
        model = ChatOpenAI(
            streaming=True,
            verbose=True,
            callback_manager=AsyncCallbackManager([AsyncStreamCallbackHandler(send)]),
        )
        await model.agenerate(messages=[[HumanMessage(content=message)]])

    return generate