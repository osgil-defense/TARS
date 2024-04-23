from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import validators
import requests
import asyncio
import aiohttp
import time
import json
import sys
import re
import os

import util


extensions = util.read_json(os.path.join(os.getcwd(), "assets/extensions.json"))


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


def remove_consecutive_empty_strings(strings):
    cleaned_strings = [
        strings[i]
        for i in range(len(strings))
        if strings[i] != "" or (i > 0 and strings[i - 1] != "")
    ]
    return cleaned_strings


def remove_empty_start_end(my_list):
    if my_list and len(my_list) > 0 and my_list[0] == "":
        my_list.pop(0)
    if my_list and len(my_list) > 0 and my_list[-1] == "":
        my_list.pop()
    return my_list


def clean_html(content):
    # parse the HTML content
    soup = BeautifulSoup(content, "html.parser")

    # remove unwanted tags (like script, style)
    for tag in soup(["script", "style"]):
        tag.decompose()

    # convert the soup text to string, preserving inherent newlines and tabs
    text = soup.get_text()

    # normalize spaces (reduce multiple spaces to a single space)
    text = re.sub(r"[ ]+", " ", text)

    # remove leading/trailing whitespaces on each line
    text = "\n".join(line.strip() for line in text.splitlines())

    # clean up duplicated spaces
    text = text.split("\n")
    text = remove_consecutive_empty_strings(text)
    text = remove_empty_start_end(text)
    text = "\n".join(text)

    return text


def http_get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    },
    timeout=15,
):
    response = None
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code < 300:
            return response.content
    except:
        pass
    return response


def has_invalid_ext(extensions, link):
    exts = [s for sublist in extensions.values() for s in sublist]
    parsed_url = urlparse(link)
    file = os.path.basename(parsed_url.path)
    for ext in exts:
        if file.endswith(ext):
            return False
    return True


# NOTE: main function, all other functions are used here
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
