import os
import subprocess
from google.genai import types

def install_dependencies(working_directory: str, project_path: str):
    abs_working_directory = os.path.abspath(working_directory)
    abs_project_path = os.path.abspath(os.path.join(working_directory, project_path))
    
    if not abs_project_path.startswith(abs_working_directory):
        return f'Error: "{project_path}" is outside the working directory.'
    
    if not os.path.isdir(abs_project_path):
        return f'Error: "{project_path}" does not exist or is not a directory.'
    
    try:
        command = "npm i"
        
        result = subprocess.run(
            command,
            cwd=abs_project_path,
            capture_output=True,
            text=True,
            shell=True,
            timeout=180
        )
        
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
        return "Error: Command timed out after 180 seconds."
    except Exception as e:
        return f'Error: An error occurred while installing dependencies: {str(e)}'

schema_install_dependencies = types.FunctionDeclaration(
    name="install_dependencies",
    description="Install npm dependencies using 'npm i' in a specified project directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "project_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the project directory where dependencies should be installed, relative to the working directory."
            )
        },
        required=["project_path"]
    )
)
