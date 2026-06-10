from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

from tools import add, multiply

TOOLS = {
    "add": add,
    "multiply":multiply
}
math_params = {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "add two numbers",
            "parameters": math_params
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "multiply two numbers",
            "parameters": math_params
        }
    }
]

response = client.chat.completions.create(
    model="qwen/qwen3-32b",
    messages=[
        {
            "role": "user",
            "content": "/no_think What is 15 * 27?"
        }
    ],
    tools=tools,
    tool_choice="required",
    temperature=0
) 

message = response.choices[0].message
print(f"{message} it is just after first time model call")

import json

tool_call = message.tool_calls[0]
print(f"{tool_call = }")

tool_name = tool_call.function.name
print(f"{tool_name = }")

arguments = json.loads(
    tool_call.function.arguments
)
print(f"{arguments = }")

result = TOOLS[tool_name](**arguments)
print(f"{result = } before final response it is what by tools")

final_response = client.chat.completions.create(
    model="qwen/qwen3-32b",
    messages=[
        {
            "role": "user",
            "content": "/no_think What is 15 * 27?"
        },
        message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content":"/no_think" + str(result) + str("happy?")
        }
    ]
)

print(final_response.choices[0].message.content)