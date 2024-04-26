import json
import os
import string
import re

from langchain_community.tools import BraveSearch
from bs4 import BeautifulSoup
from crewai_tools import tool


def remove_html(content):
    oline = content
    soup = BeautifulSoup(oline, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    tmp = " ".join(soup.stripped_strings)
    tmp = "".join(filter(lambda x: x in set(string.printable), tmp))
    tmp = re.sub(" +", " ", tmp)
    return tmp


brave_tool = BraveSearch.from_api_key(
    api_key=os.getenv("BRAVE_API_KEY"), search_kwargs={"count": 10}
)


@tool("SearchEngine")
def search_engine(query: str) -> str:
    """
    Search-Engine tool for browsing the web and getting urls, titles, and website snippets

    Parameters:
    - query (str): Query that will be sent to the search engine

    Returns:
    - str: The search result from the query containing the "Title", "Link", and "Snippet" for each search result
    """

    response = json.loads(brave_tool.run(query))

    output = ""
    for entry in response:
        output += f"TITLE:   {entry.get('title')}\n"
        output += f"LINK:    {entry.get('link')}\n"
        output += f"SNIPPET: {remove_html(entry.get('snippet'))}\n"
        output += "\n\n"

    return output[:-4]
