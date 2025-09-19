from utils import *
import customtkinter as ctk
from functools import reduce
from tkinter import messagebox

class CartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cart_items = []
        self.delivery_fee = 0  # <---- placeholder for delivery fee based on governorate

        # ================== Header ==================
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")

        logo_label = ctk.CTkLabel(header, text="Cartify - Your Cart", text_color="#D3DAD9", font=TITLE_FONT)
        logo_label.grid(row=0, column=0, padx=(15, 25), pady=10)

        def back_to_home():
            from user_home import UserHomePage
            self.controller.show_frame(UserHomePage)

        back_btn = ctk.CTkButton(header, text="Back", width=100, height=40,
                                 fg_color="#2d2d2d", hover_color="#48464f",
                                 command=back_to_home, cursor="arrow")
        back_btn.grid(row=0, column=5, padx=10, pady=10)
        header.grid_columnconfigure(1, weight=1)

        # ================== Cart Frame ==================
        self.cart_frame = ctk.CTkScrollableFrame(self, fg_color="#2d2d2d", corner_radius=10)
        self.cart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ================== Bottom frame ==================
        bottom_frame = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        bottom_frame.pack(side="bottom", fill="x", pady=5)

        self.total_label = ctk.CTkLabel(bottom_frame, text="Total: $0", text_color="white",
                                        font=("Segoe UI", 18, 'bold'))
        self.total_label.pack(side="left", padx=20, pady=10)

        checkout_btn = ctk.CTkButton(bottom_frame, text="Checkout", font=("Segoe UI", 18, 'bold'),
                                     fg_color="#2d2d2d", hover_color="#48464f", width=150,
                                     command=self.checkout)
        checkout_btn.pack(side="right", padx=20, pady=10)

    def update_cart(self, selected_products_data):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        for idx, product in enumerate(selected_products_data):
            item_frame = ctk.CTkFrame(self.cart_frame, fg_color="#3b3b3b", corner_radius=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            header_item_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            header_item_frame.pack(fill="x", padx=5, pady=(5, 0))

            # Product name label
            name_label = ctk.CTkLabel(header_item_frame, text=product['name'], text_color="white",
                                      font=("Segoe UI", 16, "bold"), anchor="w")
            name_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

            # The 'X' button
            remove_btn = ctk.CTkButton(header_item_frame, text="X", width=30, fg_color="#ff4d4d",
                                       hover=False,
                                       command=lambda i=idx: self.remove_item(i))
            remove_btn.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="e")

            header_item_frame.grid_columnconfigure(0, weight=1)

            # Product description
            description_label = ctk.CTkLabel(item_frame, text=product.get('description', ''), text_color="lightgray",
                                             font=("Segoe UI", 12), anchor="w")
            description_label.pack(fill="x", padx=10)

            quantity = product.get('quantity', 1)
            price = product['price']
            subtotal = quantity * price

            details_label = ctk.CTkLabel(item_frame, text=f"Quantity: {quantity}   (Subtotal: ${subtotal:.2f})",
                                         text_color="white",
                                         font=("Segoe UI", 14, "bold"), anchor="w")
            details_label.pack(fill="x", padx=10, pady=(5, 10))

        self.cart_items = [{'name': p['name'], 'price': p['price'], 'quantity': p.get('quantity', 1),
                            'description': p.get('description', '')} for p in selected_products_data]
        self.update_total()

    def remove_item(self, index):
        from user_home import UserHomePage
        home_page = self.controller.frames.get(UserHomePage)

        if home_page and index < len(self.cart_items):
            product_name_to_remove = self.cart_items[index]['name']
            home_page.reset_item_quantity(product_name_to_remove)

        del self.cart_items[index]
        self.update_cart(self.cart_items)

    def update_total(self):
        total = reduce(lambda acc, item: acc + item['price'] * item['quantity'], self.cart_items, 0)
        total_with_delivery = total + self.delivery_fee
        self.total_label.configure(text=f"Total: ${total_with_delivery:.2f}")

    def checkout(self):
        from user_home import UserHomePage

        messagebox.showinfo("Order details", "Checkout successful.")

        home_page = self.controller.frames.get(UserHomePage)
        if home_page:
            home_page.clear_cart_data()

        # ================== Clear Cart ==================
        self.cart_items.clear()
        self.update_cart([])

        self.controller.show_frame(UserHomePage)