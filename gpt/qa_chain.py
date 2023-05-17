from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks.base import AsyncCallbackManager
from config import Config
from pydantic import BaseModel
from typing import Any, Awaitable, Callable
from .call_back import ChatOpenAIStreamingResponse, Sender, AsyncStreamCallbackHandler

from langchain.embeddings import OpenAIEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader

cfg = Config()

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
# Define your embedding model
embeddings_model = OpenAIEmbeddings()

from langchain.document_loaders import UnstructuredWordDocumentLoader

def get_docsearch():
    docsearch = None
    
    loader = TextLoader(cfg.docx_file)
    data = loader.load()
    
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator = "\n\n",
        chunk_size = 1200,
        chunk_overlap = 0,
        length_function = len,
    )
    # texts = text_splitter.split_text(data[0].page_content)
    texts = list(map(lambda t: t +  "\n<END>", text_splitter.split_text(data[0].page_content)))
    if cfg.memory_backend == "faiss":
        if not FAISS:
            print(
                "Error: FAISS is not installed. Please install faiss"
                " to use FAISS as a memory backend."
            )
        else:
            docsearch = FAISS.from_texts(texts, embeddings_model)
            

    if docsearch is None:
        docsearch = FAISS.from_texts(texts, embeddings_model)
      
    return docsearch

docsearch = get_docsearch()

prompt = """
you are Bilibili Qa Robot, use the following pieces of context to answer the question at the end, 
if the answer is not contained within the context below, just give a polite reply

Context:
{context}

###
Instruction:
1. In above context, and image is represented using the markdown syntax, pattern is "![caption of image](url)", image is part of answer

###
Constraints:
1. Answer in chinese
2. 回答不要遗漏文档中相关的图片，不要自己生成一个虚假的图片链接
3. Pay attention to line breaks

Question: {question}"""

PROMPT = PromptTemplate(
    template=prompt, input_variables=["context", "question"]
)

class StreamRequest(BaseModel):
    """Request body for streaming."""
    message: str
    
def qa_answer(body: StreamRequest):
    # query = "从哪里查看星计划的任务进度？"
    # docs = docsearch.similarity_search(query, k = 2)
    # chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    return ChatOpenAIStreamingResponse(send_message(body.message), media_type="text/event-stream")
    
def send_message(message: str) -> Callable[[Sender], Awaitable[None]]:
    docs = docsearch.similarity_search(message, k = 3)
    async def generate(send: Sender):
        chain = load_qa_chain(
            OpenAI(
                streaming=True, 
                callback_manager=AsyncCallbackManager([AsyncStreamCallbackHandler(send)]),
                temperature=cfg.temperature, 
                model_name=cfg.fast_llm_model, 
                max_tokens=cfg.fast_stream_max_token,
                verbose=True), 
            chain_type="stuff", prompt=PROMPT, verbose=True)
        await chain.acall({"input_documents": docs, "question": message})

    return generate