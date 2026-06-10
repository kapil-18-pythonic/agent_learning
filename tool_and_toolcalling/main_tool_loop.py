
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

from tools import TOOLS,tools_given

messages = [{"role": "user", 
             "content": """
            /no_think what is 15*27 + 12*8 ? 
            You may call only one tool at a time.
            After each tool result, reconsider the next action.
            Do not predict tool outputs.
            """
             }]

max_iteration = 1
while max_iteration > 0:
    response = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages= messages,
        tools= tools_given,
        tool_choice= 'auto',
        temperature= 0
    )

    message = response.choices[0].message
    print(f"\n{message = }\n")

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if tool_name not in TOOLS:
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"{tool_name} tool is an UNKNOWN TOOL"
            })
            continue

        else:
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

    max_iteration -= 1