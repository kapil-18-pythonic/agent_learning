from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tool_and_toolcalling.tools import tools_given, TOOLS, SENSITIVE_TOOLS

from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

System_prompt = """ 
    You are a reasoning agent. Before every tool call, you MUST write your 
    reasoning in the content field. Format:
    Thought: <why you are calling this tool, what you expect>
    and call toll one by one
    After receiving a tool result, think again before the next action.
    When you have enough information, provide the final answer.
    ."""

messages = [{
        "role":"system", "content":System_prompt
    },
    {
        "role":"user", "content":"what is 12*32 + 32*21 - 100? "
                                 "and then send the result to where@example.com"
    },]

state = {
    'messages':messages,
    "results":[],
    "final_answer":None,
    "pending":None
}

def build_assistant_msg(message) -> dict:
    msg = {"role": "assistant", "content": message.content}
    if message.tool_calls:
        msg["tool_calls"] = [{
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in message.tool_calls
        ]
    return msg

max_iter = 6

while max_iter > 0:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=state['messages'],
        tools=tools_given,
        tool_choice='auto',
        temperature=0
    )

    message = response.choices[0].message

    state["messages"].append(build_assistant_msg(message)) 
    print(f"\n{state['messages'] = }\n")

    if not message.tool_calls:
        state['final_answer'] = message.content
        print(f"\n{state['final_answer'] = }\n")
        break

    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if (tool_name not in TOOLS):
            state['messages'].append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: Unknown tool '{tool_name}'"
            })
            continue

        if tool_name in SENSITIVE_TOOLS:
            state["pending"] = {
                "tool_call_id": tool_call.id,
                "tool_name": tool_name,
                "arguments": arguments,
                "thought": message.content,
                "approval": "pending"
            }
            print("\n.....HUMAN APPROVAL REQUIRED.....\n")
            print(state["pending"])

            action = input(
                "\nApprove action? (y/n) : "
            ).strip().lower()

            if action == "y":
                result = TOOLS[tool_name](**arguments)

                state['messages'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

                state["results"].append({
                    "tool_id": tool_call.id,
                    "tool_name": tool_name,
                    "result": result,
                    "thought": message.content
                })

                state["pending"]["approval"] = ("approved")
                print("\nApproved and executed.\n")

            else:
                state["pending"]["approval"] = ("rejected")

                state['messages'].append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "User rejected action"
                })
                print("\nAction rejected.\n")
            continue

        result = TOOLS[tool_name](**arguments)

        state['messages'].append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        state["results"].append({
            "tool_id": tool_call.id,
            "tool_name": tool_name,
            "result": result,
            "Thought": message.content
        })

        print(state)
        print("\n")

    max_iter -= 1

if state['final_answer'] is None:
    print("Warning: max iterations reached without a final answer.")