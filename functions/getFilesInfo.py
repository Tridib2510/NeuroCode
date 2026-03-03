
import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = ""
    if directory is None:
        directory = working_directory
        abs_directory = os.path.abspath(os.path.join(working_directory))
    else:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: "{directory}" is outside the working directory.'

    final_response = ""
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(os.path.join(abs_directory, content))
        size = os.path.getsize(content_path)
        final_response += (
            f"- {content}: file_size={size} bytes, is_directory={is_dir}\n"
        )
    return final_response


schema_get_files_info=types.FunctionDeclaration(
    name="get_files_info",
    description="List the names, sizes, and types (file/directory) of items in a directory. Does NOT show file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
        'directory':types.Schema(
            type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, it defaults to the working directory.",
        )
        }
    )
)