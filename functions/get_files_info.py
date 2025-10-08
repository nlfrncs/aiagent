import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        result_directory = os.path.join(working_directory, directory)

        root = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, directory))
        if os.path.commonpath([root, target]) != root:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target):
            return f'Error: "{directory}" is not a directory'
            
        result = os.listdir(result_directory)
        result_list = []
        for item in result:
            try:
                result_list.append(f"- {item}: file_size={os.path.getsize(os.path.join(result_directory, item))} bytes, is_dir={os.path.isdir(os.path.join(result_directory, item))}")

            except Exception as e:
                return f"Error: {e}"
        #- README.md: file_size=1032 bytes, is_dir=False
        
        return ("\n").join(result_list)
    except Exception as e:
        return f"Error: {e}"

"""
if __name__ == "__main__":
    print(get_files_info("calculator", "pkg"))  # ensure something prints
"""