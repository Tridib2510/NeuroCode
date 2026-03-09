import os
import subprocess
from google.genai import types

def run_react_app(working_directory: str, project_path: str):
    abs_working_directory = os.path.abspath(working_directory)
    abs_project_path = os.path.abspath(os.path.join(working_directory, project_path))
    
    if not abs_project_path.startswith(abs_working_directory):
        return f'Error: "{project_path}" is outside the working directory.'
    
    if not os.path.isdir(abs_project_path):
        return f'Error: "{project_path}" does not exist or is not a directory.'
    
    try:
        command = "npm run dev"
        
        process=subprocess.Popen(
        command,
        cwd=abs_project_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True
    )

        result = ""

        for line in process.stdout:
            result += line
            if "http://" in line or "localhost" in line:
                return f"React server started:\n{line}"

        
        final_string = f"""
STDOUT: {result.stdout}
STDERR: {result.stderr}
"""
        
        if result.returncode != 0:
            final_string += f"The command exited with a non-zero exit code: {result.returncode}"
        
        if result.stdout == "" and result.stderr == "":
            final_string += "The command did not produce any output."
        
        return final_string
        
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds."
    except Exception as e:
        return f'Error: An error occurred while running the React app: {str(e)}'

schema_run_react_app = types.FunctionDeclaration(
    name="run_react_app",
    description="Run a React development server with 'npm run dev' in a specified project directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "project_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the React project directory, relative to the working directory."
            )
        },
        required=["project_path"]
    )
)
