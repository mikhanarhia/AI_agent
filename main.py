from openai import OpenAI
from dotenv import load_dotenv
import os
import argparse






load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("no available api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


model = "openrouter/free"
messages = [
    {
        "role": "user",
        "content": args.user_prompt,
    }
]

response = client.chat.completions.create(model = model, messages = messages)
if response.usage == None:
    raise RuntimeError("failed API request")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
print(response.choices[0].message.content)
