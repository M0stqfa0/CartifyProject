# profile_page.py
import customtkinter as ctk
from utils import TITLE_FONT, ENTRY_FONT, BUTTON_FONT
import json
from tkinter import messagebox

USER_JSON = "user_data.json"

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ================== Header ==================
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")

        logo_label = ctk.CTkLabel(header, text="Cartify - Profile", text_color="#D3DAD9", font=TITLE_FONT)
        logo_label.grid(row=0, column=0, padx=15, pady=10)

        def sign_out():
            from login_frame import LoginFrame
            self.controller.show_frame(LoginFrame)

        signout_btn = ctk.CTkButton(header, text="Sign Out", width=100, height=40,
                                    fg_color="#2d2d2d", hover_color="#48464f",
                                    command=sign_out, cursor="arrow")
        signout_btn.grid(row=0, column=4, padx=10, pady=10)

        def back_to_home():
            from user_home import UserHomePage
            self.controller.show_frame(UserHomePage)

        back_btn = ctk.CTkButton(header, text="Back", width=100, height=40,
                                 fg_color="#2d2d2d", hover_color="#48464f",
                                 command=back_to_home, cursor="arrow")
        back_btn.grid(row=0, column=5, padx=5, pady=10)

        header.grid_columnconfigure(3, weight=1)

        # ========== MAIN FRAME ==========
        self.main_frame = ctk.CTkFrame(self, fg_color="#1f1f1f", corner_radius=10)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.entries = {}
        self.load_user_data()

        button_width = 120

        # ================== Update Info Buttons ==================
        self.update_btn = ctk.CTkButton(self.main_frame, text="Update Info",
                                        font=BUTTON_FONT, fg_color="#2d2d2d",
                                        hover_color="#48464f", width=button_width,
                                        command=self.enable_edit)
        self.update_btn.grid(row=0, column=2, padx=20, pady=5, sticky="n")

        self.confirm_btn = ctk.CTkButton(self.main_frame, text="Confirm",
                                         font=BUTTON_FONT, fg_color="#2d2d2d",
                                         hover_color="#48464f", width=button_width,
                                         command=self.save_updates, state="disabled")
        self.confirm_btn.grid(row=1, column=2, padx=20, pady=5, sticky="n")

        # ================== Password ==================
        row_offset = len(self.entries) + 2
        ctk.CTkLabel(self.main_frame, text="Update Password", text_color="white", font=BUTTON_FONT)\
            .grid(row=row_offset, column=0, columnspan=2, pady=(20,5), sticky="w", padx=10)

        self.current_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Current Password",
                                         show="*", fg_color="#2d2d2d", text_color="white",
                                         font=ENTRY_FONT, state="disabled")
        self.current_pass.grid(row=row_offset+1, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        self.new_pass = ctk.CTkEntry(self.main_frame, placeholder_text="New Password",
                                     show="*", fg_color="#2d2d2d", text_color="white",
                                     font=ENTRY_FONT, state="disabled")
        self.new_pass.grid(row=row_offset+2, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        self.retype_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Retype New Password",
                                        show="*", fg_color="#2d2d2d", text_color="white",
                                        font=ENTRY_FONT, state="disabled")
        self.retype_pass.grid(row=row_offset+3, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        self.update_pass_btn = ctk.CTkButton(self.main_frame, text="Update Password",
                                             font=BUTTON_FONT, fg_color="#2d2d2d",
                                             hover_color="#48464f", width=button_width,
                                             command=self.enable_password)
        self.update_pass_btn.grid(row=row_offset+1, column=2, padx=20, pady=5, sticky="n")

        self.save_pass_btn = ctk.CTkButton(self.main_frame, text="Save Password",
                                           font=BUTTON_FONT, fg_color="#2d2d2d",
                                           hover_color="#48464f", width=button_width,
                                           command=self.save_password, state="disabled")
        self.save_pass_btn.grid(row=row_offset+2, column=2, rowspan=2, padx=20, pady=5, sticky="n")

        # Configure columns
        for i in range(2):
            self.main_frame.grid_columnconfigure(i, weight=1)

    # ================== LOAD USER DATA ==================
    def load_user_data(self):
        with open(USER_JSON, "r") as f:
            self.user_data = json.load(f)

        fields = ["name","phone","email","gender","governorate","password","age","national_id"]
        for idx, field in enumerate(fields):
            ctk.CTkLabel(self.main_frame, text=field.replace("_"," ").title(),
                         text_color="white", font=ENTRY_FONT)\
                .grid(row=idx, column=0, sticky="w", pady=5, padx=10)

            if field == "gender":
                entry = ctk.CTkComboBox(self.main_frame,
                                         values=["Male","Female","Prefer not to say"],
                                         font=ENTRY_FONT, dropdown_font=("Segoe UI",16),
                                         state="readonly")
            elif field == "governorate":
                entry = ctk.CTkComboBox(self.main_frame,
                                         values=['Governorate', 'Dakahlia', 'Red Sea', 'Beheira', 'Faiyum',
                                                 'Gharbia', 'Alexandria', 'Ismailia', 'Giza',
                                                 'Monufia', 'Minya', 'Cairo', 'Qalyubia',
                                                 'New Valley', 'Suez', 'Aswan', 'Assiut',
                                                 'Beni Suef', 'Port Said', 'Damietta',
                                                 'Sharqia', 'South Sinai', 'Kafr El Sheikh',
                                                 'Matruh', 'Luxor', 'Qena', 'North Sinai', 'Sohag'],
                                         font=ENTRY_FONT, dropdown_font=("Segoe UI",16),
                                         state="readonly")
            else:
                entry = ctk.CTkEntry(self.main_frame, fg_color="#2d2d2d",
                                      text_color="white", font=ENTRY_FONT)
                entry.insert(0,str(self.user_data.get(field,"")))

            entry.grid(row=idx, column=1, sticky="ew", pady=5, padx=10)

            if field in ["gender","governorate"]:
                entry.set(self.user_data.get(field,""))

            entry.configure(state="disabled")
            self.entries[field] = entry

    # ================== Update Info ==================
    def enable_edit(self):
        for key, entry in self.entries.items():
            if key != "password":
                entry.configure(state="normal")
        self.confirm_btn.configure(state="normal")

    # ================== Update Password ==================
    def enable_password(self):
        self.current_pass.configure(state="normal")
        self.new_pass.configure(state="normal")
        self.retype_pass.configure(state="normal")
        self.save_pass_btn.configure(state="normal")

    # ================== Save Updates ==================
    def save_updates(self):
        for key, entry in self.entries.items():
            if key != "password" and not entry.get().strip():
                messagebox.showwarning("Empty Field", f"Please fill the '{key.replace('_',' ').title()}' field.")
                return

        for key, entry in self.entries.items():
            if key != "password":
                self.user_data[key] = entry.get()
                entry.configure(state="disabled")

        with open(USER_JSON,"w") as f:
            json.dump(self.user_data,f,indent=4)
        self.confirm_btn.configure(state="disabled")
        messagebox.showinfo("Success","Profile updated successfully")

    # ================== Save Password ==================
    def save_password(self):
        if not self.current_pass.get().strip() or not self.new_pass.get().strip() or not self.retype_pass.get().strip():
            messagebox.showwarning("Empty Field", "Please fill all password fields.")
            return

        if self.current_pass.get() != self.user_data.get("password"):
            messagebox.showerror("Error","Current password is incorrect")
            return
        if self.new_pass.get() != self.retype_pass.get():
            messagebox.showerror("Error","New password and retype do not match")
            return

        self.user_data["password"] = self.new_pass.get()
        self.entries["password"].delete(0,"end")
        self.entries["password"].insert(0,self.new_pass.get())
        self.entries["password"].configure(state="disabled")

        self.current_pass.delete(0,"end")
        self.new_pass.delete(0,"end")
        self.retype_pass.delete(0,"end")
        self.current_pass.configure(state="disabled")
        self.new_pass.configure(state="disabled")
        self.retype_pass.configure(state="disabled")
        self.save_pass_btn.configure(state="disabled")

        with open(USER_JSON,"w") as f:
            json.dump(self.user_data,f,indent=4)
        messagebox.showinfo("Success","Password updated successfully")
