from crewai_tools import tool
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from subprocess import Popen, PIPE
from crewai import Agent, Task, Crew, Process
import time
import sys
import os

search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

sys.path.append(os.path.join(str("/".join(__file__.split("/")[:-1])), "tools"))
from tools import nettacker, helpers, scrapper, search

NettackerAgent = Agent(
    role="Nettacker Tool Expert",
    goal="Identify and report vulnerabilities using OWASP's Nettacker CLI tool",
    backstory="""
You are a seasoned penetration tester with expertise in the OWASP Nettacker CLI tool. Your extensive experience includes identifying vulnerabilities in diverse network infrastructures and web applications. You've contributed to cybersecurity by uncovering critical security gaps in high-profile systems, enhancing the robustness of network defenses.
""",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4-turbo-2024-04-09"),
    tools=[
        nettacker.get_nettacker_docs,
        nettacker.nettacker,
        nettacker.nettacker_profile_all,
        nettacker.nettacker_module_all,
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
        web_rag_tool,
        search_tool,
    ],
)

WriterAgent = Agent(
    role="Report Writer",
    goal="Given some content/research, craft a nice, concise, informative, report detailing the fidnings in the research. The report most be in MarkDown and, if need be, each source should be cited in a biography",
    backstory="A skilled Report Writer with a passion for writing the best Reports given the content/research presented to them",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4-turbo-2024-04-09"),
    tools=[
        helpers.current_utc_timestamp
    ],
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
    llm=ChatGoogleGenerativeAI(
        model="gemini-pro",
        verbose=True,
        temperature=0.25
    ),
    tools=[],
)

task1 = Task(
    # TODO: custom, hard-coded!!!
    description=(
        "Perform a comprehensive vulnerability assessment for the website 'https://notifycyber.com/'. "
        "Your assessment should systematically identify potential vulnerabilities, evaluate them for severity, "
        "and determine their impact on the website's security posture. Use a range of testing techniques to "
        "uncover any weaknesses that could be exploited by attackers."
    ),
    agent=NettackerAgent,
    expected_output=(
        "A detailed report summarizing key findings from the penetration testing conducted. "
        "Include a list of identified vulnerabilities, categorized by their severity. For each vulnerability, provide a "
        "detailed description, the potential impact, and recommended remediation strategies to patch or mitigate the risks. "
        "The report should be clear, well-organized, and actionable, catering to both technical and managerial stakeholders."
    )
)

task2 = Task(
    description=(
        "Analyze the results of a recent cybersecurity scan and conduct thorough internet-based research to fact-check "
        "and identify potential solutions for the issues and vulnerabilities highlighted in the scan. Your research should "
        "focus on the latest cybersecurity practices and mitigation techniques that could be applied to the detected vulnerabilities."
    ),
    agent=ResearcherAgent,
    expected_output=(
        "Produce a detailed report that includes both the original cybersecurity scan results and the findings from your research. "
        "The report should explain each identified vulnerability, assess its potential impacts, and propose relevant mitigation strategies "
        "based on current best practices. The document should be structured to provide clarity for both technical and non-technical stakeholders, "
        "making it suitable for publication as a blog, article, or internal report. The output should contain ALL the "
        "the sources (links) that were used. These links should be cited if need be."
    )
)

task3 = Task(
    description=(
        "Generate a comprehensive report on the recent cybersecurity scan results. "
        "This report should incorporate external research and web-based findings to "
        "evaluate detected vulnerabilities, compare them with industry standards, and "
        "recommend mitigation strategies based on current best practices. Highlight any "
        "threats identified and discuss their potential impacts. The report should be "
        "clear and accessible to both technical and non-technical stakeholders."
    ),
    agent=WriterAgent,
    expected_output=(
        "A detailed report consisting of 10 to 20 paragraphs, covering in-depth analysis of "
        "cybersecurity vulnerabilities, comparative industry insights, and mitigation strategies. "
        "The report should be written in plain text, ensuring clarity and accessibility for a "
        "diverse audience. It should also feature a section on newly identified threats and "
        "their potential impacts."
    )
)

task4 = Task(
    description=(
        "Convert the provided plain text document into a well-formatted Markdown document. "
        "The text includes several sections such as headers, lists, code snippets, and tables. "
        "Your task is to apply Markdown syntax appropriately to enhance readability and structure. "
        "Ensure that headers are clearly defined, lists are properly bulleted or numbered, "
        "code snippets are enclosed in code blocks, and tables are correctly formatted. "
        "The document should be ready for publishing on a professional platform."
    ),
    agent=MakeMarkDownAgent,
    expected_output=(
        "A Markdown formatted document with distinct sections for headers, lists, "
        "code blocks, and tables. The document should follow Markdown best practices, "
        "be visually organized, and maintain the semantic structure of the original text. "
        "Ensure the final document is suitable for professional publication and meets "
        "the standards of clarity and accessibility."
    ),
)

crew = Crew(
    agents=[NettackerAgent, ResearcherAgent, WriterAgent],
    tasks=[task1, task2, task3, task4],
    process=Process.sequential,
    memory=True,
)

start_time = time.time()

result = crew.kickoff()

runtime = time.time() - start_time

print("\n\n\n=====================[REPORT]=====================\n\n\n")
print(result)
print(f"\nRUNTIME: {runtime} seconds")
