import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

def main():
    verbose = False
    args = sys.argv[:]
    if "--verbose" in args:
        verbose = True
        args = [arg for arg in args if arg != "--verbose"]
    
    if len(args) != 2:
        print('Error: No prompt provided. Example: uv run main.py "Explain binary search"')
        sys.exit(1)
    
    user_prompt = " ".join(args[1:])
    system_prompt = system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],system_instruction=system_prompt
                                              ),)
    
    if response.function_calls is not None:
        for call in response.function_calls:
            result = call_function(call)
            if not result.parts[0].function_response.response:
                raise Exception
            elif verbose:
                print(f"-> {result.parts[0].function_response.response}")
    else:
        if verbose:
            print(f"User prompt: {response.text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print(response.text)
  


if __name__ == "__main__":
    main()
