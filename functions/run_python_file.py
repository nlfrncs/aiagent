import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the Python files with optional arguments in the specified directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to execute the specified file from, relative to the working directory. ",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The list of arguments that will be used to run the python file"
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        root = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([root, target]) != root:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'
        if not target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        func_call = subprocess.run(["python", target, *args], timeout=30, capture_output=True, text=True)

        if func_call.returncode != 0:
            return f"Process exited with code {func_call.returncode}"
        elif (func_call.stdout is None or func_call.stdout.strip() == "") and (func_call.stderr is None or func_call.stderr.strip() == ""):
            return "No output produced."
        else:
            return f"STDOUT:\n{func_call.stdout}\nSTDERR:\n{func_call.stderr}"

    except Exeption as e:
        return f"Error: executing Python file: {e}"
    
if __name__ == "__main__":
    print(run_python_file("calculator", "main.py", ["3 + 5"]))  # ensure something prints
    #print(run_python_file("calculator", "tests.py"))