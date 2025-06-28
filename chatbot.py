import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

geminiapi_key = os.getenv("GEMINI_API_KEY")
if not geminiapi_key:
   raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=geminiapi_key)

def load_context():
   context_text = ""
   context_folder = os.path.join(os.path.dirname(__file__), "context")
   for filename in os.listdir(context_folder):
      filepath = os.path.join(context_folder, filename)
      with open(filepath, "r", encoding="utf-8") as file:
         context_text += file.read() + "\n\n"
   return context_text


meskott_context = load_context()


def get_chatbot_response(user_question: str) -> str:
   prompt = f"{meskott_context}\n\nUser: {user_question}\nAI:"
   try:
      model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
      response = model.generate_content(prompt)
      return response.text
   except Exception as e:
      return "Sorry, something went wrong. Please try again later."
  