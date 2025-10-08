import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites files in the specified directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to write or overwrite the specified file from, relative to the working directory. ",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written or overwritten to the specified file"
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        root = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([root, target]) != root:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        
        with open(target, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    
    except Exception as e:
        return f"Error: {e}"


    
"""
if __name__ == "__main__":
    print(write_file("calculator", "lorem.txt", "test test test test"))  # ensure something prints
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
"""