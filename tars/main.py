from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from subprocess import Popen, PIPE
from crewai import Agent, Task, Crew, Process
import time
import sys
import os

sys.path.append(os.path.join(str("/".join(__file__.split("/")[:-1])), "tools"))
from tools import nettacker  # , network, scrapper

######################################################################

google_llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
)

openai_llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09")

llm = openai_llm

######################################################################


NettackerAgent = Agent(
    role="Nettacker Tool Expert",
    goal="Identify and report vulnerabilities using OWASP's Nettacker CLI tool",
    backstory="""
You are a seasoned penetration tester with expertise in the OWASP Nettacker CLI tool. Your extensive experience includes identifying vulnerabilities in diverse network infrastructures and web applications. You've contributed to cybersecurity by uncovering critical security gaps in high-profile systems, enhancing the robustness of network defenses.
""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[
        nettacker.get_nettacker_docs,
        nettacker.nettacker,
        nettacker.nettacker_profile_all,
        nettacker.nettacker_module_all,
    ],
)

task1 = Task(
    description="Perform a vulnerability assessment for the website: https://notifycyber.com/",
    agent=NettackerAgent,
    expected_output="""
A detailed report summarizing your key findings during your penetration testing of the website. Include details about what vulnerabilities you found, their severity, as well as ways those vulnerabilities could get patched/fixed.
""",
)

crew = Crew(
    agents=[NettackerAgent],
    tasks=[task1],
    process=Process.sequential,
    memory=True,
)

start_time = time.time()

result = crew.kickoff()

runtime = time.time() - start_time

print("\n=====================[REPORT]=====================\n")
print(result)
print(f"\nRUNTIME: {runtime} seconds")
