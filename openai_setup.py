import openai

# from transformers import AutoTokenizer


MODEL_NAME = "gpt-3.5-turbo"
# tokenizer = AutoTokenizer.from_pretrained("openai-gpt")


def setup(OPENAI_TOKEN):
    openai.api_key = OPENAI_TOKEN
    # openai.ChatCompletion.create(
    #     model=MODEL_NAME,
    #     role="system",
    #     content="""
    #     You are assistant that creates a digital twin of a user, so later he can chat with hes past version and then you will connect user with his digital twin and act like twin
    #     """,
    #     messages="Let's start creating twin"
    # )


# Function to generate response using OpenAI
def generate_response(message):
    prompt = f"The following is a conversation with an AI assistant that helps to create a digital twin. The assistant is helpful, creative, clever, friendly, and connects humans with their digital twin that they can chat with.\n\nHuman: {message}\nAI:"
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
