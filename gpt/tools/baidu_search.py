from typing import Optional, Type

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from baidusearch.baidusearch import search

class BaiduSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"

    def _run(self, query: str, engine: str = "google", gl: str = "us", hl: str = "en", run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool."""
        search_wrapper = search(query, num_results=5) 
        snippets = []
        for result in search_wrapper:
            snippets.append(result["abstract"].replace('\n',''))

        return " ".join(snippets)
    
    async def _arun(self, query: str,  engine: str = "google", gl: str = "us", hl: str = "en", run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        search_wrapper = search(query, num_results=5) 
        snippets = []
        for result in search_wrapper:
            snippets.append(result["abstract"].replace('\n',''))

        return " ".join(snippets)