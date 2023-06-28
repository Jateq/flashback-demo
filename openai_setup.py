import os
from dotenv import load_dotenv
import openai
from langchain import (
    LLMMathChain,
    OpenAI,
    SerpAPIWrapper,
    SQLDatabase,
    SQLDatabaseChain,
)
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory


load_dotenv()

MODEL_NAME = "gpt-3.5-turbo-0613"
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
SERPAPI_TOKEN = os.getenv("SERPAPI_TOKEN")

memory = ConversationBufferMemory(memory_key="chat_history")

search = SerpAPIWrapper(serpapi_api_key=SERPAPI_TOKEN)
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world",
    ),
]

# agent_kwargs = [
#     SystemMessage(
#         "You are AI Assistant that helps a person to create his younger digital twin version. As a data you will require age that he wants to create, what was his life desire, main goal, what aspects of life you want to discuss. Don't annoy with question try to make it as fast as possible. "
#     )
# ]

llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_TOKEN)
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)


def generate_response(message):
    prompt = f"{message}\n"
    return agent_chain.run(input=prompt)
