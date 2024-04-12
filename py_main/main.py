from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from subprocess import Popen, PIPE

import py_main.tools as tools

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
)


NPMGOD = Agent(
    role="UNIX Command Runner",
    goal="Successfully run UNIX commands in the shell and save the output",
    backstory="You are an expert UNIX Command Runner that is experienced in UNIX CLI.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[tools.execute_unix_cmd],
)

# Define your agents with roles and goals
CopyWriter = Agent(
    role="Security Analyst",
    goal="Analyze logs produced by various penetration testing tools and identify important information",
    backstory="You are an expert security analyst that identifies critical security vulnerabilites",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools=[tools.search],
)

SEO_Researcher = Agent(
    role="Security Communications Manager",
    goal="Take important security insights from security analysts and format them to make them understandable for normal adults",
    backstory="You are an expert in security communications who helps normal people understand security insights made by professionals" ,
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools=[tools.search],
)

# Define your agents with roles and goals
researcher = Agent(
    role="Penetration Testing Manager",
    goal="Utilize a penetration testing toolkit to generate useful security analytics",
    backstory="You're an expert penetration testing manager who helps their customers identify security weaknesses",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    tools=[tools.search],
)

# Create tasks for your agents
tasku = Task(
    description="acquire information on the IP",
    agent=NPMGOD,
    expected_output="IP information",
)
task1 = Task(
    description="reseach on crew ai, reference url = https://github.com/joaomdmoura/crewAI",
    agent=researcher,
    expected_output="reseach on crew ai",
)
task2 = Task(
    description=f"Create an article on langchain agents and tools and also give an example and also write a detail summary on the basis of {researcher} response",
    agent=CopyWriter,
    expected_output="an article on langchain agents and tools",
)
task3 = Task(
    description=f"give me best tags for the article written by {CopyWriter} Agent",
    agent=SEO_Researcher,
    expected_output="best tags",
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, CopyWriter, SEO_Researcher],
    tasks=[task1, task2, task3],
    verbose=2,  # Crew verbose more will let you know what tasks are being worked on, you can set it to 1 or 2 to different logging levels
    # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
    process=Process.sequential,
)

npmgod = Crew(agents=[NPMGOD], tasks=[tasku], verbose=2, process=Process.sequential)

# Get your crew to work!
result = npmgod.kickoff()
print(result)
