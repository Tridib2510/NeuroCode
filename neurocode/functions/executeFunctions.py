from neurocode.functions.file_operations.getFilesInfo import get_files_info
from neurocode.functions.execution.run_python_file import run_python_file
from neurocode.functions.file_operations.writeIntoFile import write_file
from neurocode.functions.file_operations.getFilesContent import get_file_content
from neurocode.functions.file_operations.createFolderAndFile import create_file
from neurocode.functions.project_creation.createReactApp import create_react_vite_app
from neurocode.functions.execution.run_react_app import run_react_app
from neurocode.functions.dependencies.install_dependencies import install_dependencies
from neurocode.functions.dependencies.install_python_dependencies import (
    create_uv_environment,
    install_python_dependencies,
)
from neurocode.functions.image_analysis.analyzeImage import analyze_image

from google.genai import types

working_directory = "."


def call_function(function_call_part, verbose=False, api_key=None):
    if verbose:
        print("Function call part", function_call_part.name)
    else:
        print("Calling function", function_call_part.name)

    result = ""

    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory, **function_call_part.args)
        # **function_call_part.args->unpacking the arguments from the function call part and passing them to the get_files_info function
    if function_call_part.name == "get_file_content":
        result = get_file_content(working_directory, **function_call_part.args)
    if function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)
    if function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)
    if function_call_part.name == "create_file":
        result = create_file(working_directory, **function_call_part.args)
    if function_call_part.name == "create_react_vite_app":
        result = create_react_vite_app(working_directory, **function_call_part.args)
    if function_call_part.name == "run_react_app":
        result = run_react_app(working_directory, **function_call_part.args)
    if function_call_part.name == "install_dependencies":
        result = install_dependencies(working_directory, **function_call_part.args)
    if function_call_part.name == "create_uv_environment":
        result = create_uv_environment(working_directory, **function_call_part.args)
    if function_call_part.name == "install_python_dependencies":
        result = install_python_dependencies(
            working_directory, **function_call_part.args
        )
    if function_call_part.name == "analyze_image":
        result = analyze_image(
            working_directory, api_key=api_key, **function_call_part.args
        )

    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name, response={"result": result}
            )
        ],
    )
