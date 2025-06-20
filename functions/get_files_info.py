import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    # Ensure absolute paths for security
    working_directory = os.path.abspath(working_directory)
    if directory:
        directory = os.path.abspath(os.path.join(working_directory, directory))
    
    # Prevent access outside the working directory
    if not directory.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Ensure the directory exists and is valid
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    try:
        # Build directory contents string
        contents = []
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path) if not is_dir else 128  # Arbitrary size for dirs
            contents.append(f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}')
        
        return "\n".join(contents)
    
    except Exception as e:
        return f'Error: {str(e)}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)