# imports here
# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
import sys
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)