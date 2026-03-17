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
from neurocode.functions.web_analysis.analyzeWebpage import analyze_webpage

from google.genai import types

working_directory = "."


def call_function(function_call_part, api_key=None):
    function_mapping = {
        "get_files_info": (get_files_info, working_directory),
        "get_file_content": (get_file_content, working_directory),
        "write_file": (write_file, working_directory),
        "run_python_file": (run_python_file, working_directory),
        "create_file": (create_file, working_directory),
        "create_react_vite_app": (create_react_vite_app, working_directory),
        "run_react_app": (run_react_app, working_directory),
        "install_dependencies": (install_dependencies, working_directory),
        "create_uv_environment": (create_uv_environment, working_directory),
        "install_python_dependencies": (install_python_dependencies, working_directory),
        "analyze_image": (analyze_image, working_directory, api_key),
        "analyze_webpage": (analyze_webpage, working_directory),
    }

    if function_call_part.name not in function_mapping:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    func_info = function_mapping[function_call_part.name]
    func = func_info[0]

    if function_call_part.name == "analyze_image":
        result = func(func_info[1], api_key=func_info[2], **function_call_part.args)
    else:
        result = func(func_info[1], **function_call_part.args)

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
