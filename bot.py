import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("NEW"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="you a student assistant you help them pick a sutable facult based on theie strength and intrests, \nyou ask them one by one question separately\nyou first ask them their gps in different subjects they took in school one by one\nand when you suggesting the faculties you don't explain them until the user asks you to",
)

chat_session = model.start_chat(
  history=[
  ]
)

while True:
  ask = input('user: ')
  response = chat_session.send_message(ask)
  print(response.text)