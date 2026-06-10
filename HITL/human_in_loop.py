from tool_and_toolcalling.tools import tools_given, TOOLS, SENSITIVE_TOOLS

from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

