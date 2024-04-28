from crewai import Agent, Task, Crew, Process
import time
import sys

import routers
import tasks
import dyanmic_tasks
import agents

import config

def crewai_result_to_json(result):
    try:
        output = {"final_output": result["final_output"], "tasks_outputs": []}
        for task_output in result["tasks_outputs"]:
            output["tasks_outputs"].append(
                {
                    "description": task_output.description,
                    "summary": task_output.summary,
                    "exported_output": task_output.exported_output,
                }
            )
        return output
    except:
        return result

def call_crew(user_question):
    prompt_router = routers.prompt_route(
        config.router_model_name,
        config.router_config,
        user_question,
    )

    prompt_router = prompt_router.split(", ")
    question = user_question
    crew = None

    if "Network" in prompt_router:
        crew = Crew(
            agents=[
                agents.NettackerAgent,
                agents.ResearcherAgent,
                agents.WriterAgent,
                agents.MakeMarkDownAgent,
            ],
            tasks=[
                dyanmic_tasks.pentest_task(question, agents.NettackerAgent),
                tasks.cybersecurity_research,
                tasks.build_cybersecurity_report,
                tasks.convert_report_to_markdown,
            ],
            process=Process.sequential,
            memory=True,
            cache=True,
            full_output=True,
        )

    if crew == None:
        return None

    # run the job (crew team)
    start_time = time.time()
    result = crew.kickoff()
    runtime = time.time() - start_time

    return {
        "result": crewai_result_to_json(result),
        "runtime": {
            "runtime": runtime,
            "unit": "seconds"
        }
    }


# EXAMPLE: "Are there any vulnerabilities with my website: https://notifycyber.com/"
user_question = input("QUESTION: ")

output_filename = f"stdout_yagent_{int(time.time())}.txt"
print(f"Writing STDOUT To: {output_filename}")
call_crew_output = None
original_stdout = sys.stdout
with open(output_filename, "w") as f:
    sys.stdout = f
    call_crew(user_question)
sys.stdout = original_stdout
print(f"Finished Writing To: {output_filename}")
