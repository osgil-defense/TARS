from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from crewai_tools import tool
import validators
import asyncio
import aiohttp
import string
import json
import os
import signal
import time
import json
import re
import math

# 3rd party packages
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import tiktoken

################################################################################################################


def read_json(path):
    with open(str(path)) as file:
        content = json.load(file)
    return content


extensions = read_json(
    os.path.join(str("/".join(__file__.split("/")[:-1])), "assets/extensions.json")
)


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


################################################################################################################


def remove_html(content):
    oline = content
    soup = BeautifulSoup(oline, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    tmp = " ".join(soup.stripped_strings)
    tmp = "".join(filter(lambda x: x in set(string.printable), tmp))
    tmp = re.sub(" +", " ", tmp)
    return tmp


class TimeoutException(Exception):
    pass


def timeout(seconds=10, error_message="function call timed out"):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # disable the alarm
            return result

        return wrapper

    return decorator


@timeout(seconds=60)
def scrape_html(url, time_delay=10):
    options = webdriver.ChromeOptions()

    # NOTE: this was added to work in a container
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    try:
        driver.get(url)

        # wait for page to load
        time.sleep(time_delay)

        return driver.page_source
    finally:
        driver.quit()


def tokens_counter(model_name: str, string: str) -> int:
    encoding_name = tiktoken.encoding_for_model(model_name)
    encoding = tiktoken.get_encoding(encoding_name.name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def trim_end(text, model_name, max_size, p, rs=10):
    new_text = str(text)
    current_token_size = tokens_counter(model_name, text)

    while current_token_size > max_size and len(new_text) >= rs:
        tokens = new_text.split()
        rs = min(rs, math.ceil(len(tokens) / 2))
        last_token = tokens[-rs]
        new_text = new_text[
            : -(len(last_token) + 1)
        ]  # +1 to remove the space before last_token
        current_token_size = tokens_counter(model_name, new_text)
        rs = int(abs(max_size - current_token_size) * p)
        rs = max(1, rs)

        # print("{}() - [ Current Token Size: {} | Text Length: {} | RS Value: {} ]".format(trim_end.__name__, current_token_size, len(new_text), rs))

    percentage = len(new_text) / len(text)

    return new_text, percentage


################################################################################################################


@tool("ScrapeWebsite")
def scrape_website(
    url: str, token_limit: int = 120_000, model: str = "gpt-4-turbo"
) -> str:
    """
    Scrape content from the specified URL, remove HTML tags, and limit the output based on token count.

    Parameters:
    - url (str): The URL of the website to scrape.
    - token_limit (int): The maximum number of tokens allowed in the output. Default is 1096.
    - model (str): The model used for counting tokens. Default is "gpt-4".

    Returns:
    - str: The scraped website content, cleaned of HTML and truncated to the token limit if necessary.
    """
    content = remove_html(scrape_html(url))
    tokens = tokens_counter(model, content)
    if tokens > token_limit:
        new_prompt, percentage = trim_end(content, model, token_limit, 0.5, 10)
        print(f"Trimmed scrape for {url} by {(1 - percentage) * 100}%")
        return new_prompt
    return content


@tool("CrawlWebsiteURLs")
def crawl_website_urls(url: str) -> str:
    """
    Given a root URL, extract all the unique sub-URLs by crawling the entire site.

    Returns:
    - str: A JSON formatted string containing a list of unique URLs.
    """

    output = extract_unique_links_from_root_url(url)

    return json.dumps(output, indent=4)
