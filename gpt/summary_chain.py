from .loader.bilibili_loader import Bilibili_loader
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks.manager import AsyncCallbackManager, BaseCallbackManager
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
import logging
import sys
from config import Config
from typing import Awaitable, Callable, List
from .call_back import ChatOpenAIStreamingResponse, Sender, AsyncStreamCallbackHandler, StreamCallbackHandler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
logger = logging.getLogger(__name__)

cfg = Config()

map_prompt_template = """Write a concise summary of the following:

{text}

CONCISE SUMMARY IN CHINESE:"""

reduce_prompt_template = """Write a detailed summary of the following:

{text}

DETAILED SUMMARY IN CHINESE:"""


MAP_PROMPT = PromptTemplate(
    template=map_prompt_template, input_variables=["text"]
)

REDUCE_PROMPT = PromptTemplate(
    template=reduce_prompt_template, input_variables=["text"]
)

def summary_bilibili_video(url: str):
    """使用LLM对视频内容做一个summary"""
    
    loader = Bilibili_loader(url=url, sessdata=cfg.sess_data, bili_jct=cfg.bili_jct, buvid3=cfg.buvid3)
    video_info = loader.load()
    raw_transcript = (
        f"Video Title: {video_info.title},"
        f"description: {video_info.desc}"
        f"category: {video_info.tname}\n\n"
        f"Transcript: {video_info.transcript}"
    )
    context_token_count = get_token_count(raw_transcript)
    print(context_token_count)
    # prompt_token_count = get_token_count(prompt)
    # token_count = context_token_count + prompt_token_count
    # if token_count > 4096:
    #     logger.debug("🚧 Exceeded token limit, truncating context")
    #     token_delta = 4096 - prompt_token_count
    #     raw_transcript = raw_transcript[:token_delta]
    
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator = " ",
        chunk_size = 3800,
        chunk_overlap = 0,
        length_function = get_token_count,
    )

    docs = list(map(lambda t: Document(page_content=t), text_splitter.split_text(raw_transcript)))
    return ChatOpenAIStreamingResponse(send_message(docs), media_type="text/event-stream")

def send_message(docs: List[Document]) -> Callable[[Sender], Awaitable[None]]:
    async def generate(send: Sender):
        base_llm = ChatOpenAI(
            temperature=cfg.temperature, 
            model_name=cfg.fast_llm_model, 
            max_tokens=cfg.fast_stream_max_token)
        reduce_llm = ChatOpenAI(
            streaming=True, 
            callback_manager=BaseCallbackManager([StreamCallbackHandler(send)]),
            temperature=cfg.temperature, 
            model_name=cfg.fast_llm_model, 
            max_tokens=cfg.fast_stream_max_token,
            verbose=True)
        chain = load_summarize_chain(
            llm = base_llm, 
            reduce_llm = reduce_llm,
            chain_type="map_reduce", 
            return_intermediate_steps=False, 
            map_prompt=MAP_PROMPT, 
            combine_prompt=REDUCE_PROMPT, 
            verbose=True)
        await chain.acall({"input_documents": docs}, return_only_outputs=True)

    return generate

def get_token_count(text: str):
    if not text:
        return 0
    return OpenAI().get_num_tokens(text=text)
