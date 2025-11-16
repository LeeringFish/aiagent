import os
from config import CHAR_LIMIT

def get_file_content(working_directory, file_path):
    try:
        parent_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not (target_path == parent_path or target_path.startswith(parent_path)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_path, "r") as f:
            file_content_string = f.read(CHAR_LIMIT)
            if f.read(1) != "":
                file_content_string += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
            return file_content_string
        
    except Exception as e:
        return f"Error: {e}"