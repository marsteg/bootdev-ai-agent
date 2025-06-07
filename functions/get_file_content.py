import os
from google import genai

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    if ".." in file_path:
        return 'Error: Directory traversal is not allowed.'
    if file_path.startswith('/'):
        return 'Error: Absolute paths are not allowed.'
    if file_path is None:
        file_path = working_directory
    else:
        file_path = os.path.join(working_directory, file_path)

    if not os.path.exists(file_path):
        return f'Error: "{file_path}" does not exist.'
    full_directory = os.path.abspath(file_path)
    full_working_directory = os.path.abspath(working_directory)
    if not full_directory.startswith(full_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    

    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    if len(file_content_string) == MAX_CHARS:
        file_content_string += f'... File "{file_path}" truncated at 10000 characters'

    return file_content_string

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file in the specified directory, constrained to the working directory. Content is limited to 10,000 characters.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file to retreive the content from, relative to the working directory.",
            ),
        },
    ),
)   
    