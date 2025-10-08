import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
#import sys
import argparse
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="user prompt")
parser.add_argument("--verbose", action="store_true", help="enable verbose output")
args = parser.parse_args()
messages = [
types.Content(role="user", parts=[types.Part(text=args.prompt)]),
]

def main():
    print("Hello from pythonaiagent!")
    i = 0
    while i < 20:
        try:
            i += 1
            result = generate_content()
            if result == None:
                continue
            else:
                print(f"User prompt: {args.prompt}")
                print(f"Answer: {result.text}")
                break

        except Exception as e:
            return f"Error: {e}"


def generate_content():

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    for entry in response.candidates:
        messages.append(entry.content)

    #print(f"responsetext: {response.text}")
    #print(f"response.function_calls: {response.function_calls}")

    if args.verbose:
        #print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for fc in response.function_calls:
            result = call_function(fc, args.verbose)
            if len(result.parts) < 1:
                raise Exception("empty parts")
            elif not result.parts[0].function_response:
                raise Exception("empty response")
            elif not isinstance(result.parts[0].function_response.response, dict):
                raise Exception("not a dict")
            else:
                print(f"-> {result.parts[0].function_response.response}")
                func_resp = types.FunctionResponse(
                    name = fc.name,
                    response = result.parts[0].function_response.response
                )
                addtl_msg = types.Content(
                    role="user",
                    parts=[types.Part(
                        function_response=func_resp
                        )
                    ]
                )
                messages.append(addtl_msg)

    elif response.text and response.function_calls == None:
        return response
        
    else:
        return None


        


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    funcs = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "run_python_file" : run_python_file,
        "write_file" : write_file,
    }

    if function_call_part.name not in funcs:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    func_args = function_call_part.args.copy()
    func_args["working_directory"] = "./calculator"
    func = funcs[function_call_part.name]
    result = func(**func_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

if __name__ == "__main__":
    main()


