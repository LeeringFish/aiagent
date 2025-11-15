import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                              contents=messages,)
    
    if verbose:
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
