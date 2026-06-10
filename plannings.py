from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

from tools import TOOLS, tools_given

task = """
Plan how to solve:
What is (15*27)+(12*8)?
Return JSON format of the plan only.
"""
models = ['qwen/qwen3-32b']
for model in models:
    response = client.chat.completions.create(
        model = model,
        messages = [{"role":"user","content":task}],
        tools = tools_given,
        tool_choice= 'auto',
        temperature= 0.1
    )

    print(f"{model  =  }")
    print(response.choices[0].message)