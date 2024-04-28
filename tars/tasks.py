from crewai import Agent, Task, Crew, Process
import agents

cybersecurity_research = Task(
    description=(
        "Analyze the results of a recent cybersecurity scan and conduct thorough internet-based research to fact-check "
        "and identify potential solutions for the issues and vulnerabilities highlighted in the scan. Your research should "
        "focus on the latest cybersecurity practices and mitigation techniques that could be applied to the detected vulnerabilities."
    ),
    agent=agents.ResearcherAgent,
    expected_output=(
        "Produce a detailed report that includes both the original cybersecurity scan results and the findings from your research. "
        "The report should explain each identified vulnerability, assess its potential impacts, and propose relevant mitigation strategies "
        "based on current best practices. The document should be structured to provide clarity for both technical and non-technical stakeholders, "
        "making it suitable for publication as a blog, article, or internal report. The output should contain ALL the "
        "the sources (links) that were used. These links should be cited if need be."
    ),
)

build_cybersecurity_report = Task(
    description=(
        "Generate a comprehensive report on the recent cybersecurity scan results. "
        "This report should incorporate external research and web-based findings to "
        "evaluate detected vulnerabilities, compare them with industry standards, and "
        "recommend mitigation strategies based on current best practices. Highlight any "
        "threats identified and discuss their potential impacts. The report should be "
        "clear and accessible to both technical and non-technical stakeholders."
    ),
    agent=agents.WriterAgent,
    expected_output=(
        "A detailed report consisting of 10 to 20 paragraphs, covering in-depth analysis of "
        "cybersecurity vulnerabilities, comparative industry insights, and mitigation strategies. "
        "The report should be written in plain text, ensuring clarity and accessibility for a "
        "diverse audience. It should also feature a section on newly identified threats and "
        "their potential impacts."
    ),
)

convert_report_to_markdown = Task(
    description=(
        "Convert the provided plain text document into a well-formatted Markdown document. "
        "The text includes several sections such as headers, lists, code snippets, and tables. "
        "Your task is to apply Markdown syntax appropriately to enhance readability and structure. "
        "Ensure that headers are clearly defined, lists are properly bulleted or numbered, "
        "code snippets are enclosed in code blocks, and tables are correctly formatted. "
        "The document should be ready for publishing on a professional platform."
    ),
    agent=agents.MakeMarkDownAgent,
    expected_output=(
        "A Markdown formatted document with distinct sections for headers, lists, "
        "code blocks, and tables. The document should follow Markdown best practices, "
        "be visually organized, and maintain the semantic structure of the original text. "
        "Ensure the final document is suitable for professional publication and meets "
        "the standards of clarity and accessibility."
    ),
)
