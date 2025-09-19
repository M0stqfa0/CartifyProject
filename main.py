import customtkinter as ctk
from login_frame import LoginFrame
from register_frame import RegisterFrame
from user_home import UserHomePage
from cart_page import CartPage
from profile_frame import ProfilePage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cartify - Local Shopping System")
        self.geometry("1000x700")
        self.minsize(900,600)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ================== A container for all the frames ==================
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # ================== Any new frame should be stored here ==================
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, UserHomePage, CartPage, ProfilePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # ================== Starts at the Login frame ==================
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == '__main__':
    app = App()
    app.mainloop()
