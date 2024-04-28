from crewai import Agent, Task, Crew, Process
import time
import sys

import routers
import tasks
import dyanmic_tasks
import agents


def main(user_question):
    prompt_router = routers.prompt_route(
        "gpt-3.5-turbo-0125",
        {
            "default_none": "None",
            "options": {
                "Network": ["protocols", "ports", "encryption", "VPN"],
                "Web Application": [
                    "HTML/CSS",
                    "JavaScript",
                    "SQL injection",
                    "cross-site",
                ],
                "Wireless": ["Wi-Fi", "Bluetooth", "NFC", "security protocols"],
                "Social Engineering": [
                    "phishing",
                    "pretexting",
                    "baiting",
                    "tailgating",
                ],
                "Physical": [
                    "locks",
                    "security badges",
                    "surveillance",
                    "alarm systems",
                ],
                "Cloud": ["SaaS", "IaaS", "PaaS", "multi-tenancy"],
                "IoT": ["sensors", "smart devices", "connectivity", "home automation"],
            },
        },
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
        )

    if crew == None:
        print(f"[ERROR] (1) Question: {question}")
        print(
            f"[ERROR] (1) Message:  The inputted question's category is not supported!"
        )
        sys.exit(1)

    # TODO: this prints the final results but it needs major refining
    start_time = time.time()
    result = crew.kickoff()
    runtime = time.time() - start_time
    print("\n\n\n=====================[REPORT]=====================\n\n\n")
    print(result)
    print(f"\nRUNTIME: {runtime} seconds")


# EXAMPLE: "Are there any vulnerabilities with my website: https://notifycyber.com/"
user_question = input("QUESTION: ")

output_filename = f"stdout_yagent_{int(time.time())}.txt"
print(f"Writing STDOUT To: {output_filename}")
original_stdout = sys.stdout
with open(output_filename, "w") as f:
    sys.stdout = f
    main(user_question)
sys.stdout = original_stdout
print(f"Finished Writing To: {output_filename}")
