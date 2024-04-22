from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import tool


@tool("DuckDuckGoSearch")
def search(query: str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(query)
