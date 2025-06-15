import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("Prompt is not provided")
        sys.exit(1)
    promt = sys.argv[1]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=promt)]),
    ]

    generate_content(client, messages)

def generate_content(client, messages):
    response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages
    )
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()