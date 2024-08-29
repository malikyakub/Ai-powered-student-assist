import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox
import time
import os
import google.generativeai as genai
import threading
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("gemini_API"))

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

        self.welcome_label = ctk.CTkLabel(self.scrollable_frame, text="Hello there! I'm here to help you find the right faculty based on your interests and strengths.", fg_color="#444654", corner_radius=8, wraplength=500, justify="left", padx=8, pady=8, font=("Arial", 12))
        self.welcome_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")

        self.message_frame = ctk.CTkFrame(self.main_frame, fg_color="#343541", height=80)
        self.message_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text="Send a message", height=36, corner_radius=18, font=("Arial", 12))
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        send_icon = ctk.CTkImage(Image.open("images/send-icon.png"), size=(22, 22))
        self.send_button = ctk.CTkButton(self.message_frame, text="", image=send_icon, width=36, height=36, corner_radius=18, command=self.send_message)
        self.send_button.pack(side="right")

        self.after(800, self.show_welcome_message)

        self.after(1600, self.show_math_results_message)

        self.questions = [
            "What is your math results?",
            "What are your physics results?",
            "What are your biology results?",
            "What are your chemistry results?",
            "What do you interest in?"
        ]
        self.current_question = 0
        self.user_answers = {}
        self.Good_At = ''
        self.highest_score = 0
        self.user_interest = ''

        self.math_result = 0
        self.physics_result = 0
        self.biology_result = 0
        self.chemistry_result = 0
        self.interest_result = ''

    def show_welcome_message(self):
        self.welcome_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")

    def show_math_results_message(self):
        self.question_label = self.create_message_label(self.questions[self.current_question], is_user=False)
        self.question_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")

    def send_message(self):
        user_message = self.message_entry.get().strip()
        if user_message:
            if self.current_question < len(self.questions) - 1:
                try:
                    user_score = float(user_message)
                    self.user_answers[self.questions[self.current_question]] = user_score
                    user_label = self.create_message_label(user_message, is_user=True)
                    user_label.pack(pady=(0, 8), padx=(40, 40), anchor="e")
                    self.message_entry.delete(0, 'end')
                    self.current_question += 1
                    self.after(1000, self.show_next_question)
                except ValueError:
                    error_message = "Please enter a valid number for your result."
                    messagebox.showerror("Error", error_message)
            else:
                if not user_message:
                    error_message = "Please enter your interest."
                    messagebox.showerror("Error", error_message)
                else:
                    self.user_interest = user_message
                    user_label = self.create_message_label(user_message, is_user=True)
                    user_label.pack(pady=(0, 8), padx=(40, 40), anchor="e")
                    self.message_entry.delete(0, 'end')
                    self.calculate_good_at()

    def show_next_question(self):
        new_question_label = self.create_message_label(self.questions[self.current_question], is_user=False)
        new_question_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")

    def create_message_label(self, text, is_user=False):
        return ctk.CTkLabel(self.scrollable_frame, text=text, fg_color="#444654", corner_radius=8, wraplength=500, justify="left", padx=8, pady=8, font=("Arial", 12))

    def calculate_good_at(self):
        subject_scores = {
            "Math": self.user_answers.get("What is your math results?", 0),
            "English": self.user_answers.get("What are your English language results?", 0),
            "Islamic Studies": self.user_answers.get("What are your Islamic studies results?", 0),
            "Physics": self.user_answers.get("What are your physics results?", 0),
            "Biology": self.user_answers.get("What are your biology results?", 0),
            "Chemistry": self.user_answers.get("What are your chemistry results?", 0),
            "Geography": self.user_answers.get("What are your geography results?", 0),
            "History": self.user_answers.get("What are your history results?", 0),
            "Somali": self.user_answers.get("What are your Somali language results?", 0)
        }
        self.Good_At = max(subject_scores, key=subject_scores.get)
        self.highest_score = subject_scores[self.Good_At]
        self.user_prompt()

    def user_prompt(self):
        user_prompt = f"Based on the student who has {self.highest_score} in {self.Good_At} as the highest score and their expressed interest in {self.user_interest}, please recommend 5 suitable faculties or academic programs. Format your response as a numbered list from 1 to 5, without any additional explanations."
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 256,
        }
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config)
        
        loading_label = self.create_message_label("Loading...", is_user=False)
        loading_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")
        
        def generate_response():
            while True:
                try:
                    response = model.generate_content(user_prompt)
                    self.after(0, lambda: self.update_response(loading_label, response.text))
                    break
                except Exception as e:
                    error_message = f"Error: {str(e)} \n \nSuggestion: Wait for 2 seconds then try again"
                    self.after(0, lambda: loading_label.configure(text=error_message))
                    time.sleep(2)
        
        threading.Thread(target=generate_response).start()

    def update_response(self, loading_label, response_text):
        loading_label.configure(text=response_text)

app = App()
app.mainloop()