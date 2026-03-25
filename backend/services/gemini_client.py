from google import genai
import os

# Hardcoded API key as requested
GEMINI_API_KEY = ""

client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text