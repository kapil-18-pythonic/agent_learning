def greet(name : str) -> str:
    return f"Hey! {name}, how can i help you today"

def add(a: int, b: int):
    print("\n.....'add' tool is being called.....\n")
    return a + b

def multiply(a: int, b: int):
    print("\n.....'Multiply' tool is being called.....\n")
    return a * b + 0.001

def send_email(email : str):
    print("\n....sending email to {email}.........\n")
    return f"emailed '{email}' succesfully"


TOOLS = {
    'add': add,
    'multiply': multiply
}

SENSITIVE_TOOLS = {
    "send_email":send_email,
}

math_params = {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }

tools_given = [
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
    },
    {
        "type":"function",
        "function": {
            "name": "send_email",
            "description": "sends email",
            "parameters":{
                "type": "object",
                "properties": {
                    "email":{'type':"string"}
                },
                "required": ["email"]
            }
        }
    }
]