import os
from google.genai import types
from google import genai
from dotenv import load_dotenv
from neurocode.functions.file_operations.getFilesInfo import schema_get_files_info
from neurocode.functions.file_operations.writeIntoFile import schema_write_file
from neurocode.functions.execution.run_python_file import schema_run_python_file
from neurocode.functions.file_operations.getFilesContent import schema_get_files_content
from neurocode.functions.file_operations.createFolderAndFile import schema_create_file
from neurocode.functions.project_creation.createReactApp import (
    schema_create_react_vite_app,
)
from neurocode.functions.execution.run_react_app import schema_run_react_app
from neurocode.functions.dependencies.install_dependencies import (
    schema_install_dependencies,
)

from neurocode.functions.dependencies.install_python_dependencies import (
    schema_create_uv_environment,
    schema_install_python_dependencies,
)
from neurocode.functions.executeFunctions import call_function
from colorama import Fore, Style, init

init(
    autoreset=True
)  # python library Colorama to automatically reset terminal colors after each print. Otherwise the same color continues, because it was never reset

print(f"\n{Fore.CYAN}{'=' * 60}")
print(f"{Fore.CYAN}  NeuroCode - AI Coding Agent")
print(f"{Fore.CYAN}{'=' * 60}\n")

print(f"{Fore.YELLOW}Enter your Gemini API Key:")
api_key = input(f"{Fore.GREEN}> {Style.BRIGHT}")

while not api_key.strip():
    print(
        f"{Fore.RED}API Key cannot be empty! Please enter a valid key.{Style.RESET_ALL}"
    )
    api_key = input(f"{Fore.GREEN}> {Style.BRIGHT}")

client = genai.Client(api_key=api_key)

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

messages = []

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


def process_request(prompt, messages):
    MAX_ITER = 10

    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

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


def main():
    while True:
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.YELLOW}Enter your prompt:")
        print(
            f"{Fore.CYAN}Type your request below and press Enter (or 'exit' to quit):{Style.RESET_ALL}"
        )
        prompt = input(f"{Fore.GREEN}> {Style.BRIGHT}")

        if prompt.strip().lower() in ["exit", "quit", "q"]: #.strip() removes extra characters from a string
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}\n")
            break

        while not prompt.strip():
            print(
                f"{Fore.RED}Prompt cannot be empty! Please enter a valid request.{Style.RESET_ALL}"
            )
            prompt = input(f"{Fore.GREEN}> {Style.BRIGHT}")

        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.GREEN}Processing your request...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}\n")

        process_request(prompt, messages)


if __name__ == "__main__":
    main()
