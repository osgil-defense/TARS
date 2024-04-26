from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import sys


def prompt_route(model_name, prompt_template_params, user_input):
    # one example prompt that would be generated:
    """
    You are good at classifying a question.
    Given the user question below, classify it as either being about 'Car', 'Restaurant', or 'Technology'.

    <If the question is about car, mechanics, models, automative technolgoy, classify it as 'Car'>
    <If the question is about cuisines, dining experiences, or restaurant services, classify it as 'Restaurant'>
    <If the question is about gadgets, software, or technological trends, classify it as 'Technology'>
    <If the question does not fit any of the classifications, classify it as 'None'>

    <question>
    How do I fix a wheel?
    <question>

    Classifgication:
    """

    ChatOpenAI(model=model_name, temperature=0)

    # generate classfication listing for prompt
    main_list = "Given the user question below, classify it as either being about "
    carrot_list = ""
    i = 0
    d = prompt_template_params["options"]
    for option in d:
        main_list += f"'{option}'"
        if i != len(d) - 1:
            main_list += ", "
        else:
            main_list += "."
        tmp = ",".join(d[option][:-1] + ["or " + d[option][-1]]).replace(",", ", ")
        carrot_list += f"<If the question is about {tmp}, classify it as '{option}'>\n"
        i += 1
    carrot_list += f"<If the question does not fit any of the classifications, classify it as '{prompt_template_params['default_none']}'>"

    classification_chain = PromptTemplate.from_template(
        """You are good at classifying a question.
        {main_list}

        {carrot_list}

        <question>
        {question}
        <question>

        Classifgication:"""
    ) | ChatOpenAI()

    classification = classification_chain.invoke(
        {"question": user_input, "main_list": main_list, "carrot_list": carrot_list}
    )

    return classification.content


# main function calls
cmodel = "gpt-4-turbo-2024-04-09"
coptions = {
    "default_none": "None",
    "options": {
        "Car": ["car", "mechanics", "models", "automative technolgoy"],
        "Restaurant": ["cuisines", "dining experiences", "restaurant services"],
        "Technology": ["gadgets", "software", "technological trends"],
    },
}
cout = prompt_route(cmodel, coptions, input("PROMPT: "))
print(cout)
