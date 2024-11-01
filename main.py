import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox
import time
import os
import google.generativeai as genai
from customtkinter import StringVar
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
  system_instruction="you a student assistant you help them pick a sutable facult based on theie strength and intrests, \nyou ask them one by one question separately\nyou first ask them their gps in different subjects they took in school one by one\nand when you suggesting the faculties you don't explain them until the user asks you to \nand if the user has nothing else you gonna help him with you stop talking just have a nice day",
)

chat_session = model.start_chat(
  history=[
  ]
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('AI Powered Student Assistant')
        width = 1000
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#202123")
        self.iconbitmap('images/app-icon.ico')

        ctk.set_widget_scaling(1.1)
        ctk.set_window_scaling(1.1)
        
        self.user_message = StringVar()

        self.side_frame = ctk.CTkFrame(self, width=180, fg_color="#202123")
        self.side_frame.pack(side="left", fill="y", expand=False)
        
        self.team_frame = ctk.CTkFrame(self.side_frame, fg_color="#2A2B32", corner_radius=12)
        self.team_frame.pack(side="bottom", fill="x", padx=5, pady=5, ipady=20, ipadx=10)
        
        team_icon = ctk.CTkImage(Image.open("images/team-icon.png"), size=(35, 35))
        team_icon_label = ctk.CTkLabel(self.team_frame, image=team_icon, text="")
        team_icon_label.pack(side="left", padx=(5, 10))
        
        team_label = ctk.CTkLabel(self.team_frame, text="Team 5".upper(), font=("Arial", 18))
        team_label.pack(side="right", padx=(5, 10))
        
        self.main_frame = ctk.CTkFrame(self, fg_color="#343541")
        self.main_frame.pack(side="right", fill="both", expand=True)
        new_chat_icon = ctk.CTkImage(Image.open("images/new-chat-icon.png"), size=(18, 18))
        new_chat_button = ctk.CTkButton(self.side_frame, text="New chat", image=new_chat_icon, compound="left", fg_color="#202123", hover_color="#2A2B32", border_width=1, border_color="#565869", height=32, font=("Arial", 12))
        new_chat_button.pack(padx=6, pady=(6, 3), fill="x")

        current_chat_button = ctk.CTkButton(self.side_frame, text="Faculty recommendation", fg_color="#2A2B32", hover_color="#343541", anchor="w", height=32, font=("Arial", 12))
        current_chat_button.pack(padx=6, pady=5, fill="x")
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#343541")
        self.scrollable_frame.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        
        self.message_frame = ctk.CTkFrame(self.main_frame, fg_color="#343541", height=80)
        self.message_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text="Send a message", height=36, corner_radius=18, font=("Arial", 12), textvariable=self.user_message)
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        send_icon = ctk.CTkImage(Image.open("images/send-icon.png"), size=(22, 22))
        self.send_button = ctk.CTkButton(self.message_frame, text="", image=send_icon, width=36, height=36, corner_radius=18, command=self.send_message)
        self.send_button.pack(side="right")

    def send_message(self):
        user_message = self.user_message.get()
        self.create_user_message_label(user_message)
        self.ai_response(user_message)
        self.message_entry.delete(0, ctk.END)
        
    def create_user_message_label(self, text):
        label = ctk.CTkLabel(self.scrollable_frame, text=text, fg_color="#444654", corner_radius=8, justify="left", padx=8, pady=10, font=("Arial", 12), wraplength=350)
        label.pack(pady=(0, 8), padx=(40, 40), anchor="e")
        return label
    
    def create_ai_respose_label(self, text):
        label = ctk.CTkLabel(self.scrollable_frame, text=text, fg_color="#444654", corner_radius=8, justify="left", padx=8, pady=10, font=("Arial", 12), wraplength=350)
        label.pack(pady=(0, 8), padx=(40, 40), anchor="w")
        return label
        
    def ai_response(self, user_message):
        response = chat_session.send_message(user_message)
        self.create_ai_respose_label(response.text)        

app = App()
app.mainloop()