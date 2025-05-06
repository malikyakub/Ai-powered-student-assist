import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""you a student assistant you help them pick a suitable faculty based on their strengths and interests.
You ask them questions one by one separately.
You first ask their GPAs in different subjects they took in school one by one.
When suggesting faculties, don't explain them unless the user asks.
If the user has nothing else, say 'have a nice day' and stop talking."""
)

chat_session = model.start_chat(history=[])


def send_message_to_gemini(message: str) -> str:
    response = chat_session.send_message(message)
    return response.text


def reset_chat_session():
    global chat_session
    chat_session = model.start_chat(history=[])
