import os
from google.genai import types


def create_file(working_directory, file_path, content=""):
    abs_working_directory = os.path.abspath(working_directory)

    # Build absolute file path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check (prevent leaving working directory)
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: "{file_path}" is outside the working directory.'

    # Extract folder path from file_path
    parent_dir = os.path.dirname(abs_file_path)

    # Create folder(s) if they don't exist
    if not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f'Error: Could not create directories: {str(e)}'

    # Create file
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Could not create file "{file_path}": {str(e)}'

    return f'Successfully created "{file_path}".'


schema_create_file = types.FunctionDeclaration(
    name="create_file",
    description="Create a file in the working directory. If the path includes folders (e.g. calculator/cal.py), the folders will be created automatically.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to create relative to the working directory. Example: calculator/cal.py",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write inside the file.",
            ),
        },
        required=["file_path"],
    ),
)

