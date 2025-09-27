from tkinter import messagebox
import customtkinter as ctk
import json
from PIL import Image
from theme import *
glob_current_user = {}

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ================== Main Frame ==================
        content_frame = ctk.CTkFrame(self, width=700, height=900)
        content_frame.pack(fill="x")

        # ================== Frame containing all content ==================
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ================== Label & Subtitle ==================
        logo_label = ctk.CTkLabel(form_frame, text="", image=ctk.CTkImage(dark_image=Image.open("images/CartifyLogo.png"),
                                                      size=(450, 240)), fg_color="transparent")
        logo_label.pack()

        subtitle_label = ctk.CTkLabel(form_frame, text="Sign into your account",
                                      font=SUBTITLE_FONT, text_color=TEXT_COLOR)
        subtitle_label.pack(pady=(0, 20))

        # ================== Entry Fields ==================
        self.mail_field = ctk.CTkEntry(form_frame, placeholder_text="E-Mail",
                                       font=ENTRY_FONT, width=300)
        self.mail_field.pack(pady=5)

        self.password_field = ctk.CTkEntry(form_frame, placeholder_text="Password",
                                           show="*", font=ENTRY_FONT, width=300)
        self.password_field.pack(pady=5)

        # ================== Submit Buttons ==================
        login_btn = ctk.CTkButton(form_frame, text="Login", corner_radius=32,
                                  width=250, font=BUTTON_FONT,
                                  border_width=2, command=self.login_user)
        login_btn.pack(pady=(20, 5))

        register_btn = ctk.CTkButton(form_frame, text="Create a new account", corner_radius=32,
                                     width=250, font=BUTTON_FONT,
                                     border_width=2, command=self.go_register)
        register_btn.pack(pady=5)


    # ================== Functions related to buttons ==================
    def go_register(self):
        from register_frame import RegisterFrame
        self.controller.show_frame(RegisterFrame)

    def login_user(self):
        global glob_current_user # To modify the global variable
        email = self.mail_field.get().strip()
        password = self.password_field.get().strip()

        if not email or not password:
            messagebox.showerror("Missing Field", "Please fill all fields.")
            return

        if email == "admin@gmail.com" and password == "admin123":
            from admin_home import AdminHomePage
            messagebox.showinfo("Welcome", "Welcome, Admin!")
            self.mail_field.delete(0, "end")
            self.password_field.delete(0, "end")
            self.controller.show_frame(AdminHomePage)
            return

        try:
            with open("user_data.json", "r") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []

        found_user = None
        for user in users_data:
            if user.get("email") == email:
                found_user = user
                break # Found the user, stop searching

        if found_user:
            if password == found_user.get("password"):
                from user_home import UserHomePage
                glob_current_user = found_user # Set the global user
                messagebox.showinfo("Welcome", f"Welcome, {found_user.get('name')}!")
                self.mail_field.delete(0, "end")
                self.password_field.delete(0, "end")
                self.controller.show_frame(UserHomePage)
            else:
                messagebox.showerror("Invalid Credentials", "Incorrect password.")
        else:
            messagebox.showerror("Error", "Email not found!\nPlease create an account.")
