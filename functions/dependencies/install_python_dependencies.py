import os
import subprocess
from google.genai import types


def create_uv_environment(working_directory: str, project_path: str):
    abs_working_directory = os.path.abspath(working_directory)
    abs_project_path = os.path.abspath(os.path.join(working_directory, project_path))

    if not abs_project_path.startswith(abs_working_directory):
        return f'Error: "{project_path}" is outside the working directory.'

    if not os.path.isdir(abs_project_path):
        return f'Error: "{project_path}" does not exist or is not a directory.'

    uv_venv_path = os.path.join(abs_project_path, ".venv")

    if os.path.exists(uv_venv_path):
        return "UV environment already exists at .venv"

    try:
        command = "uv venv"

        result = subprocess.run(
            command,
            cwd=abs_project_path,
            capture_output=True,
            text=True,
            shell=True,
            timeout=120,
        )

        final_string = f"""
STDOUT: {result.stdout}
STDERR: {result.stderr}
"""

        if result.returncode != 0:
            final_string += (
                f"The command exited with a non-zero exit code: {result.returncode}"
            )

        if result.stdout == "" and result.stderr == "":
            final_string += "The command did not produce any output."

        return final_string

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 120 seconds."
    except Exception as e:
        return f"Error: An error occurred while creating UV environment: {str(e)}"


def install_python_dependencies(working_directory: str, project_path: str):
    abs_working_directory = os.path.abspath(working_directory)
    abs_project_path = os.path.abspath(os.path.join(working_directory, project_path))

    if not abs_project_path.startswith(abs_working_directory):
        return f'Error: "{project_path}" is outside the working directory.'

    if not os.path.isdir(abs_project_path):
        return f'Error: "{project_path}" does not exist or is not a directory.'

    try:
        command = (
            "uv pip install -r requirements.txt"
            if os.path.exists(os.path.join(abs_project_path, "requirements.txt"))
            else "uv pip install ."
        )

        result = subprocess.run(
            command,
            cwd=abs_project_path,
            capture_output=True,
            text=True,
            shell=True,
            timeout=180,
        )

        final_string = f"""
STDOUT: {result.stdout}
STDERR: {result.stderr}
"""

        if result.returncode != 0:
            final_string += (
                f"The command exited with a non-zero exit code: {result.returncode}"
            )

        if result.stdout == "" and result.stderr == "":
            final_string += "The command did not produce any output."

        return final_string

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 180 seconds."
    except Exception as e:
        return (
            f"Error: An error occurred while installing Python dependencies: {str(e)}"
        )


schema_create_uv_environment = types.FunctionDeclaration(
    name="create_uv_environment",
    description="Create a UV virtual environment in a specified project directory if it doesn't already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "project_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the project directory where the UV environment should be created, relative to the working directory.",
            )
        },
        required=["project_path"],
    ),
)

schema_install_python_dependencies = types.FunctionDeclaration(
    name="install_python_dependencies",
    description="Install Python dependencies using 'uv pip install' in a specified project directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "project_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the project directory where dependencies should be installed, relative to the working directory.",
            )
        },
        required=["project_path"],
    ),
)
