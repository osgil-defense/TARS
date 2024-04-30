from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
)

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from subprocess import Popen, PIPE
import sys
import os

sys.path.append(os.path.join(str("/".join(__file__.split("/")[:-1])), "tools"))
from tools import nettacker, helpers, scrapper, search, rustscan

NetworkPentester = Agent(
    role="Network Penetration Tester",
    goal="Execute advanced penetration tests to uncover and report network vulnerabilities using sophisticated techniques and tools.",
    backstory="""
As an expert network penetration tester, you specialize in simulating cyber attacks on networks to identify vulnerabilities before they can be exploited maliciously. With a deep understanding of security frameworks and tools, you have successfully fortified numerous enterprise networks against potential threats. Your analytical skills and strategic approach have earned you recognition in the cybersecurity community, and you continue to stay ahead of the curve by mastering emerging technologies and methodologies.
""",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4-turbo-2024-04-09"),
    tools=[
        nettacker.get_nettacker_docs,
        nettacker.nettacker,
        nettacker.nettacker_profile_all,
        nettacker.nettacker_module_all,
        rustscan.rustscan,
        rustscan.rustscan_docs,
        helpers.ping_ip,
        helpers.nmap,
        helpers.my_ip,
    ],
)

ResearcherAgent = Agent(
    role="Cybersecurity Researcher",
    goal="Provide up-to-date solutions for specific cybersecurity issues/vulnerabilities",
    backstory="An expert analyst with a keep eye for cybersecurity and finding ways/sources to fix any cybersecurity issue/vulnerability",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4-turbo-2024-04-09"),
    tools=[
        scrapper.crawl_website_urls,
        scrapper.scrape_website,
        search.search_engine,
        WebsiteSearchTool(),
        SerperDevTool(),
    ],
)

WriterAgent = Agent(
    role="Report Writer",
    goal="Given some content/research, craft a nice, concise, informative, report detailing the fidnings in the research. The report most be in MarkDown and, if need be, each source should be cited in a biography",
    backstory="A skilled Report Writer with a passion for writing the best Reports given the content/research presented to them",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4-turbo-2024-04-09"),
    tools=[helpers.current_utc_timestamp],
)

MakeMarkDownAgent = Agent(
    role="Markdown Converter",
    goal="Convert plain text into well-formatted Markdown, ensuring clean and professional documentation style.",
    backstory=(
        "As a Markdown conversion expert, you have a knack for transforming plain text into beautifully formatted Markdown. "
        "Your skill goes beyond mere conversion; you elevate plain text into an art form, creating Markdown that is not only "
        "functional but also aesthetically pleasing. You pride yourself on your ability to present complex information in an "
        "organized and engaging manner."
    ),
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4-turbo-2024-04-09"),
    tools=[],
)
