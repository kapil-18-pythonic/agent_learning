from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()


from tool_and_toolcalling.tools import TOOLS, tools_given
## ----------------------Prompt Based ReAct-------------------------

System_prompt = """ 
    You must follow this format exactly:
        Thought: <your reasoning>
        Action: <tool_name>(<args>)

    When done:
        Thought: <reasoning>
        Answer: <final answer>"

    Then you parse "Action:" lines, execute them, append "Observation: <result>", loop."""

message = [{
        "role":"system", "content":System_prompt
    },
    {
        "role":"user", "content":"what is 12*32 + 32*21 - 100?"
    },]


# response = client.chat.completions.create(
#         model = "llama-3.3-70b-versatile",
#         messages = message,
#         temperature= 0.3
#     )

# print(response.choices[0].message.content.strip())

System_prompt = """ 
    You are a reasoning agent. Before every tool call, you MUST write your 
    reasoning in the content field. Format:
    Thought: <why you are calling this tool, what you expect>

    After receiving a tool result, think again before the next action.
    When you have enough information, provide the final answer."""

messages = [{
        "role":"system", "content":System_prompt
    },
    {
        "role":"user", "content":"what is 12*32 + 32*21 - 100?"
    },]

state = {
    'messages':messages,
    "results":[],
    "final_answer":None,
}

max_iter = 2

while max_iter > 0:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=state['messages'],
        tools=tools_given,
        tool_choice='auto',
        temperature=0
    )

    message = response.choices[0].message
    print(f"\n{message.content = }\n")

    state['messages'].append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name not in TOOLS:
                state['messages'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Error: unknown tool '{tool_name}'",
                })
                continue

            result = TOOLS[tool_name](**arguments)
            state['messages'].append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })
            state["results"].append({
                "tool_id": tool_call.id,
                "tool_name": tool_name,
                "result": result,
                "Thought": message.content
            })
            print(state)
    else:
        state['final_answer'] = message.content  # FIX #1
        print(f"\n{state['final_answer'] = }")
        break

    max_iter -= 1  # FIX #2

if state['final_answer'] is None:
    print("Warning: max iterations reached without a final answer.")