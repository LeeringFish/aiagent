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

    Use the tools to find and read project files; do not ask the user for file paths.
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

    try:
        for _ in range(20):
            response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                                    contents=messages,
                                                    config=types.GenerateContentConfig(
                                                        tools=[available_functions],system_instruction=system_prompt
                                                    ),)
            
            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            function_call_parts = []

            for candidate in response.candidates:
                messages.append(candidate.content)
                for part in candidate.content.parts:
                    if getattr(part, "function_call", None):
                        function_call_parts.append(part)
            
            if response.text and not function_call_parts:
                print("\n------\n")
                print(response.text)
                break
            else:
                function_responses = []
                for part in function_call_parts:
                    result = call_function(part.function_call, verbose)
                    if not result.parts[0].function_response.response:
                        raise Exception("empty function call result")
                    
                    if verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    function_responses.append(result.parts[0])

                if not function_responses:
                    raise Exception("no function responses generated, exiting.")

                messages.append(types.Content(role="user", parts=function_responses))


    except Exception as e:
        print(f"Error: {e}")
  


if __name__ == "__main__":
    main()
