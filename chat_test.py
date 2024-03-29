import os
from utils.chat import chat_openai
from dotenv import load_dotenv

load_dotenv()

# Get the OpenAI API key from the environment variablexs
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the model
model = chat_openai(openai_api_key=openai_api_key)

# Use the model to generate a response
# Replace 'complete' with the correct method name
response = model.complete("Hello, OpenAI!")

# Print the response
print(response)
