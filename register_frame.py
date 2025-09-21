from tkinter import messagebox
import customtkinter as ctk
import json
from theme import *

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ================== Main Frame ==================
        content_frame = ctk.CTkFrame(self, width=700, height=600)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        content_frame.pack_propagate(False)

        # ================== Frame containing all content ==================
        inner_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ================== Logo & Subtitle ==================
        logo_label = ctk.CTkLabel(inner_frame, text="Cartify",
                                  font=TITLE_FONT, text_color=TEXT_COLOR)
        logo_label.pack(pady=(20, 10), fill="x")

        subtitle_label = ctk.CTkLabel(inner_frame, text="Create a new account",
                                      font=SUBTITLE_FONT, text_color=TEXT_COLOR)
        subtitle_label.pack(pady=(0, 20), fill="x")

        # ========================= NAME =========================
        self.name_field = ctk.CTkEntry(inner_frame, placeholder_text="Name",
                                       font=ENTRY_FONT, width=300)
        self.name_field.pack(pady=5)

        # ========================= PHONE NUMBER =========================
        self.phone_num_field = ctk.CTkEntry(inner_frame, placeholder_text="Phone Number",
                                            font=ENTRY_FONT, width=300)
        self.phone_num_field.pack(pady=5)

        # ========================= EMAIL =========================
        self.mail_field = ctk.CTkEntry(inner_frame, placeholder_text="E-Mail",
                                       font=ENTRY_FONT, width=300)
        self.mail_field.pack(pady=5)

        # ========================= GENDER =========================
        self.gender_field = ctk.CTkComboBox(inner_frame, values=["Gender", "Male", "Female", "Prefer not to say"],
                                            font=ENTRY_FONT, width=300)
        self.gender_field.pack(pady=5)

        # ========================= GOVERNORATE =========================
        self.governorate_field = ctk.CTkComboBox(inner_frame, font=ENTRY_FONT, width=300,
                                                 values=['Governorate', 'Dakahlia', 'Red Sea', 'Beheira', 'Faiyum',
                                                         'Gharbia', 'Alexandria', 'Ismailia', 'Giza',
                                                         'Monufia', 'Minya', 'Cairo', 'Qalyubia',
                                                         'New Valley', 'Suez', 'Aswan', 'Assiut',
                                                         'Beni Suef', 'Port Said', 'Damietta',
                                                         'Sharqia', 'South Sinai', 'Kafr El Sheikh',
                                                         'Matruh', 'Luxor', 'Qena', 'North Sinai', 'Sohag'])
        self.governorate_field.pack(pady=5)

        # ========================= PASSWORD =========================
        self.password_field = ctk.CTkEntry(inner_frame, placeholder_text="Password",
                                           show="*", font=ENTRY_FONT, width=300)
        self.password_field.pack(pady=5)

        # ========================= AGE =========================
        self.age_field = ctk.CTkEntry(inner_frame, placeholder_text="Age",
                                      font=ENTRY_FONT, width=300)
        self.age_field.pack(pady=5)

        # ========================= NATIONAL ID =========================
        self.national_field = ctk.CTkEntry(inner_frame, placeholder_text="National ID",
                                           font=ENTRY_FONT, width=300)
        self.national_field.pack(pady=5)

        # ========================= REGISTER BUTTON =========================
        register_btn = ctk.CTkButton(inner_frame, text="Register", corner_radius=32, width=250, font=BUTTON_FONT,
                                     border_width=2, command=self.register_user)
        register_btn.pack(pady=(20, 5))

        # ========================= LOGIN BUTTON =========================
        login_btn = ctk.CTkButton(inner_frame, text="Back to Login", corner_radius=32, width=250, font=BUTTON_FONT,
                                  border_width=2, command=self.go_login)
        login_btn.pack(pady=5)


    # ================== Functions related to buttons ==================
    def go_login(self):
        from login_frame import LoginFrame
        self.controller.show_frame(LoginFrame)

    def register_user(self):
        name = self.name_field.get()
        phone = self.phone_num_field.get()
        email = self.mail_field.get()
        password = self.password_field.get()
        gender = self.gender_field.get()
        governorate = self.governorate_field.get()
        age = self.age_field.get()
        national_id = self.national_field.get()

        if not name or not phone or not email or not password or gender == "Gender" or governorate == "Governorate":
            messagebox.showerror("Missing Field", "Please fill all fields.")
            return

        new_user ={ "email": email,
                    "password": password,
                    "name": name,
                    "phone": phone,
                    "gender": gender,
                    "governorate": governorate,
                    "age": age,
                    "national_id": national_id}

        with open("user_data.json", "r") as f:
            users_data = json.load(f)

        users_data.append(new_user)

        with open("user_data.json", "w") as f:
            json.dump(users_data, f, indent=4)

        messagebox.showinfo("Success", "Your account has been created successfully!")
        from login_frame import LoginFrame
        self.controller.show_frame(LoginFrame)