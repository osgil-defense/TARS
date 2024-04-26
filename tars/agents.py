from crewai_tools import tool
from crewai_tools import (
    FileReadTool,
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

file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

sys.path.append(os.path.join(str("/".join(__file__.split("/")[:-1])), "tools"))
from tools import nettacker, network, scrapper, search

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
    llm=ChatGoogleGenerativeAI(
        model="gemini-pro",
        verbose=True,
        temperature=0.5,
    ),
    tools=[
        file_tool
    ],
)

task1 = Task(
    # TODO: custom, hard-coded!!!
    description="Perform a vulnerability assessment for the website: https://notifycyber.com/",
    agent=NettackerAgent,
    expected_output="""
A detailed report summarizing your key findings during your penetration testing of the website. Include details about what vulnerabilities you found, their severity, as well as ways those vulnerabilities could get patched/fixed.
""",
)

task2 = Task(
    description="Given the results of a cybersecurity scan/analysis, do some research (using the internet) to figure out/fact-check possible solutions for any issues/vulnerabilities presented in the scan/analysis",
    agent=ResearcherAgent,
    expected_output="""
Text, article, blog, or a report explaing the findings from the research. This context should also include the original cybersecurity scan/analysis that was provided before researching
""",
)

task3 = Task(
    description="Generate a comprehensive report on the recent cybersecurity scan results, incorporating external research and web-based findings. The report should include an evaluation of detected vulnerabilities, comparison with industry standards, and recommended strategies for mitigation based on current best practices. Highlight any new threats identified and discuss potential impacts. Ensure the language is clear, and the findings are accessible to both technical and non-technical stakeholders",
    agent=WriterAgent,
    expected_output="""
A 10 to 20 paragraph in depth and comprehensive report written in MarkDown format
""",
)

crew = Crew(
    agents=[NettackerAgent, ResearcherAgent, WriterAgent],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    memory=True,
)

start_time = time.time()

result = crew.kickoff()

runtime = time.time() - start_time

print("\n\n\n=====================[REPORT]=====================\n\n\n")
print(result)
print(f"\nRUNTIME: {runtime} seconds")
