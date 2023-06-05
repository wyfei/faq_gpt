from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import AsyncCallbackManager
from config import Config
from typing import Any, Awaitable, Callable
from .call_back import ChatOpenAIStreamingResponse, Sender, AsyncStreamCallbackHandler

from langchain.embeddings import OpenAIEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from .output_parser import (
    GPTOutputParser,
    BaseGPTOutputParser,
)
from .transfer_question import TransferQuestionGPT

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
        chunk_size = 500,
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
if the answer is not contained within the context below, just give a polite reply in chinese

Context:
{context}

###
Instruction of above context:
1. image is represented using the markdown syntax, pattern is "![caption of image](url)"

###
Constraints:
1. Answer in chinese
2. Answer should include the relevant images base on caption in markdown format if any and do not create a fake image link yourself
3. Pay attention to line breaks

Question: {question}"""

PROMPT = PromptTemplate(
    template=prompt, input_variables=["context", "question"]
)
    
def qa_answer(question: str):
    # question = body.message
    # retrieval_llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    # retrieval_agent = RetrievalQuestionGPT.from_llm(retrieval_llm)
    # action = retrieval_agent.run(question=question)
    # next_step = action.name
    # print("question: {}, next_step: {}".format(question, next_step)) 
    # if next_step == 'retrieval':
    #     reply = action.args["question"]
    # transfer_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # transfer_agent = TransferQuestionGPT.from_llm(transfer_llm)
    # action = transfer_agent.run(question=question)
    # retrieval_question = action.retrieval
    # print("question: {}, retrieval: {}, similarity: {}".format(question, retrieval_question, action.similarity)) 
    # if float(action.similarity) < 0.9:
    #     question=question + retrieval_question
        
    return ChatOpenAIStreamingResponse(send_message(question), media_type="text/event-stream")
    
def send_message(message: str) -> Callable[[Sender], Awaitable[None]]:
    docs = docsearch.similarity_search(message, k = 7)
    async def generate(send: Sender):
        chain = load_qa_chain(
            ChatOpenAI(
                streaming=True, 
                callback_manager=AsyncCallbackManager([AsyncStreamCallbackHandler(send)]),
                temperature=cfg.temperature, 
                model_name=cfg.fast_llm_model, 
                max_tokens=cfg.fast_stream_max_token,
                verbose=True), 
            chain_type="stuff", prompt=PROMPT, verbose=True)
        await chain.acall({"input_documents": docs, "question": message})

    return generate