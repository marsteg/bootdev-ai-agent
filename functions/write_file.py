import os
from google import genai

def write_file(working_directory, file_path, content):
    if ".." in file_path:
        return 'Error: Directory traversal is not allowed.'
    if file_path.startswith('/'):
        return 'Error: Absolute paths are not allowed.'
    if file_path is None:
        file_path = working_directory
    else:
        file_path = os.path.join(working_directory, file_path)

    full_directory = os.path.abspath(file_path)
    full_working_directory = os.path.abspath(working_directory)
    if not full_directory.startswith(full_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(os.path.dirname(full_directory)):
        os.makedirs(os.path.dirname(full_directory))

    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Could not write to file "{file_path}": {str(e)}'
    
schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified directory, constrained to the working directory. If the file does not exist, it will be created.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The Path to the file to which should be written, relative to the working directory.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
