import os
import subprocess
from google.genai import types

def create_react_vite_app(working_directory, project_name):
    abs_working_directory = os.path.abspath(working_directory)
    try:
        command = f"npx create-vite@latest {project_name} --template react"
        
        

        result = subprocess.run(
            command,
            cwd=abs_working_directory,
            input="\n",          # Auto-confirms any interactive prompts
            capture_output=True,
            text=True,
            shell=True,
            timeout=120
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("Return code:", result.returncode)

        if result.returncode != 0:
            return f"Error creating project: {result.stderr}"

        return f"React Vite project '{project_name}' created successfully.\n{result.stdout}"

    except subprocess.TimeoutExpired:
        return "Error: Project creation timed out after 120 seconds."

    except Exception as e:
        return f"Error: {str(e)}"

schema_create_react_vite_app = types.FunctionDeclaration(
    name="create_react_vite_app",
    description="Create a new React project using Vite in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "project_name": types.Schema(
                type=types.Type.STRING,
                description="The name of the React Vite project to create."
            )
        },
        required=["project_name"]
    )
)