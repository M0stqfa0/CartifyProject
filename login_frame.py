from tkinter import messagebox
from utils import *

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ================== Main Frame ==================
        content_frame = ctk.CTkFrame(self, width=700, height=600)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        content_frame.pack_propagate(False)

        # ================== Frame containing all content ==================
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ================== Label & Subtitle ==================
        logo_label = ctk.CTkLabel(form_frame, text="Cartify",
                                  font=TITLE_FONT, text_color="white")
        logo_label.pack(pady=(20, 10))

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
        email = self.mail_field.get().strip()
        password = self.password_field.get().strip()
        if email == "admin@gmail.com" and password == "admin123":
            from user_home import UserHomePage
            messagebox.showinfo("Welcome", "Welcome, Admin!")
            # Clear the entry fields after login
            self.mail_field.delete(0, "end")
            self.password_field.delete(0, "end")
            self.controller.show_frame(UserHomePage)
        else:
            messagebox.showerror("Error", "Invalid credentials")
