from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

ChatOpenAI(model="gpt-4-turbo-2024-04-09", temperature=0)

classification_template = PromptTemplate.from_template(
    """You are good at classifying a question.
    Given the user question below, classify it as either being about 'Car', 'Restaurant', or 'Technology'.

    <If the question is about car, mechanics, models, automative technolgoy, classify it as 'Car'>
    <If the question is about cuisines, dining experiences, or restaurant services, classify it as 'Restaurant'>
    <If the question is about gadgets, software, or technological trends, classify it as 'Technology'>
    <If the question does not fit any of the classifications, classify it as 'None'>

    <question>
    {question}
    <question>

    Classifgication:"""
)

classification_chain = classification_template | ChatOpenAI()

classification = classification_chain.invoke({"question": str(input("PROMPT: "))})

print(classification.content)
