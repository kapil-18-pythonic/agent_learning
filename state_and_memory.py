from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

from tools import TOOLS, tools_given

state = {
    'messages':[{
        "role":"user", "content":"what is 12*8 + 13*8?"
    }],
    "results":[],
    "final_answer":None,
}

max_iteration = 1

while max_iteration > 0:
    response = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages= state['messages'],
        tools= tools_given,
        tool_choice= 'auto',
        temperature= 0
    )

    message = response.choices[0].message
    print(f"\n{message = }\n")
    state['messages'].append(message.model_dump())

    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name not in TOOLS:
                state['messages'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Error: unknown tool '{tool_name}'"
                })
                continue  # skip to next tool_call

            else:
                result = TOOLS[tool_name](**arguments)
                
                state['messages'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

                state["results"].append({
                    "tool_id":tool_call.id,
                    "tool_name":tool_name,
                    "result":result
                })

                print(state)
                print("\n")

    else:
        state['final_answer'] = message.content
        break

    max_iteration -= 1

print(state['final_answer'])