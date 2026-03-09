import os
from google.genai import types  
def write_file(working_directory,file_path,content):
    abs_working_directory=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: "{file_path}" is outside the working directory.'

    parent_dir=os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        parent_dir=os.path.dirname(abs_file_path)
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f'Could not create parent dirs: {str(e)}'
        
    
    if not os.path.isfile(abs_file_path):
        pass
        parent_dir=os.path.dirname(abs_file_path)
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f'Could not create parent dirs: {str(e)}'
        
    try:
        with open(abs_file_path,'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}".'
    except Exception as e:
        return f'Error: An error occurred while writing to the file: {str(e)}'
    
schema_write_file=types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in a specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory."
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file as a string."
            )
        }
    )
)