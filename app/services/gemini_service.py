import google.generativeai as genai
import os
from app.core.config import settings
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)

def gemini_response(text):
    # Eliminate the markdowns from the text
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # Remove markdown links
    text = re.sub(r'[#*`]', '', text)  # Remove markdown symbols

    # Make sure to have a limit for the token (input)
    max_tokens = 1000  # Example token limit
    if len(text) > max_tokens:
        text = text[:max_tokens]

    # Generate content
    response = model.generate_content(text)

    # Make sure to have a pagination for the output
    output = response.text
    page_size = 500  # Example page size
    pages = [output[i:i + page_size] for i in range(0, len(output), page_size)]

    return pages
