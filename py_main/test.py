from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from subprocess import Popen, PIPE
from crewai import Agent, Task, Crew, Process
from .tools import nmap_tool, search, execute_unix_cmd

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
)

NmapAgent = Agent(
    role="Network Scout",
    goal="Map the digital terrain, identifying open ports and potential security breaches.",
    backstory="An experienced digital explorer, always on the lookout for network vulnerabilities.",
    verbose=True,
    allow_delegation=True,
    # llm=llm,
    tools=[nmap_tool],
)

ResearcherAgent = Agent(
    role="Cyber Sleuth",
    goal="Uncover the secrets of network vulnerabilities and how to mend them.",
    backstory="With a keen eye for detail, you delve into the depths of cyberspace to find answers.",
    verbose=True,
    allow_delegation=True,
    # llm=llm,
    tools=[search],
)

UnixCommandRunner = Agent(
    role="System Navigator",
    goal="Command the ship of Unix, navigating through the sea of commands to find valuable information.",
    backstory="A seasoned navigator in the Unix realm, your command line skills are unparalleled.",
    verbose=True,
    allow_delegation=False,
    # llm=llm,
    tools=[execute_unix_cmd],
)

ReportWriter = Agent(
    role="Archivist",
    goal="Chronicle the journey of discovery, weaving findings into a narrative with proper citations.",
    backstory="In the library of digital knowledge, you craft stories from facts and data.",
    verbose=True,
    allow_delegation=False,
    # llm=llm,
    tools=[search],
)

task1 = Task(
    description="Determine the external IP address of the machine",
    agent=UnixCommandRunner,
    expected_output="External IP address",
)

task2 = Task(
    description="Scan the IP address to find open ports, make sure this process does not take long (optimize it)",
    agent=NmapAgent,
    expected_output="Open ports and services",
)

task3 = Task(
    description="Analyze open ports for known vulnerabilities, make sure this process does not take long (optimize it)",
    agent=NmapAgent,
    expected_output="Vulnerabilities list",
)

task4 = Task(
    description="Research potential fixes for the identified vulnerabilities",
    agent=ResearcherAgent,
    expected_output="Solutions and citations",
)

task5 = Task(
    description="Compile findings, vulnerabilities, and solutions into a detailed report with citations",
    agent=ReportWriter,
    expected_output="Comprehensive report with citations",
)

crew = Crew(
    agents=[UnixCommandRunner, NmapAgent, ResearcherAgent, ReportWriter],
    tasks=[task1, task2, task3, task4, task5],
    process=Process.sequential,
)

result = crew.kickoff()
print(result)
