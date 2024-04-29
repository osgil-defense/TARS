from crewai import Agent, Task, Crew, Process
import time
import json
import sys
import os

import routers
import tasks
import dynamic_tasks
import agents
import support

import config


def networkPentTester(question):
    return Crew(
        agents=[
            agents.NettackerAgent,
            agents.ResearcherAgent,
            agents.WriterAgent,
            agents.MakeMarkDownAgent,
        ],
        tasks=[
            dynamic_tasks.pentest_task(question, agents.NettackerAgent),
            tasks.cybersecurity_research,
            tasks.build_cybersecurity_report,
            tasks.convert_report_to_markdown,
        ],
        process=Process.sequential,
        memory=True,
        cache=True,
        full_output=True,
    )


def testCrew():
    return Crew(
        agents=[agents.WriterAgent],
        tasks=[tasks.build_cybersecurity_report],
        process=Process.sequential,
        memory=True,
        cache=True,
        full_output=True,
    )


# MAIN CREW ALL WITH LOGIC IF STATEMENTS
def call_crew(user_question):
    prompt_router = routers.prompt_route(
        config.router_model_name,
        config.router_config,
        user_question,
    )

    prompt_router = prompt_router.split(", ")
    question = user_question
    crew = None

    # if "Network" in prompt_router:
    #     # crew = networkPentTester(question)

    #     # TODO: remove after quick testing
    #     crew = testCrew()

    crew = testCrew()

    if crew == None:
        raise Exception(
            f"User question ({user_question}) does not aligh with a valid category"
        )

    start_time = time.time()
    result = crew.kickoff()
    runtime = time.time() - start_time

    return {
        "result": support.crewai_result_to_json(result),
        "runtime": {"runtime": runtime, "unit": "seconds"},
    }
