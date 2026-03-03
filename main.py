import os
from google.genai import types
from google import genai
from dotenv import load_dotenv
from functions.getFilesInfo import get_files_info,schema_get_files_info
import sys
load_dotenv()
api_key=os.getenv('GEMINI_API_KEY')
client=genai.Client(api_key=api_key)

prompt=sys.argv[1]



system_prompt=(
    """
Your are a helpful AI coding agent
        When user asks a question or makes a request, make a function call plan . You can perform the following operations:
        -List files and directories
        All path you provide should be relative to the working directory of the project. You should not provide any absolute path. This is a guardrail to prevent any malicious use of the function.  
    """
)

messages=[
    types.Content(role="user",parts=[types.Part(text=prompt)])
]

available_functions=types.Tool(
    function_declarations=[
        schema_get_files_info
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

def main():
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config
    )
    for candidate in response.candidates:
        print(candidate.content)



if __name__ == "__main__":
    main()
