from openai import OpenAI
from dotenv import load_dotenv
import os
import argparse
from call_function import call_function, available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
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
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=available_functions,
)

if response.usage is None:
    raise RuntimeError("failed API request")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"System prompt: {system_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, args.verbose)
        if result_message["content"] is None:
            raise Exception("content is empty")
        if args.verbose:
            print(f"-> {result_message['content']}")
# else:
#     print(message.content)
