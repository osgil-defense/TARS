from bs4 import BeautifulSoup
from crewai_tools import tool
import requests
import string
import json
import re


def remove_html(content):
    oline = content
    soup = BeautifulSoup(oline, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    tmp = " ".join(soup.stripped_strings)
    tmp = "".join(filter(lambda x: x in set(string.printable), tmp))
    tmp = re.sub(" +", " ", tmp)
    return tmp


@tool("GetTopTenOWASPList")
def grab_owasp_top_ten_list() -> str:
    url = "https://raw.githubusercontent.com/OWASP/www-project-top-ten/master/index.md"

    response = requests.get(url)
    content = response.text

    urls = []
    for line in re.split(r"[() ]+", content):
        if "https" in line:
            urls.append(line)

    url_data = {}
    for url in urls:
        tmp = requests.get(url)
        tmp = tmp.text
        tmp = remove_html(tmp)
        url_data[str(url)] = tmp

    return json.dumps({"home_page": content, "links": url_data}, indent=4)
