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
        separator = "<END>",
        chunk_size = 300,
        chunk_overlap = 0,
        length_function = len,
    )
    texts = text_splitter.split_text(data[0].page_content)

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
Answer the question as truthfully as possible using the following context, and if the answer is not contained within the context below, say "I don't know"

Context:
{context}

###
Instruction:
1. In above context, image is represented using the markdown syntax, pattern is ![caption of image](url)
2. Line begin with "Q" is question and following line util first "<END>" is the answer of this question

Constraints:
1. Answer in chinese
2. Answer should include images if any and each image is a separate line, don't try to make up a iamge
3. Pay attention to line breaks

System: This reminds you of these events from your past:

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