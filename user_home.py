import customtkinter as ctk
from PIL import Image
import json
from profile_frame import ProfilePage
from cart_page import CartPage
from utils import TITLE_FONT, BUTTON_FONT

class UserHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_products = set()
        self.cart_products = []

        # ================== Header Frame ==================
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")

        logo_label = ctk.CTkLabel(header, text="Cartify", text_color="#D3DAD9", font=TITLE_FONT)
        logo_label.grid(row=0, column=0, padx=(15, 5), pady=10)

        # ================== Search bar & button ==================
        search_bar = ctk.CTkEntry(header, width=400, height=40, font=BUTTON_FONT, placeholder_text="Search...",
                                  fg_color="#1f1f1f", text_color="#D3DAD9")
        search_bar.grid(row=0, column=1, padx=(0, 5), pady=10, sticky="ew")

        search_btn = ctk.CTkButton(header, text="", image=ctk.CTkImage(dark_image=Image.open("images/magnifying-glass(2).png"), size=(30, 30)),
                                   width=80, height=40, fg_color="transparent", hover_color="#48464f")
        search_btn.grid(row=0, column=2, padx=(5, 3), pady=10)

        # ================== Filter button ==================
        filter_btn = ctk.CTkButton(header, text="", width=80, height=40,
                                   image=ctk.CTkImage(dark_image=Image.open("images/filter.png"), size=(35, 35)),
                                   fg_color="transparent", hover_color="#48464f")
        filter_btn.grid(row=0, column=3, padx=(3, 10), pady=10)

        # ================== Profile button ==================
        profile_btn = ctk.CTkButton(header, text="", width=80, height=40,
                                    image=ctk.CTkImage(dark_image=Image.open("images/vectorstock_42797441-removebg-preview.png"), size=(45, 45)),
                                    fg_color="transparent", hover_color="#48464f",
                                    command=self.go_to_profile, cursor="arrow")
        profile_btn.grid(row=0, column=4, padx=(3, 3), pady=10)

        # ================== Cart button ==================
        cart_btn = ctk.CTkButton(header, text="", image=ctk.CTkImage(
            dark_image=Image.open("images/shoppingcart.png"), size=(45, 45)),
                                 width=80, height=40, fg_color="transparent", hover_color="#48464f",
                                 command=self.go_to_cart, cursor="arrow")
        cart_btn.grid(row=0, column=5, padx=(3, 30), pady=10)

        header.grid_columnconfigure(1, weight=1)

        # ================== Main frame ==================
        middle_frame = ctk.CTkFrame(self, fg_color="#44444E")
        middle_frame.pack(expand=True, fill="both")

        # ================== Load products from JSON ==================
        with open("products.json", "r") as f:
            self.products_data = json.load(f)

        # ====================================================== Left Panel ======================================================
        left_panel = ctk.CTkFrame(middle_frame, fg_color="#1f1f1f", width=250, corner_radius=10)
        left_panel.pack(side="left", fill="y", padx=5, pady=5)

        categories_frame = ctk.CTkFrame(left_panel, fg_color="#2d2d2d", corner_radius=10)
        categories_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ================== Category buttons ==================
        self.categories_list = ["Home", "Appliances", "Electronics", "Fashion", "Books", "Sports",
                                "Gaming", "Furniture", "Groceries", "Toys", "Beauty"]

        for key in self.categories_list:
            btn = ctk.CTkButton(categories_frame, text=key, fg_color="transparent", hover_color="#333333",
                                text_color="white", corner_radius=5, font=BUTTON_FONT, anchor="w",
                                command=lambda k=key: self.filter_products(k))
            btn.pack(fill="x", pady=3, padx=5)

        # ====================================================== Right Panel ======================================================
        right_panel = ctk.CTkFrame(middle_frame, fg_color="#1f1f1f", corner_radius=10)
        right_panel.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        title_label = ctk.CTkLabel(right_panel, text="All Products", font=("Segoe UI", 22, "bold"), height=35)
        title_label.pack(fill="x", padx=10, pady=(10, 0))

        self.products_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2d2d2d", corner_radius=10, width=600, height=500)
        self.products_frame.pack(fill="both", expand=True, padx=10, pady=10)

        add_cart_btn = ctk.CTkButton(right_panel, text="Add to cart", font=("Segoe UI", 22, 'bold'),
                                     fg_color="#2d2d2d", hover_color="#48464f", text_color="#D3DAD9",
                                     command=self.add_to_cart)
        add_cart_btn.pack(anchor="center", pady=(5, 15))

        self.display_products(self.products_data) # <--- Show all products initially

    # ================== Display Products ==================
    def display_products(self, products):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        def toggle_selection(i, frame):
            if i in self.selected_products:
                self.selected_products.remove(i)
                frame.configure(fg_color="#3b3b3b")
            else:
                self.selected_products.add(i)
                frame.configure(fg_color="#555555")

        for i, product in enumerate(products):
            product_card = ctk.CTkFrame(self.products_frame, fg_color="#3b3b3b", corner_radius=8)
            product_card.pack(fill="x", padx=5, pady=5)
            product_card.bind("<Button-1>", lambda e, i=i, f=product_card: toggle_selection(i, f))

            ctk.CTkLabel(product_card, text=product["name"], text_color="white", font=("Segoe UI", 16), anchor="w").pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(product_card, text=product["description"], text_color="white", font=("Segoe UI", 12), anchor="w").pack(anchor="w", padx=10, pady=(0, 0))
            ctk.CTkLabel(product_card, text=f"${product['price']}", text_color="white").pack(side="right", padx=10, pady=10)



    # ================== Filter Products ==================
    def filter_products(self, category):
        if category == "Home":
            filtered = self.products_data
        else:
            filtered = [p for p in self.products_data if p["category"].strip().lower() == category.strip().lower()]
        self.display_products(filtered)

    # ================== Cart ==================
    def add_to_cart(self):
        for i in self.selected_products:
            product_data = self.products_data[i]
            if product_data not in self.cart_products:
                self.cart_products.append(product_data)
        self.selected_products.clear()

    def go_to_cart(self):
        cart_page = self.controller.frames.get(CartPage)
        if cart_page:
            cart_page.update_cart(self.cart_products)
        self.controller.show_frame(CartPage)

    # ================== Profile Icon ==================
    def go_to_profile(self):
        profile_page = self.controller.frames.get(ProfilePage)
        if profile_page is None:
            profile_page = ProfilePage(self.controller.container, self.controller)
            self.controller.frames[ProfilePage] = profile_page
            profile_page.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame(ProfilePage)
