from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

from tools import TOOLS

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

messages = [{"role": "user", 
             "content": """
            /no_think what is 15*27 + 12*8 ? 
            You may call only one tool at a time.
            After each tool result, reconsider the next action.
            Do not predict tool outputs.
            """
             }]
while True:
    response = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages= messages,
        tools= tools,
        tool_choice= 'auto',
        temperature= 0
    )

    message = response.choices[0].message
    print(f"\n{message = }\n")

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        result = TOOLS[tool_name](**arguments)
        print(f"\n{tool_name = } {arguments = } {result = }\n")

        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

    else:
        print(f"\n{message}")
        break