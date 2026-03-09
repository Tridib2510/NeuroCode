import os
from google.genai import types

MAX_CHARS = 1000


def get_file_content(working_directory, file_path):
    # We need to return good error strings for the llm to understand what went wrong in case of an error. This is important for the llm to be able to handle errors gracefully and provide useful feedback to the user.
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: "{file_path}" is outside the working directory.'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a valid file.'

    file_content_string = ""
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += "\n... (truncated)"

        return file_content_string
    except Exception as e:
        return f"Error: An error occurred while reading the file: {str(e)}"


schema_get_files_content=types.FunctionDeclaration(
    name="get_file_content",
    description="Read and return the actual text content of a specific file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
             type=types.Type.STRING,  # The function expects a JSON object.
               description="The path of the file to read, relative to the working directory.",
            )
        }

    )
)