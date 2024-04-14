from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from subprocess import Popen, PIPE

import tools

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
)

# Define your agents with roles and goals
Reporter = Agent(
    role="News Reporter",
    goal="Your goal is to find and report the latest cybersecurity news that matters",
    backstory="You live to tell the truth, site your findings, and report on what matters because you take people's time seriously",
    verbose=True,
    allow_delegation=True,
    # llm=llm,
    tools=[tools.get_past_week_data, tools.search_data, tools.search],
)

task1 = Task(
    description="Write me a report on the latest cybersecurity news",
    agent=Reporter,
    expected_output="report/essay with citations",
)


# Instantiate your crew with a sequential process
crew = Crew(
    agents=[Reporter],
    tasks=[task1],
    process=Process.sequential,
)

# Get your crew to work!
result = crew.kickoff()
print(result)
