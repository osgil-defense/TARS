from langchain_community.tools import DuckDuckGoSearchRun
from subprocess import Popen, PIPE
from crewai_tools import tool
import requests


@tool("GetLocalIp")
def get_external_ip():
    """Get external ip address or provide one"""
    try:
        response = requests.get("https://api.ipify.org", timeout=15)
        return str(response.text)
    except:
        return None


@tool("DuckDuckGoSearch")
def search(query: str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(query)
