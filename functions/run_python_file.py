import os
import subprocess

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

    if not stdout and not stderr == 0:
        return "No output produced."
    
    output = f"STDOUT: {stdout}STDERR: {stderr}"

    if completed.returncode != 0:
        output += f" Process exited with code {completed.returncode}"
    
    return output

