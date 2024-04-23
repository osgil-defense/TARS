from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from crewai_tools import tool
import validators
import asyncio
import aiohttp
import json
import re
import os
import string
import json
import re


def read_json(path):
    with open(str(path)) as file:
        content = json.load(file)
    return content


extensions = read_json(os.path.join(os.getcwd(), "assets/extensions.json"))


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            content_type = response.headers.get("Content-Type", "")
            if (
                "text/html" in content_type
                or "application/xml" in content_type
                or "text/xml" in content_type
            ):
                return await response.text(), content_type
            else:
                return None, None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None


async def get_all_website_links(session, url, domain_name, visited_urls, found_links):
    if url in visited_urls:
        return
    visited_urls.add(url)

    content, content_type = await fetch(session, url)
    if content is None:
        return

    if "xml" in content_type:
        soup = BeautifulSoup(content, "xml")
    else:
        soup = BeautifulSoup(content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if parsed_href.netloc == domain_name and href not in visited_urls:
            found_links.append(href)
            await get_all_website_links(
                session, href, domain_name, visited_urls, found_links
            )


async def collect_links(starting_url):
    domain_name = urlparse(starting_url).netloc
    visited_urls = set()
    found_links = []
    async with aiohttp.ClientSession() as session:
        await get_all_website_links(
            session, starting_url, domain_name, visited_urls, found_links
        )
    return found_links


def has_invalid_ext(extensions, link):
    exts = [s for sublist in extensions.values() for s in sublist]
    parsed_url = urlparse(link)
    file = os.path.basename(parsed_url.path)
    for ext in exts:
        if file.endswith(ext):
            return False
    return True


def extract_unique_links_from_root_url(url):
    if validators.url(url) == False:
        raise Exception(f"url {url} is not a valid URL")

    parsed_url = urlparse(url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    links = asyncio.run(collect_links(root_url))
    links = list(set(links))

    link_path = []
    link_content = []
    for link in links:
        print(f"Found URL: {url}")
        if not has_invalid_ext(extensions, link):
            link_content.append(link)
            continue
        link_path.append(link)

    return list(set(link_path + link_content))


@tool("CrawlWebsiteURLs")
def crawl_website_urls(url: str) -> str:
    """
    Given a root URL, extract all the unique sub-URLs by crawling the entire site.

    Returns:
    - str: A JSON formatted string containing a list of unique URLs.
    """

    output = extract_unique_links_from_root_url(url)

    return json.dumps(output, indent=4)
