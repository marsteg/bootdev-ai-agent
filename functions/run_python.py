import os
import subprocess
from google import genai

def run_python_file(working_directory, file_path):
    if ".." in file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if file_path.startswith('/'):
        return 'Error: Absolute paths are not allowed.'
    if file_path is None:
        file_path = working_directory
    else:
        orig_path = file_path
        file_path = os.path.join(working_directory, file_path)

    full_directory = os.path.abspath(file_path)
    full_working_directory = os.path.abspath(working_directory)
    if not full_directory.startswith(full_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_path):
        return f'Error: File "{orig_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file.'
    
    reply = ""

    try:
        output = subprocess.run(['python3', full_directory], cwd=working_directory, timeout=30, capture_output=True)
        if output.stdout:
            reply += f'STDOUT: {output.stdout.decode()}\n'
        if output.stderr:
            reply += f'STDERR: {output.stderr.decode()}\n'
        if output.returncode != 0:
            return f'Error: executing Python file returned non-zero exit code {output.returncode}'
        
        if not reply:
            reply = 'No output produced.'
        return f'{reply}'
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python Python file in the specified directory, constrained to the working directory. The File must have a .py extension.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The Path to the Python file to execute.",
            ),
        },
    ),
)
