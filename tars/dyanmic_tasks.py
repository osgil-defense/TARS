from crewai import Agent, Task, Crew, Process
from textwrap import dedent
import agents

# agents.NettackerAgent


def pentest_task(question, agent):
    return Task(
        description=dedent(
            f"""
Your goal as a penetration tester (pentester) is to identify and exploit vulnerabilities in a system or network to determine it's security weaknesses, thereby enabling the individual/organization to fix those issues to prevent actual attacks or breaches from happening. Knowing this, use your knowledge and the tools you have to answer the following question from your employer:
<question>
{question}
<question>
"""
        ),
        agent=agent,
        expected_output=(
            "A detailed report summarizing key findings from the penetration testing conducted. "
            "Include a list of identified vulnerabilities, categorized by their severity. For each vulnerability, provide a "
            "detailed description, the potential impact, and recommended remediation strategies to patch or mitigate the risks. "
            "The report should be clear, well-organized, and actionable, catering to both technical and managerial stakeholders."
        ),
    )
