import os
from google.genai import types
from google import genai
from dotenv import load_dotenv
from functions.getFilesInfo import schema_get_files_info
from functions.writeIntoFile import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.getFilesContent import schema_get_files_content
from functions.createFolderAndFile import schema_create_file
from functions.createReactApp import schema_create_react_vite_app
from functions.executeFunctions import call_function
import sys
load_dotenv()
api_key=os.getenv('GEMINI_API_KEY')
client=genai.Client(api_key=api_key)

prompt=sys.argv[1]

system_prompt=(
    """
You are a helpful AI coding agent.

When a user asks for an operation, analyze the request and decide which tool to use.

Guidelines:
1. Prefer completing the entire task in the minimum number of tool calls.
2. If a tool supports performing multiple actions in one call, use that instead of making separate calls.
3. After receiving a successful tool response, do not repeat the same operation.
4. Only call tools when necessary. If the task is complete, respond to the user with a final message.
5. Never use absolute paths. All paths must be relative to the working directory.

Available capabilities:
- List files and directories
- Read file contents
- Write files
- Run Python scripts
- Create folders and files
- Create react apps
    """
)

messages=[
    types.Content(role="user",parts=[types.Part(text=prompt)])
]

available_functions=types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_files_content,
        schema_create_file,
        schema_create_react_vite_app
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

def main():

    MAX_ITER=10

    for i in range(MAX_ITER):

        response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config
        )   

        for candidate in response.candidates:
            if candidate is None or candidate.content is None:
                continue
            messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                print(f'Function name {function_call_part.name} arg are {function_call_part.args}')
                result=call_function(function_call_part,True)
                messages.append(result)
                
        else:
            print(response.text)
            return 

    



if __name__ == "__main__":
    main()
