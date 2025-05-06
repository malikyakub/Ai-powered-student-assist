import customtkinter as ctk
from PIL import Image
from model import send_message_to_gemini, reset_chat_session
from customtkinter import StringVar
import re

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
        new_chat_button = ctk.CTkButton(self.side_frame, text="New chat", image=new_chat_icon, compound="left", fg_color="#202123", hover_color="#2A2B32", border_width=1, border_color="#565869", height=32, font=("Arial", 12), command=self.new_chat)
        new_chat_button.pack(padx=6, pady=(6, 3), fill="x")

        current_chat_button = ctk.CTkButton(self.side_frame, text="Faculty recommendation", fg_color="#2A2B32", hover_color="#343541", anchor="w", height=32, font=("Arial", 12))
        current_chat_button.pack(padx=6, pady=5, fill="x")

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#343541")
        self.scrollable_frame.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        
        self.message_frame = ctk.CTkFrame(self.main_frame, fg_color="#343541", height=80)
        self.message_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text="Send a message", height=36, corner_radius=18, font=("Arial", 12), textvariable=self.user_message)
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.message_entry.bind("<Return>", self.send_message)

        send_icon = ctk.CTkImage(Image.open("images/send-icon.png"), size=(22, 22))
        self.send_button = ctk.CTkButton(self.message_frame, text="", image=send_icon, width=36, height=36, corner_radius=18, command=self.send_message)
        self.send_button.pack(side="right")

    def send_message(self, event=None):
        user_message = self.user_message.get()
        if not user_message.strip():
            return
        self.create_user_message_label(user_message)
        self.ai_response(user_message)
        self.message_entry.delete(0, ctk.END)
        
    def create_user_message_label(self, text):
        return self._create_message_label(text, anchor="e")

    def create_ai_respose_label(self, text):
        # Split text into parts (normal text and bullet points)
        bullet_pattern = r"\*\*([^*]+)\*\*"  # matches **bold text**
        parts = re.split(r"(\*\*[^*]+\*\*)", text)

        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#444654", corner_radius=8)
        frame.pack(pady=(0, 8), padx=(40, 40), anchor="w")

        for part in parts:
            if re.match(bullet_pattern, part):
                faculty_name = re.findall(bullet_pattern, part)[0]
                label = ctk.CTkLabel(frame, text=f"• {faculty_name}", justify="left", padx=8, pady=4,
                                    font=("Arial", 12, "bold"), wraplength=350)
                label.pack(anchor="w", padx=12)
            elif part.strip():
                label = ctk.CTkLabel(frame, text=part.strip(), justify="left", padx=8, pady=4,
                                    font=("Arial", 12), wraplength=350)
                label.pack(anchor="w")

        return frame

    def _create_message_label(self, text, anchor):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#444654", corner_radius=8)
        frame.pack(pady=(0, 8), padx=(40, 40), anchor=anchor)

        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", expand=True)

        label = ctk.CTkLabel(content_frame, text=text, justify="left", padx=8, pady=10, font=("Arial", 12), wraplength=350)
        label.pack(side="left", fill="x", expand=True)

        copy_icon = ctk.CTkImage(Image.open("images/copy.png"), size=(10, 10))
        copy_button = ctk.CTkButton(content_frame, text="", image=copy_icon, width=15, height=15, fg_color="transparent", hover_color="#555", command=lambda: self.copy_to_clipboard(text))
        copy_button.pack(side="right", padx=2, pady=2)
        copy_button.pack_forget()  # initially hidden

        # Track hover state
        is_hovering = {"message": False, "button": False}

        def update_visibility():
            if is_hovering["message"] or is_hovering["button"]:
                copy_button.pack(side="right", padx=2, pady=2)
            else:
                copy_button.pack_forget()

        def on_enter_message(e):
            is_hovering["message"] = True
            update_visibility()

        def on_leave_message(e):
            is_hovering["message"] = False
            update_visibility()

        def on_enter_button(e):
            is_hovering["button"] = True
            update_visibility()

        def on_leave_button(e):
            is_hovering["button"] = False
            update_visibility()

        # Bind hover events
        frame.bind("<Enter>", on_enter_message)
        frame.bind("<Leave>", on_leave_message)
        label.bind("<Enter>", on_enter_message)
        label.bind("<Leave>", on_leave_message)
        copy_button.bind("<Enter>", on_enter_button)
        copy_button.bind("<Leave>", on_leave_button)

        return label

    def ai_response(self, user_message):
        try:
            response_text = send_message_to_gemini(user_message)
            self.create_ai_respose_label(response_text)
        except Exception as e:
            error_message = f"Error: {str(e).splitlines()[0]}"
            self.create_ai_respose_label(error_message)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def new_chat(self):
        reset_chat_session()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


app = App()
app.mainloop()
