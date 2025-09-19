from utils import *
import customtkinter as ctk
from functools import reduce

class CartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cart_items = []
        self.delivery_fee = 0  # <---- placeholder for delivery fee based on governorate


        # ================== Header
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")

        logo_label = ctk.CTkLabel(header, text="Cartify - Your Cart", text_color="#D3DAD9", font=TITLE_FONT)
        logo_label.grid(row=0, column=0, padx=(15,25), pady=10)

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

        self.total_label = ctk.CTkLabel(bottom_frame, text="Total: $0", text_color="white", font=("Segoe UI",18,'bold'))
        self.total_label.pack(side="left", padx=20, pady=10)

        checkout_btn = ctk.CTkButton(bottom_frame, text="Checkout", font=("Segoe UI",18,'bold'),
                                     fg_color="#2d2d2d", hover_color="#48464f", width=150,
                                     command=self.checkout)
        checkout_btn.pack(side="right", padx=20, pady=10)

    def update_cart(self, selected_products_data):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        self.qty_labels = []

        for idx, product in enumerate(selected_products_data):
            item_frame = ctk.CTkFrame(self.cart_frame, fg_color="#3b3b3b", corner_radius=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            remove_btn = ctk.CTkButton(item_frame, text="X", width=30, fg_color="#ff4d4d",
                                       hover=False,
                                       command=lambda i=idx: self.remove_item(i))
            remove_btn.place(relx=1, rely=0, anchor="ne", x=-5, y=5)

            name_label = ctk.CTkLabel(item_frame, text=product['name'], text_color="white", font=("Segoe UI",16))
            name_label.pack(anchor="w", padx=10, pady=(10,0))

            description_label = ctk.CTkLabel(item_frame, text=product.get('description', ''), text_color="white", font=("Segoe UI",12))
            description_label.pack(anchor="w", padx=10)

            price_label = ctk.CTkLabel(item_frame, text=f"${product['price']}", text_color="white", font=("Segoe UI",14,'bold'))
            price_label.pack(side="right", padx=10, pady=10)

            qty_frame = ctk.CTkFrame(item_frame, fg_color="#2d2d2d", corner_radius=5, height=40)
            qty_frame.pack(anchor="w", padx=10, pady=(0,10))
            qty_frame.pack_propagate(True)

            qty_label = ctk.CTkLabel(qty_frame, text="Quantity: 1", text_color="white", font=("Segoe UI",12))
            qty_label.pack(side="left", padx=5)
            self.qty_labels.append(qty_label)

            def update_qty(delta, index=idx):
                self.cart_items[index]['quantity'] += delta
                if self.cart_items[index]['quantity'] < 1:
                    self.cart_items[index]['quantity'] = 1
                self.qty_labels[index].configure(text=f"Quantity: {self.cart_items[index]['quantity']}")
                self.update_total()

            minus_btn = ctk.CTkButton(qty_frame, text="-", width=30, fg_color="transparent",
                                      hover_color="#2d2d2d", command=lambda d=-1,i=idx:update_qty(d,i))
            minus_btn.pack(side="left", padx=5)
            plus_btn = ctk.CTkButton(qty_frame, text="+", width=30, fg_color="transparent",
                                     hover_color="#2d2d2d", command=lambda d=1,i=idx:update_qty(d,i))
            plus_btn.pack(side="left", padx=5)

        self.cart_items = [{'name': p['name'], 'price': p['price'], 'quantity': 1, 'description': p.get('description', '')} for p in selected_products_data]
        self.update_total()

    def remove_item(self, index):
        del self.cart_items[index]
        self.update_cart(self.cart_items)

    def update_total(self):
        total = reduce(lambda acc, item: acc + item['price']*item['quantity'], self.cart_items, 0)
        total_with_delivery = total + self.delivery_fee  # <--- This to calculate delivery fee, not done yet
        self.total_label.configure(text=f"Total: ${total_with_delivery}")

    def checkout(self):
        for item in self.cart_items:
            print(f"{item['name']} orders increased by {item['quantity']}")
        self.cart_items.clear()
        self.update_cart([])
        self.update_total()
        from user_home import UserHomePage
        self.controller.show_frame(UserHomePage)
