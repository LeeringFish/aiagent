import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        parent_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))

        if not (target_path == parent_path or target_path.startswith(parent_path)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for item in os.listdir(target_path):
            item_path = os.path.join(target_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)
    
    except Exception as e:
        return f"Error: {e}"


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