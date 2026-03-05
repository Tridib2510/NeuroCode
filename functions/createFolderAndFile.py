import os
from google.genai import types


def create_folder_and_file(
    working_directory, folder_path=None, file_path=None, content=""
):
    abs_working_directory = os.path.abspath(working_directory)

    result = ""

    if folder_path:
        abs_folder_path = os.path.abspath(os.path.join(working_directory, folder_path))
        if not abs_folder_path.startswith(abs_working_directory):
            return f'Error: "{folder_path}" is outside the working directory.'

        if not os.path.isdir(abs_folder_path):
            try:
                os.makedirs(abs_folder_path)
                result += f'Successfully created folder "{folder_path}".\n'
            except Exception as e:
                return f'Error: Could not create folder "{folder_path}": {str(e)}'
        else:
            result += f'Folder "{folder_path}" already exists.\n'

    if file_path:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: "{file_path}" is outside the working directory.'

        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.isdir(parent_dir):
            try:
                os.makedirs(parent_dir)
            except Exception as e:
                return f'Error: Could not create parent directories for "{file_path}": {str(e)}'

        try:
            with open(abs_file_path, "w") as f:
                f.write(content)
            result += f'Successfully created file "{file_path}".'
        except Exception as e:
            return f'Error: Could not create file "{file_path}": {str(e)}'

    return (
        result if result else "Error: Neither folder_path nor file_path was provided."
    )


schema_create_folder_and_file = types.FunctionDeclaration(
    name="create_folder_and_file",
    description="Create folders and/or files in a specified working directory. Can create both folders and files in a single call.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "folder_path": types.Schema(
                type=types.Type.STRING,
                description="Optional: The path of the folder to create, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Optional: The path of the file to create, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Optional: The content to write to the file. Defaults to empty string if not provided.",
            ),
        },
    ),
)
