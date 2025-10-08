import os
from functions.config import *
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of the file in the specified directory with the character length truncated at 'MAX_CHARS' length",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to read the specified file from, relative to the working directory. ",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):

    try:
        root = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.commonpath([root, target]) != root:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        
        if len(file_content_string) > MAX_CHARS:
            return f'{file_content_string} \n ...File "{file_path}" truncated at {MAX_CHARS} characters'
        else:
            return file_content_string
    
    except Exception as e:
        return f"Error: {e}"

"""
if __name__ == "__main__":
    print(get_file_content("calculator", "lorem.txt"))  # ensure something prints
"""