import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()

if len(sys.argv) < 2:
    print("Prompt is not provided")
    sys.exit(1)
promt = sys.argv[1]
print(promt)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=promt
)
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")