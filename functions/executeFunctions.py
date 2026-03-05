from functions.getFilesInfo import get_files_info
from functions.run_python_file import run_python_file
from functions.writeIntoFile import write_file
from functions.run_python_file import run_python_file

from google.genai import types
working_directory="."

def call_function(function_call_part,verbose=False):
    if verbose:
        print("Function call part",function_call_part.name)
    else:
        print("Calling function",function_call_part.name)
    
    result=""
   
    if function_call_part.name == "get_files_info":
       result= get_files_info(working_directory,**function_call_part.args)
        #**function_call_part.args->unpacking the arguments from the function call part and passing them to the get_files_info function
    if function_call_part.name == "get_file_content":
       result= get_files_info(working_directory,**function_call_part.args)
    if function_call_part.name == "write_file":
       result= write_file(working_directory,**function_call_part.args)
    if function_call_part.name == "run_python_file":
       result= run_python_file(working_directory,**function_call_part.args)

    if result=="":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error":f"Unknown function: {function_call_part.name}"}
                )
            ]
        )    
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={'result':result}
            )
        ],
    )