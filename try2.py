from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from unixtool import ExecuteCommandTool
from subprocess import Popen, PIPE

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose=True,
                             temperature=0.5,
                             google_api_key="AIzaSyCq0uwbe3NodnEwRlE1SNgMTkPCiTw3lBA")


@tool('DuckDuckGoSearch')
def search(query: str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(query)


@tool('RunCommand')
def runcommand(command: str) -> str:
    """Run a UNIX Command"""
    if command is None:
        raise ValueError("Command is required")

    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f"Error executing command: {stderr.decode('utf-8')}"

    return stdout.decode('utf-8')


NPMGOD = Agent(
    role='UNIX Command Runner',
    goal='Successfully run UNIX commands in the shell and save the output',
    backstory="You are an expert UNIX Command Runner that is experienced in UNIX CLI.",
    verbose=True,
    allow_delegation=False,
    #llm=llm,
    tools=[
        runcommand
    ]
)

# Define your agents with roles and goals
CopyWriter = Agent(
    role='Copy Writer',
    goal='To write the best article',
    backstory="You're an experienced Copy writer who writes Technical articles",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[
        search
    ]
)

SEO_Researcher = Agent(
    role='SEO analyst',
    goal='To Give the best seo based analyst tags',
    backstory="You're an experienced seo analyst who Give the best seo tags",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[
        search
    ]

)
# Define your agents with roles and goals
researcher = Agent(
    role='Researcher',
    goal='You provide results on the basis of Facts and only Facts along with supported doc related URLs ,You go to the root cause and give the best possible outcomes',
    backstory="You're an ai researcher who researches on the field of  AI and have won multiple awards",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[
        search
    ]
)

# Create tasks for your agents
tasku = Task(
    description='acquire information on the IP', agent=NPMGOD, expected_output='IP information')
task1 = Task(
    description='reseach on crew ai, reference url = https://github.com/joaomdmoura/crewAI', agent=researcher, expected_output='reseach on crew ai')
task2 = Task(
    description=f'Create an article on langchain agents and tools and also give an example and also write a detail summary on the basis of {researcher} response', agent=CopyWriter, expected_output='an article on langchain agents and tools')
task3 = Task(
    description=f'give me best tags for the article written by {CopyWriter} Agent', agent=SEO_Researcher, expected_output='best tags')

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, CopyWriter, SEO_Researcher],
    tasks=[task1, task2, task3],
    verbose=2,  # Crew verbose more will let you know what tasks are being worked on, you can set it to 1 or 2 to different logging levels
    # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
    process=Process.sequential
)

npmgod = Crew(
    agents=[NPMGOD],
    tasks=[tasku],
    verbose=2,
    process=Process.sequential
)

# Get your crew to work!
result = npmgod.kickoff()
print(result)