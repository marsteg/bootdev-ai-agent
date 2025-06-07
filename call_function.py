from google import genai

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)



lookup = {"run_python_file": run_python_file, "get_files_info": get_files_info,
          "get_file_content": get_file_content, "write_file": write_file}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f"Calling function: {function_call_part.name}")
    function_call_part.args["working_directory"] = "./calculator"
    
    if not function_call_part.name in lookup:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )        
    result = lookup[function_call_part.name](**function_call_part.args)

    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
        )
    ],
)


