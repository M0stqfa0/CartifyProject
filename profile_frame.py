import customtkinter as ctk
from theme import *
import json
from tkinter import messagebox
import login_frame


class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entries = {}
        self.current_user_email = None

        # ================== Header ==================
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")
        logo_label = ctk.CTkLabel(header, text="Cartify - Profile", text_color="#D3DAD9", font=TITLE_FONT)
        logo_label.grid(row=0, column=0, padx=15, pady=10)
        signout_btn = ctk.CTkButton(header, text="Sign Out", width=100, height=40, fg_color="#2d2d2d",
                                    hover_color="#48464f", command=self.sign_out)
        signout_btn.grid(row=0, column=4, padx=10, pady=10)
        back_btn = ctk.CTkButton(header, text="Back", width=100, height=40, fg_color="#2d2d2d", hover_color="#48464f",
                                 command=self.back_to_home)
        back_btn.grid(row=0, column=5, padx=5, pady=10)
        header.grid_columnconfigure(3, weight=1)

        # ========== MAIN FRAME ==========
        self.main_frame = ctk.CTkFrame(self, fg_color="#1f1f1f", corner_radius=10)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_widgets()

    def refresh_data(self):
        self.current_user_email = login_frame.glob_current_user.get("email")
        if not self.current_user_email:
            messagebox.showerror("Error", "Could not load user data. Please log in again.")
            self.sign_out()
            return

        for field, widget in self.entries.items():
            value = login_frame.glob_current_user.get(field, "")
            widget.configure(state="normal")
            if isinstance(widget, ctk.CTkComboBox):
                widget.set(str(value))
            else:
                widget.delete(0, "end")
                widget.insert(0, str(value))
            widget.configure(state="disabled")

    def create_widgets(self):
        fields = ["name", "phone", "email", "gender", "governorate", "age", "national_id"]
        for idx, field in enumerate(fields):
            ctk.CTkLabel(self.main_frame, text=field.replace("_", " ").title(), text_color="white",
                         font=ENTRY_FONT).grid(row=idx, column=0, sticky="w", pady=5, padx=10)
            if field == "gender":
                entry = ctk.CTkComboBox(self.main_frame, values=["Male", "Female", "Prefer not to say"],
                                        font=ENTRY_FONT)
            elif field == "governorate":
                entry = ctk.CTkComboBox(self.main_frame,
                                        values=['Cairo', 'Giza', 'Alexandria', 'Dakahlia', 'Red Sea', 'Beheira',
                                                'Faiyum', 'Gharbia', 'Ismailia', 'Monufia', 'Minya', 'Qalyubia',
                                                'New Valley', 'Suez', 'Aswan', 'Assiut', 'Beni Suef', 'Port Said',
                                                'Damietta', 'Sharqia', 'South Sinai', 'Kafr El Sheikh', 'Matruh',
                                                'Luxor', 'Qena', 'North Sinai', 'Sohag'], font=ENTRY_FONT)
            else:
                entry = ctk.CTkEntry(self.main_frame, fg_color="#2d2d2d", text_color="white", font=ENTRY_FONT)

            entry.grid(row=idx, column=1, sticky="ew", pady=5, padx=10)
            entry.configure(state="disabled")
            self.entries[field] = entry

        button_width = 200

        self.update_btn = ctk.CTkButton(self.main_frame, text="Update Info",
                                        font=("Segoe UI", 18), width=button_width, command=self.enable_edit,
                                        fg_color="transparent", hover_color="#48464f")
        self.update_btn.grid(row=0, column=2, padx=20, pady=5, sticky="n")

        self.confirm_btn = ctk.CTkButton(self.main_frame, text="Confirm Changes",
                                         font=("Segoe UI", 18), width=button_width, command=self.save_updates,
                                         state="disabled",
                                         fg_color="transparent", hover_color="#48464f")
        self.confirm_btn.grid(row=1, column=2, padx=20, pady=5, sticky="n")

        row_offset = len(fields) + 2
        ctk.CTkLabel(self.main_frame, text="Update Password", font=("Segoe UI", 18, "bold")).grid(row=row_offset,
                                                                                                  column=0,
                                                                                                  columnspan=2,
                                                                                                  pady=(20, 5),
                                                                                                  sticky="w", padx=10)
        self.current_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Current Password", show="*",
                                         state="disabled")
        self.current_pass.grid(row=row_offset + 1, column=0, columnspan=2, sticky="ew", pady=5, padx=10)
        self.new_pass = ctk.CTkEntry(self.main_frame, placeholder_text="New Password", show="*", state="disabled")
        self.new_pass.grid(row=row_offset + 2, column=0, columnspan=2, sticky="ew", pady=5, padx=10)
        self.retype_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Retype New Password", show="*",
                                        state="disabled")
        self.retype_pass.grid(row=row_offset + 3, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        self.update_pass_btn = ctk.CTkButton(self.main_frame, text="Update Password",
                                             width=button_width, command=self.enable_password,
                                             font=("Segoe UI", 18),
                                             fg_color="transparent", hover_color="#48464f")
        self.update_pass_btn.grid(row=row_offset + 1, column=2, padx=20, pady=5, sticky="n")

        self.save_pass_btn = ctk.CTkButton(self.main_frame, text="Save Password",
                                           width=button_width, command=self.save_password, state="disabled",
                                           font=("Segoe UI", 18),
                                           fg_color="transparent", hover_color="#48464f")
        self.save_pass_btn.grid(row=row_offset + 2, column=2, rowspan=2, padx=20, pady=5, sticky="n")

        self.main_frame.grid_columnconfigure(1, weight=1)

    def enable_edit(self):
        for key, entry in self.entries.items():
            if key != "email": entry.configure(state="normal")
        self.confirm_btn.configure(state="normal")

    def enable_password(self):
        self.current_pass.configure(state="normal")
        self.new_pass.configure(state="normal")
        self.retype_pass.configure(state="normal")
        self.save_pass_btn.configure(state="normal")

    def save_updates(self):
        with open("user_data.json", "r") as f:
            all_users = json.load(f)
        for user_dict in all_users:
            if user_dict.get("email") == self.current_user_email:
                for key, entry in self.entries.items():
                    if key != "email": user_dict[key] = entry.get()
                login_frame.glob_current_user.update(user_dict)
                break
        with open("user_data.json", "w") as f:
            json.dump(all_users, f, indent=4)
        for entry in self.entries.values(): entry.configure(state="disabled")
        self.confirm_btn.configure(state="disabled")
        messagebox.showinfo("Success", "Profile updated successfully")

    def save_password(self):
        if not all([self.current_pass.get(), self.new_pass.get(), self.retype_pass.get()]):
            messagebox.showwarning("Empty Field", "Please fill all password fields.")
            return
        if self.current_pass.get() != login_frame.glob_current_user.get("password"):
            messagebox.showerror("Error", "Current password is incorrect")
            return
        if self.new_pass.get() != self.retype_pass.get():
            messagebox.showerror("Error", "New passwords do not match")
            return
        with open("user_data.json", "r") as f:
            all_users = json.load(f)
        for user_dict in all_users:
            if user_dict.get("email") == self.current_user_email:
                user_dict["password"] = self.new_pass.get()
                login_frame.glob_current_user["password"] = self.new_pass.get()
                break
        with open("user_data.json", "w") as f:
            json.dump(all_users, f, indent=4)
        self.current_pass.delete(0, "end")
        self.new_pass.delete(0, "end")
        self.retype_pass.delete(0, "end")
        self.current_pass.configure(state="disabled")
        self.new_pass.configure(state="disabled")
        self.retype_pass.configure(state="disabled")
        self.save_pass_btn.configure(state="disabled")
        messagebox.showinfo("Success", "Password updated successfully")

    def sign_out(self):
        from login_frame import LoginFrame
        login_frame.glob_current_user.clear()
        self.controller.show_frame(LoginFrame)

    def back_to_home(self):
        from user_home import UserHomePage
        self.controller.show_frame(UserHomePage)