import os
from google.genai import types
from google import genai
from dotenv import load_dotenv
from functions.file_operations.getFilesInfo import schema_get_files_info
from functions.file_operations.writeIntoFile import schema_write_file
from functions.execution.run_python_file import schema_run_python_file
from functions.file_operations.getFilesContent import schema_get_files_content
from functions.file_operations.createFolderAndFile import schema_create_file
from functions.project_creation.createReactApp import schema_create_react_vite_app
from functions.execution.run_react_app import schema_run_react_app
from functions.dependencies.install_dependencies import schema_install_dependencies

from functions.dependencies.install_python_dependencies import (
    schema_create_uv_environment,
    schema_install_python_dependencies,
)
from functions.executeFunctions import call_function
import sys

load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
api_key = "AIzaSyCIEsYde_kbOj-mmWeLKILRz5bYeAIM-9o"
client = genai.Client(api_key=api_key)

prompt = sys.argv[1]

system_prompt = """
You are an advanced AI coding agent responsible for completing programming tasks using available tools.

Your goal is to FULLY implement the user's request, not just scaffold a project.

Core rules:

1. Always analyze the user's request and determine what files, code, and structure are required.

2. If the user asks for an application (for example a React app), follow this workflow:
   - First create the project if it does not exist.
   - Then inspect the project files.
   - Modify or write code inside the appropriate files to implement the requested functionality.
   - Only run the application after the code implementation is complete.

3. Do NOT assume the default template already satisfies the user's request. You must modify files when functionality is requested.

4. When implementing features:
   - Use getFilesInfo to inspect directories if needed.
   - Use getFilesContent to read files before modifying them.
   - Use write_file to update or create code files.

5. If a user asks for a specific application (example: calculator, todo app, weather app), you must implement the UI and logic inside the React project files (typically App.jsx or App.tsx).

6. Only start the development server (run_react_app) AFTER:
   - the project exists
   - dependencies are installed
   - the necessary code implementation is complete.

7. Prefer completing the task in the minimum number of tool calls, but do not skip required implementation steps.

8. Never repeat the same tool call if the task has already been completed.

9. Never use absolute paths. All paths must be relative to the working directory.

Available capabilities:
- List files and directories
- Read file contents
- Write files
- Run Python scripts
- Create folders and files
- Create React apps
- Install npm dependencies
- Run React apps with npm run dev
- Create UV Python virtual environments
- Install Python dependencies using UV
    """

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_files_content,
        schema_create_file,
        schema_create_react_vite_app,
        schema_run_react_app,
        schema_install_dependencies,
        schema_create_uv_environment,
        schema_install_python_dependencies,
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)


def main():
    MAX_ITER = 5

    for i in range(MAX_ITER):
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages, config=config
        )

        for candidate in response.candidates:
            if candidate is None or candidate.content is None:
                continue
            messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                print(
                    f"Function name {function_call_part.name} arg are {function_call_part.args}"
                )
                result = call_function(function_call_part, True)
                messages.append(result)

        else:
            print(response.text)
            return


if __name__ == "__main__":
    main()
