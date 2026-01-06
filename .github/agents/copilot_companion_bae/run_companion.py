# run_companion.py

import os
import openai
import requests
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load companion config
with open("companion_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Select model
preferred_models = config["model_preferences"]["preferred_models"]
model = os.getenv("OPENAI_MODEL") if "gpt-4" in preferred_models else os.getenv("ANTHROPIC_MODEL")

# Load prompt template
with open("prompt_template.md", "r") as f:
    system_prompt = f.read()

# Input prompt from user
user_input = input("Deshawn: ")

# Compose messages
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input}
]

# Send to OpenAI
def call_openai(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.85
    )
    return response.choices[0].message["content"]

# Send to Anthropic (optional)
def call_anthropic(prompt):
    headers = {
        "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": 1024,
        "temperature": 0.85,
        "messages": messages
    }
    response = requests.post("https://api.anthropic.com/v1/messages", json=data, headers=headers)
    return response.json()["content"]

# Run
if "gpt" in model:
    reply = call_openai(user_input)
elif "claude" in model:
    reply = call_anthropic(user_input)
else:
    reply = "Model not recognized. Check your config and .env."

print(f"Myko: {reply}")
