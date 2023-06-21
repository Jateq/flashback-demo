import openai
import os
from dotenv import load_dotenv

# Construct the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')

# Load the environment variables from the .env file
load_dotenv(dotenv_path)

# Access the token from the environment variables
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
print(OPENAI_TOKEN)

# Use the token for further setup logic
# ...
