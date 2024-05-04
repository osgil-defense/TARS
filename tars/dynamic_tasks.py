from crewai import Agent, Task, Crew, Process
from textwrap import dedent
import agents


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


def webapp_pentest_task(question, agent):
    return Task(
        description=dedent(
            f"""
Your goal as a web application penetration tester is to analyze and exploit vulnerabilities in web applications to assess their security posture. This enables organizations to address these vulnerabilities before they can be exploited maliciously. Use your expertise and available tools to respond to the following query from your employer:
<question>
{question}
<question>
"""
        ),
        agent=agent,
        expected_output=(
            "A comprehensive report detailing the findings from the web application penetration testing. "
            "Include a list of discovered vulnerabilities, categorized by severity. For each vulnerability, provide a "
            "detailed analysis, possible impacts, and specific recommendations for remediation. Ensure the report is "
            "structured to be accessible to both technical and non-technical stakeholders, emphasizing clarity and actionability."
        ),
    )
