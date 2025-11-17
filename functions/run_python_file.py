import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    parent_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not (target_path == parent_path or target_path.startswith(parent_path + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    
    try:
        completed = subprocess.run(["python", target_path, *args], cwd=parent_path,
                                    capture_output=True, text=True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    stdout = completed.stdout
    stderr = completed.stderr

    if not stdout and not stderr:
        return "No output produced."
    
    output = f"STDOUT: {stdout}STDERR: {stderr}"

    if completed.returncode != 0:
        output += f" Process exited with code {completed.returncode}"
    
    return output


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Use this when the user asks to run a Python file; execute the Python" \
                    "file at file_path and optionally pass CLI arguments args (list of strings)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),

            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional CLI arguments to pass to the script"
            ),
        },
        required=["file_path"]
    ),
)