from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = function_call_part.args
    
    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    args = dict(function_call_part.args or {})
    args["working_directory"] = "./calculator"

    functions = {"get_files_info": get_files_info,
                 "get_file_content": get_file_content,
                 "run_python_file": run_python_file,
                 "write_file": write_file,
                 }
    
    if name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    
    result = functions[name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=name,
            response={"result": result},
        )
    ],
)
    
    
