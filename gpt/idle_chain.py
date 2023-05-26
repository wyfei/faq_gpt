# from langchain.agents import Tool
# from langchain.agents import AgentType
# from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.callbacks.manager import AsyncCallbackManager
from .call_back import ChatOpenAIStreamingResponse, Sender, AsyncStreamCallbackHandler, StreamCallbackHandler
from config import Config
from typing import Any, Awaitable, Callable
# from .tools.baidu_search import BaiduSearchTool


cfg = Config()

# search = BaiduSearchTool()

# tools = [
#     Tool(
#         name = "Current Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events or the current state of the world",
#         coroutine=search.arun
#     ),
# ]

FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer in chinese to the original input question"""

def idle_ask(message: str):
    """_summary_
    闲聊
    Args:
        message (str): _description_

    Returns:
        _type_: _description_
    """
    return ChatOpenAIStreamingResponse(send_message(message), media_type="text/event-stream")


def send_message(message: str) -> Callable[[Sender], Awaitable[None]]:
    async def generate(send: Sender):
        llm=OpenAI(
            streaming=True, 
            callback_manager=AsyncCallbackManager([AsyncStreamCallbackHandler(send)]),
            temperature=cfg.temperature, 
            model_name=cfg.fast_llm_model, 
            max_tokens=cfg.fast_stream_max_token,
            verbose=True)

        # agent_chain = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs={"format_instructions" : FORMAT_INSTRUCTIONS})
        # await agent_chain.arun(input=message)
        await llm.agenerate([message])
    return generate