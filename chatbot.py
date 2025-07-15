import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

geminiapi_key = os.getenv("GEMINI_API_KEY")
if not geminiapi_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=geminiapi_key)

# Load static context from context/ folder
def load_context():
    context_text = ""
    context_folder = os.path.join(os.path.dirname(__file__), "context")
    for filename in os.listdir(context_folder):
        filepath = os.path.join(context_folder, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            context_text += file.read() + "\n\n"
    return context_text

meskott_context = load_context()

# Chat memory: in-memory dictionary keyed by user_id
chat_histories = {}  # user_id: list of (user_input, bot_response) tuples

def get_chatbot_response(user_question: str, user_id: str) -> str:
    prompt = f"{meskott_context}\n\n"

    history = chat_histories.get(user_id, [])
    for user, bot in history[-5:]:  # include last 5 exchanges
        prompt += f"User: {user}\nAI: {bot}\n"
    
    prompt += f"User: {user_question}\nAI:"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        response = model.generate_content(prompt)
        bot_reply = response.text

        # Save to history
        chat_histories.setdefault(user_id, []).append((user_question, bot_reply))
        return bot_reply

    except Exception as e:
        return "Sorry, something went wrong. Please try again later."

def get_chat_history(user_id: str) -> list:
    return chat_histories.get(user_id, [])