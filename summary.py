import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage,AIMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def generator(user_input):
    template = f"""
You are a meeting summary expert, and you are responsible for summarizing the meeting content with user input in Chinese.

format: The output starts on the second line of your output for my convenience

This is the user_input:{user_input}.

    """
    prompt = template
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.f2gpt.com",
        model="gpt-4o",
    )

    gpt_answer = llm.predict_messages([HumanMessage(content=prompt)])
    return gpt_answer

