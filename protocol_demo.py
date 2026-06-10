openai_response = {
    "tool_calls":[
        {
            "function":{
                "name":"add",
                "args":{"a": 15, "b": 27}
            }
        }
    ]
}

anthropic_response = {
    "type":"tool_use",
    "name":"add",
    "inputs":{
        "a":15,
        "b":27
    }
}

gemini_response = {
    "functionCall":{
        "name":"add",
        "args":{
            "a":15,
            "b":27
        }
    }
}

# ("add", ("a": 15, "b":27))

def parse_openai(openai_response):
    tool_calls = (openai_response["tool_calls"][0])
    tool_name = str(tool_calls['function']['name'])
    tool_args = tool_calls['function']['args']
    return (tool_name, tool_args)

def parse_anthropic(anthropic_response):
    tool_name = str(anthropic_response['name'])
    tool_args = anthropic_response['inputs']
    return (tool_name, tool_args)


def parse_gemini(gemini_response):
    tool_name = str(gemini_response['functionCall']['name'])
    tool_args = (gemini_response['functionCall']['args'])
    return (tool_name, tool_args)

print(parse_anthropic(anthropic_response), parse_openai(openai_response), parse_gemini(gemini_response))