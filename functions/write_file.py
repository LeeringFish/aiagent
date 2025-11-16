import os

def write_file(working_directory, file_path, content):
    try:
        parent_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not (os.path.commonpath([parent_path, target_path]) == parent_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dir_path = os.path.dirname(target_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"