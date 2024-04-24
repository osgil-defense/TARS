from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from subprocess import Popen, PIPE
from crewai import Agent, Task, Crew, Process
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "tools"))
from tools import nettacker, network, scrapper

################################################

google_llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
)

openai_llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09")

llm = openai_llm

################################################

# NettackerAgent = Agent(
#     role="Nettacker Tool Expert",
#     goal="Deep dive into a target and find as many vulnerabilities in that target as possible just by using the OWASP's Nettacker CLI tool",
#     backstory="""
# You are a professional, senior level, penetration tester. You are an expert in the OWASP's Nettacker CLI tool, which is a modular and open-source security scanner that facilitates automated penetration testing through its command-line interface (CLI), offering a wide range of options to detect vulnerabilities in servers, web applications, and network infrastructures.
# """,
#     verbose=True,
#     allow_delegation=False,
#     llm=llm,
#     tools=[
#         nettacker.get_nettacker_docs,
#         nettacker.nettacker,
#         nettacker.nettacker_profile_all,
#         nettacker.nettacker_module_all
#     ],
# )
# task1 = Task(
#     description="Find all the vulnerabilities for the followign website: https://notifycyber.com/",
#     agent=NettackerAgent,
#     expected_output="A report of all the vulnerabilities found using Nettacker",
# )

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
    expected_output="A detailed report outlining all vulnerabilities detected by Nettacker",
)

crew = Crew(
    agents=[NettackerAgent],
    tasks=[task1],
    process=Process.sequential,
    memory=True,
)

result = crew.kickoff()

print("\n=====================\n")
print(result)
