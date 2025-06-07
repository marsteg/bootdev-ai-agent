import os
from google import genai

def get_files_info(working_directory, directory=None):
    if directory == None:
        directory = working_directory
    else:
        directory = os.path.join(working_directory, directory)
    if ".." in directory:
        return 'Error: Directory traversal is not allowed.'
    if directory.startswith('/'):
        return 'Error: Absolute paths are not allowed.'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    if not os.path.exists(directory):
        return f'Error: "{directory}" does not exist.'
    full_directory = os.path.abspath(directory)
    full_working_directory = os.path.abspath(working_directory)
    if not full_directory.startswith(full_working_directory):
        return f'Error: "{directory}" is not within the working directory "{working_directory}".'
    filestrings = []
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else '0'
        file_string = f'- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}'
        filestrings.append(file_string)

    #print('\n'.join(filestrings) if filestrings else 'No files found in the directory.')
    return '\n'.join(filestrings) if filestrings else 'No files found in the directory.'

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory. If no directory is specified, lists files in the working directory itself.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
