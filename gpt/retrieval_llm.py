from __future__ import annotations
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from .output_parser import (
    GPTOutputParser,
    BaseGPTOutputParser,
)
from typing import List, Optional
from langchain.chat_models.base import BaseChatModel

template = """你是Bilibili的运营人员，可以回答用户关于“星计划”活动的相关问题。
星计划活动的任务包括了涨粉任务、投稿天数任务、限时任务和优质内容任务4中任务
如果用户的问题中包含播放量/天数/涨粉数/奖金之类的信息，但是没有告诉你是哪个活动，你需要先反问用户他提问的是哪个任务
其他情况下返回用户的问题

Constraints:
1. Exclusively use the commands listed in double quotes e.g. "command name"

Commands:
1. retrieval: when you need to ask more information from user. Args json schema: 
{{
    "retrieval": {{
        "question": "question", "type": "string"
    }}
}}
2. continue: when you need to answer the question continue.

<< FORMATTING >>
You should only respond in JSON format as described below 
Response Format: 
{{
    "question": the question user ask
    "thoughts": {{
        "text": "thought",
        "reasoning": "reasoning"
    }},
    "command":{{
        "name": "command name",
        "args": {{
            "arg name": "value"
        }}
    }}
    
}}

Question: {question}

Determine which next command to use, and respond using the format specified above:
"""


class RetrievalQuestionGPT:
    def __init__(
        self,
        chain: LLMChain,
        output_parser: BaseGPTOutputParser,
    ):
        self.chain = chain
        self.output_parser = output_parser
        
    @classmethod
    def from_llm(
        cls,
        llm: BaseChatModel,
        output_parser: Optional[BaseGPTOutputParser] = None,
    ) -> RetrievalQuestionGPT:
        prompt = PromptTemplate(input_variables=["question"], template=template)
        chain = LLMChain(llm=llm, prompt=prompt)
        return cls(
            chain,
            output_parser or GPTOutputParser(),
        )
        
    def run(self, question: str) -> BaseGPTOutputParser:
        # Send message to AI, get response
        assistant_reply = self.chain.run(
            question = question
        )

        # Get command name and arguments
        action = self.output_parser.parse(assistant_reply)
        return action
        