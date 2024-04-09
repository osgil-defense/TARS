import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    convert_system_message_to_human=True,
    verbose=True,
    temperature=0.1,
)

search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  llm=llm,
  tools=[search_tool]
)

writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True,
  llm=llm,
)

# Create tasks for your agents
task1 = Task(
    description=(
        "Conduct a comprehensive analysis of the latest advancements in AI in 2024."
        "Identify key trends, breakthrough technologies, and potential industry impacts."
        "Compile your findings in a detailed report."
        "Make sure to check with a human if the draft is good before finalizing your answer."
    ),
    expected_output="A comprehensive full report on the latest AI advancements in 2024, leave nothing out",
    agent=researcher,
)

task2 = Task(
    description=(
        "Using the insights from the researcher's report, develop an engaging blog post that highlights the most significant AI advancements."
        "Your post should be informative yet accessible, catering to a tech-savvy audience."
        "Aim for a narrative that captures the essence of these breakthroughs and their implications for the future."
    ),
    expected_output="A compelling 3 paragraphs blog post formatted as markdown about the latest AI advancements in 2024",
    agent=writer,
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)

