import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Initialize API key
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

def get_response(prompt, model_name="text-bison-001"):
    """
    Returns response from Google Generative AI for a given prompt.
    """
    model = genai.get_model(model_name)
    response = model.generate_content(prompt)
    return response.result
