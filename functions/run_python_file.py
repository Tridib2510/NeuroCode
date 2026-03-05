import os
import subprocess
from dotenv import load_dotenv
from google.genai import types
import sys

def run_python_file(working_directory:str,file_path:str,args=[]):
    abs_working_directory=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: "{file_path}" is outside the working directory.'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        final_args=[sys.executable,file_path]
        #sys.executable gives the path of the Python interpreter that is currently running the script. This ensures that we are using the same Python environment to run the target script, which can help avoid issues related to different Python versions or environments.
        final_args.extend(args) #This allows us to pass additional arguments to the script if needed.
        output=subprocess.run(
            final_args,  
            text=True, #This tells Python to treat the output as text instead of bytes.         
            timeout=30, #The process is allowed to run for maximum 30 seconds.
            capture_output=True,#This tells Python to capture: stdout → normal output (print statements)
            cwd=abs_working_directory) #This sets the directory where the script will run.
        
        

        final_string= f"""
STDOUT :{output.stdout} 
STDERR :{output.stderr}
            
"""
        #STDOUT-> This is the normal output of the script, which includes anything that the script prints to the console using print statements.
#STDERR-> This is the error output of the script, which includes any error messages or exceptions that occur during the execution of the script.
# We are doing this so that when our llm runs a python file it gets the complete feedback of what the code is doing so it can improve it
        if output.returncode!=0:
            final_string+=f"The script exited with a non-zero exit code: {output.returncode}"

        if output.stdout=="" and output.stderr=="":
            final_string+="The script did not produce any output."
        return final_string
    except Exception as e:
        return f'Error: An error occurred while running the file: {str(e)}'


schema_run_python_file=types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file in a specified working directory.Accepts additional CLI args as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={ #This defines the input arguments structure.You are defining the JSON schema of the function.
            "file_path": types.Schema(
                type=types.Type.STRING, #The function expects a JSON object.
                description="The path of the Python file to run, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional array of strings to be used as CLI args for the python file",
                items=types.Schema( #This defines the type of the items in the array. In this case, we are saying that the array should contain strings.
                    type=types.Type.STRING
                )

            )
        }
    )
)