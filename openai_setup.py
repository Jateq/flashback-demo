import openai
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory, ChatMessageHistory

from main import OPENAI_TOKEN

# from transformers import AutoTokenizer
MODEL_NAME = "gpt-3.5-turbo"
# tokenizer = AutoTokenizer.from_pretrained("openai-gpt")


def setup():
    openai.api_key = OPENAI_TOKEN


class MyService:
    def __init__(self):
        self.openai_api_key = OPENAI_TOKEN
        self.llm = OpenAI(
            streaming=True,
            temperature=0.7,
            callbacks=[]  # Add your callback handlers if needed
        )
        self.memory = ConversationBufferMemory()
        self.chat_model = ChatOpenAI(
            streaming=True,
            temperature=0.7,
            callbacks=[]  # Add your callback handlers if needed
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.chat_history = ChatMessageHistory(variable_name="history")
        self.tools = [
            # Define your tools here
            # Tool(name="tool_name", func=tool_function, description="Tool description"),
        ]
        self.main_prompt_text = "Your main prompt text goes here"
        self.chat_template = "Your chat template goes here"

        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.YOUR_AGENT_TYPE,
            verbose=True
        )

    def process_request(self, input_message):
        # Process the user's input message
        response = self.agent.run(self.main_prompt_text)
        # Further process the response as needed
        return response

# Create an instance of your service
service = MyService()

# Process user input
user_input = "User's input message"
response = service.process_request(user_input)

# Print the response
print(response)


# Function to generate response using OpenAI
def generate_response(message):
    prompt = f"{message}\nAI:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    )
    return response.choices[0].text.strip()
