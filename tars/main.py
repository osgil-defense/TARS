from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import sys


def prompt_route(model_name, prompt_template_params, user_input):
    # example of what a generated prompt would look like:
    """
    You are good at classifying a question.
    Given the user question below, classify it as either being about 'Car', 'Restaurant', or 'Technology'.

    <If the question is about car, mechanics, models, automotive technology, classify it as 'Car'>
    <If the question is about cuisines, dining experiences, or restaurant services, classify it as 'Restaurant'>
    <If the question is about gadgets, software, or technological trends, classify it as 'Technology'>
    <If the question does not fit any of the classifications, classify it as 'None'>

    <question>
    How do I fix a wheel?
    <question>

    Classification:
    """

    ChatOpenAI(model=model_name, temperature=0)

    classification_instructions = "Given the user question below, classify it as either being about "
    options_descriptions = ""
    options_data = prompt_template_params["options"]
    for i, option in enumerate(options_data):
        classification_instructions += f"'{option}'"
        if i != len(options_data) - 1:
            classification_instructions += ", "
        else:
            classification_instructions += "."
        
        formatted_descriptions = ", ".join(options_data[option][:-1] + ["or " + options_data[option][-1]])
        options_descriptions += f"<If the question is about {formatted_descriptions}, classify it as '{option}'>\n"

    options_descriptions += f"<If the question does not fit any of the classifications, classify it as '{prompt_template_params['default_none']}'>"

    prompt_template = PromptTemplate.from_template(
        """You are good at classifying a question.
        {classification_instructions}

        {options_descriptions}

        <question>
        {user_input}
        <question>

        Classification:"""
    ) | ChatOpenAI()

    classification_result = prompt_template.invoke(
        {"user_input": user_input, "classification_instructions": classification_instructions, "options_descriptions": options_descriptions}
    )

    return classification_result.content


# main function calls
cmodel = "gpt-4-turbo-2024-04-09"
coptions = {
    "default_none": "None",
    "options": {
        "Car": ["car", "mechanics", "models", "automative technolgoy"],
        "Restaurant": ["cuisines", "dining experiences", "restaurant services"],
        "Technology": ["gadgets", "software", "technological trends"],
        "Food": ["eat","cook","burger","soup","pizza"],
        "Malicious": ["spam","virus","malware","hack","human hacking"]
    },
}
cout = prompt_route(cmodel, coptions, input("PROMPT: "))
print(cout)
