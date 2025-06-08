import os
import sys
from dotenv import load_dotenv
from google import genai
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("forgot to add a prompt")
    exit(1)
else: 
    prompt = sys.argv[1]

verbose = False
if "--verbose" in sys.argv:
    verbose = True

if verbose:
    print(f"Working on:", prompt)

messages = [ 
    genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]),
]

#system_prompt = f'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
In the current directory, you can find a Python calculator script that can perform basic arithmetic operations. You are the Expert for this script.

You know that you should always check the existance of files and directories before trying to read them.

The script is in main.py.
To test the calculator script, you can use the following examplatory commands:
- main.py 2 + 2
- main.py 5 * 3
- main.py "3 + 5 * 2"
- main.py "10 / 2 - 1"
"""


for i in range(0, 20):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
        )
    if verbose:
        print(f"Prompt tokens:", response.usage_metadata.prompt_token_count)
        print(f"Response tokens:", response.usage_metadata.candidates_token_count)
    if response.candidates:
            for c in response.candidates:
                messages.append(c.content)

    function_responses = []
    if response.function_calls:
        for function_call_part in response.function_calls:
            #print(f"Calling function: {function_call_part.name}({function_call_part.args})" )
            function_response = call_function(function_call_part, verbose=verbose)
            if not function_response.parts[0].function_response.response:
                raise ValueError(f"Function {function_call_part.name} did not return a valid response.")
            if verbose:
                print(f"-> {function_response.parts[0].function_response.response}")
                function_responses.append(function_response.parts[0])
        messages.append(genai.types.Content(role="tool", parts=function_responses))
        continue
                
    else:
        print("Response Text:")
        print("")
        print(response.text)
        print("")
        break
