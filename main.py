import customtkinter as ctk  # Import the customtkinter library for custom UI elements
from PIL import Image, ImageTk  # Import PIL for image handling
from datetime import datetime  # Import datetime for date and time operations
from tkinter import messagebox  # Import messagebox for displaying error messages
import time  # Import time module for time-related functions
import os  # Import os module for operating system related operations
import google.generativeai as genai  # Import Google's generative AI library
import threading  # Import threading for concurrent execution

# Configure the API key from environment variable
genai.configure(api_key=os.environ.get("gemini_API"))  # Set up the Gemini API with the key from environment variables

class App(ctk.CTk):  # Define the main application class
    def __init__(self):  # Initialize the application
        super().__init__()  # Call the parent class constructor
        self.title('AI Powered Student Assistant')  # Set the window title
        width = 1000  # Set the window width
        height = 600  # Set the window height
        screen_width = self.winfo_screenwidth()  # Get the screen width
        screen_height = self.winfo_screenheight()  # Get the screen height
        x = (screen_width - width) // 2  # Calculate x position for centering
        y = (screen_height - height) // 2  # Calculate y position for centering
        self.geometry(f'{width}x{height}+{x}+{y}')  # Set the window size and position
        ctk.set_appearance_mode("dark")  # Set the app appearance to dark mode
        self.configure(fg_color="#202123")  # Set the background color
        self.iconbitmap('images/app-icon.ico')  # Set the app icon

        ctk.set_widget_scaling(1.1)  # Set widget scaling
        ctk.set_window_scaling(1.1)  # Set window scaling

        self.side_frame = ctk.CTkFrame(self, width=180, fg_color="#202123")  # Create the side frame
        self.side_frame.pack(side="left", fill="y", expand=False)  # Pack the side frame
        
        self.team_frame = ctk.CTkFrame(self.side_frame, fg_color="#2A2B32", corner_radius=12)  # Create the team frame
        self.team_frame.pack(side="bottom", fill="x", padx=5, pady=5, ipady=20, ipadx=10)  # Pack the team frame
        
        team_icon = ctk.CTkImage(Image.open("images/team-icon.png"), size=(35, 35))  # Load the team icon
        team_icon_label = ctk.CTkLabel(self.team_frame, image=team_icon, text="")  # Create a label for the team icon
        team_icon_label.pack(side="left", padx=(5, 10))  # Pack the team icon label
        
        team_label = ctk.CTkLabel(self.team_frame, text="Team 5".upper(), font=("Arial", 18))  # Create a label for the team name
        team_label.pack(side="right", padx=(5, 10))  # Pack the team name label
        
        self.main_frame = ctk.CTkFrame(self, fg_color="#343541")  # Create the main frame
        self.main_frame.pack(side="right", fill="both", expand=True)  # Pack the main frame
        new_chat_icon = ctk.CTkImage(Image.open("images/new-chat-icon.png"), size=(18, 18))  # Load the new chat icon
        new_chat_button = ctk.CTkButton(self.side_frame, text="New chat", image=new_chat_icon, compound="left", fg_color="#202123", hover_color="#2A2B32", border_width=1, border_color="#565869", height=32, font=("Arial", 12))  # Create the new chat button
        new_chat_button.pack(padx=6, pady=(6, 3), fill="x")  # Pack the new chat button

        current_chat_button = ctk.CTkButton(self.side_frame, text="Faculty recommendation", fg_color="#2A2B32", hover_color="#343541", anchor="w", height=32, font=("Arial", 12))  # Create the current chat button
        current_chat_button.pack(padx=6, pady=5, fill="x")  # Pack the current chat button
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#343541")  # Create a scrollable frame
        self.scrollable_frame.pack(side="top", fill="both", expand=True, padx=15, pady=15)  # Pack the scrollable frame

        self.welcome_label = ctk.CTkLabel(self.scrollable_frame, text="Hello there! I'm here to help you find the right faculty based on your interests and strengths.", fg_color="#444654", corner_radius=8, wraplength=500, justify="left", padx=8, pady=8, font=("Arial", 12))  # Create the welcome label
        self.welcome_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")  # Pack the welcome label

        self.message_frame = ctk.CTkFrame(self.main_frame, fg_color="#343541", height=80)  # Create the message frame
        self.message_frame.pack(side="bottom", fill="x", padx=40, pady=20)  # Pack the message frame
        # self.message_frame.pack_propagate(False)  # Prevent the message frame from shrinking

        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text="Send a message", height=36, corner_radius=18, font=("Arial", 12))  # Create the message entry field
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))  # Pack the message entry field

        send_icon = ctk.CTkImage(Image.open("images/send-icon.png"), size=(22, 22))  # Load the send icon
        self.send_button = ctk.CTkButton(self.message_frame, text="", image=send_icon, width=36, height=36, corner_radius=18, command=self.send_message)  # Create the send button
        self.send_button.pack(side="right")  # Pack the send button

        self.after(800, self.show_welcome_message)  # Schedule showing the welcome message

        self.after(1600, self.show_math_results_message)  # Schedule showing the math results message

        self.questions = [  # Define the list of questions
            "What is your math results?",
            # "What are your English language results?",
            # "What are your Islamic studies results?",
            "What are your physics results?",
            "What are your biology results?",
            "What are your chemistry results?",
            # "What are your geography results?",
            # "What are your history results?",
            # "What are your Somali language results?",
            "What do you interest in?"
        ]
        self.current_question = 0  # Initialize the current question index
        self.user_answers = {}  # Initialize the dictionary to store user answers
        self.Good_At = ''  # Initialize the variable to store the subject the user is good at
        self.highest_score = 0  # Initialize the variable to store the highest score
        self.user_interest = ''  # Initialize the variable to store the user's interest

        # Create 10 different variables to hold the result of each subject
        self.math_result = 0  # Initialize math result
        self.english_result = 0  # Initialize English result
        self.islamic_studies_result = 0  # Initialize Islamic studies result
        self.physics_result = 0  # Initialize physics result
        self.biology_result = 0  # Initialize biology result
        self.chemistry_result = 0  # Initialize chemistry result
        self.geography_result = 0  # Initialize geography result
        self.history_result = 0  # Initialize history result
        self.somali_result = 0  # Initialize Somali result
        self.interest_result = ''  # Initialize interest result

    def show_welcome_message(self):  # Method to show the welcome message
        self.welcome_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")  # Pack the welcome label

    def show_math_results_message(self):  # Method to show the math results message
        self.question_label = self.create_message_label(self.questions[self.current_question], is_user=False)  # Create a label for the current question
        self.question_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")  # Pack the question label

    def send_message(self):  # Method to handle sending a message
        user_message = self.message_entry.get().strip()  # Get the user's message
        if user_message:  # If the message is not empty
            if self.current_question < len(self.questions) - 1:  # If it's not the last question
                try:
                    user_score = float(user_message)  # Try to convert the message to a float
                    self.user_answers[self.questions[self.current_question]] = user_score  # Store the user's answer
                    user_label = self.create_message_label(user_message, is_user=True)  # Create a label for the user's message
                    user_label.pack(pady=(0, 8), padx=(40, 40), anchor="e")  # Pack the user's message label
                    self.message_entry.delete(0, 'end')  # Clear the message entry
                    self.current_question += 1  # Move to the next question
                    self.after(1000, self.show_next_question)  # Schedule showing the next question
                except ValueError:  # If the input is not a valid number
                    error_message = "Please enter a valid number for your result."  # Create an error message
                    messagebox.showerror("Error", error_message)  # Show an error message box
            else:  # If it's the last question (about interest)
                self.user_interest = user_message  # Store the user's interest
                user_label = self.create_message_label(user_message, is_user=True)  # Create a label for the user's message
                user_label.pack(pady=(0, 8), padx=(40, 40), anchor="e")  # Pack the user's message label
                self.message_entry.delete(0, 'end')  # Clear the message entry
                self.calculate_good_at()  # Calculate what subject the user is good at

    def show_next_question(self):  # Method to show the next question
        new_question_label = self.create_message_label(self.questions[self.current_question], is_user=False)  # Create a label for the next question
        new_question_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")  # Pack the next question label

    def create_message_label(self, text, is_user=False):  # Method to create a message label
        return ctk.CTkLabel(self.scrollable_frame, text=text, fg_color="#444654", corner_radius=8, wraplength=500, justify="left", padx=8, pady=8, font=("Arial", 12))  # Return a new label with the given text

    def calculate_good_at(self):  # Method to calculate what subject the user is good at
        subject_scores = {  # Create a dictionary of subject scores
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
        self.Good_At = max(subject_scores, key=subject_scores.get)  # Find the subject with the highest score
        self.highest_score = subject_scores[self.Good_At]  # Store the highest score
        self.user_prompt()  # Call the user_prompt method

    def user_prompt(self):  # Method to generate and send a prompt to the AI model
        user_prompt = f"Based on the student who has {self.highest_score} in {self.Good_At} as the highest score and their expressed interest in {self.user_interest}, please recommend 5 suitable faculties or academic programs. Format your response as a numbered list from 1 to 5, without any additional explanations."  # Create the prompt for the AI
        print(user_prompt)  # Print the prompt (for debugging)
        # Create the model
        generation_config = {  # Set up the generation configuration
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 256,
        }
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config)  # Create the AI model
        
        # Display loading message
        loading_label = self.create_message_label("Loading...", is_user=False)  # Create a loading message label
        loading_label.pack(pady=(0, 8), padx=(40, 40), anchor="w")  # Pack the loading message label
        
        # Generate response in a separate thread
        def generate_response():  # Define a function to generate the AI response
            while True:
                try:
                    response = model.generate_content(user_prompt)  # Generate the AI response
                    self.after(0, lambda: self.update_response(loading_label, response.text))  # Schedule updating the response
                    print(response.text)
                    break  # Exit the loop if successful
                except Exception as e:  # If an error occurs
                    print(f"An error occurred: {str(e)}. Retrying...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
        
        threading.Thread(target=generate_response).start()  # Start a new thread to generate the response

    def update_response(self, loading_label, response_text):  # Method to update the response label
        loading_label.configure(text=response_text)  # Update the text of the loading label with the response

app = App()  # Create an instance of the App class
app.mainloop()  # Start the main event loop