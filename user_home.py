import customtkinter as ctk
from PIL import Image
import json
from tkinter import messagebox
from utils import TITLE_FONT, BUTTON_FONT


class UserHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.item_quantities = {}
        self.cart_products = []
        self.product_widgets = {}

        # ================== Header Frame ==================
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")

        logo_label = ctk.CTkLabel(header, text="Cartify", text_color="#D3DAD9", font=TITLE_FONT)
        logo_label.grid(row=0, column=0, padx=(15, 5), pady=10)

        self.search_bar = ctk.CTkEntry(header, width=400, height=40, font=BUTTON_FONT, placeholder_text="Search...",
                                       fg_color="#1f1f1f", text_color="#D3DAD9")
        self.search_bar.grid(row=0, column=1, padx=(0, 5), pady=10, sticky="ew")
        search_btn = ctk.CTkButton(header, text="",
                                   image=ctk.CTkImage(dark_image=Image.open("images/magnifying-glass(2).png"),
                                                      size=(30, 30)), width=80, height=40, fg_color="transparent",
                                   hover_color="#48464f", command=self.perform_search)
        search_btn.grid(row=0, column=2, padx=(5, 3), pady=10)

        self.sort_by_combo = ctk.CTkComboBox(header, values=["Name", "Price"])
        self.sort_by_combo.grid(row=0, column=3, padx=(3, 10), pady=10)
        self.sort_by_combo.set("Sort by...")

        self.sort_order_combo = ctk.CTkComboBox(header, values=["Ascending", "Descending"])
        self.sort_order_combo.grid(row=0, column=4, padx=(3, 10), pady=10)
        self.sort_order_combo.set("Order")

        sort_btn = ctk.CTkButton(header, text="", image=ctk.CTkImage(dark_image=Image.open("images/up-and-down-arrow.png"), size=(30, 30)),
                                 fg_color="transparent", hover_color="#48464f",width=60, command=self.perform_sort)
        sort_btn.grid(row=0, column=5, padx=(3, 10), pady=10)

        profile_btn = ctk.CTkButton(header, text="", width=80, height=40, image=ctk.CTkImage(
            dark_image=Image.open("images/vectorstock_42797441-removebg-preview.png"), size=(45, 45)),
                                    fg_color="transparent", hover_color="#48464f", command=self.go_to_profile,
                                    cursor="arrow")
        profile_btn.grid(row=0, column=6, padx=(3, 3), pady=10)
        cart_btn = ctk.CTkButton(header, text="",
                                 image=ctk.CTkImage(dark_image=Image.open("images/shoppingcart.png"), size=(45, 45)),
                                 width=80, height=40, fg_color="transparent", hover_color="#48464f",
                                 command=self.go_to_cart, cursor="arrow")
        cart_btn.grid(row=0, column=7, padx=(3, 30), pady=10)

        header.grid_columnconfigure(1, weight=1)

        # ================== Main frame ==================
        middle_frame = ctk.CTkFrame(self, fg_color="#44444E")
        middle_frame.pack(expand=True, fill="both")

        with open("products.json", "r") as f:
            self.all_products = json.load(f)

        self.currently_displayed = self.all_products

        # ================== Left Panel ==================
        left_panel = ctk.CTkFrame(middle_frame, fg_color="#1f1f1f", width=250, corner_radius=10)
        left_panel.pack(side="left", fill="y", padx=5, pady=5)
        categories_frame = ctk.CTkFrame(left_panel, fg_color="#2d2d2d", corner_radius=10)
        categories_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.categories_list = ["Home", "Appliances", "Electronics", "Fashion", "Books", "Sports", "Gaming",
                                "Furniture", "Groceries", "Toys", "Beauty"]
        for key in self.categories_list:
            btn = ctk.CTkButton(categories_frame, text=key, fg_color="transparent", hover_color="#333333",
                                text_color="white", corner_radius=5, font=BUTTON_FONT, anchor="w",
                                command=lambda k=key: self.filter_products(k))
            btn.pack(fill="x", pady=3, padx=5)

        # ================== Right Panel ==================
        right_panel = ctk.CTkFrame(middle_frame, fg_color="#1f1f1f", corner_radius=10)
        right_panel.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.title_label = ctk.CTkLabel(right_panel, text="All Products", font=("Segoe UI", 22, "bold"), height=35)
        self.title_label.pack(fill="x", padx=10, pady=(10, 0))
        self.products_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2d2d2d", corner_radius=10, width=600,
                                                     height=500)
        self.products_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_products(self.all_products)

    def merge(self, left, right, key, reverse):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if (not reverse and key(left[i]) <= key(right[j])) or \
                    (reverse and key(left[i]) >= key(right[j])):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort(self, arr, key, reverse=False):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], key, reverse)
        right = self.merge_sort(arr[mid:], key, reverse)
        return self.merge(left, right, key, reverse)

    def perform_sort(self):
        sort_by_text = self.sort_by_combo.get()
        sort_order = self.sort_order_combo.get()

        if "Sort by" in sort_by_text or "Order" in sort_order:
            messagebox.showwarning("Selection Error", "Please select both a sort attribute and an order.")
            return

        key_attr = "name" if "Name" in sort_by_text else "price"
        key_func = lambda item: item[key_attr]
        reverse = (sort_order == "Descending")

        sorted_list = self.merge_sort(self.currently_displayed, key=key_func, reverse=reverse)
        self.display_products(sorted_list)

    def perform_search(self):
        search_term = self.search_bar.get().lower()
        if not search_term:
            self.display_products(self.all_products)
            return

        results = [p for p in self.all_products if search_term in p['name'].lower()]
        self.display_products(results)

    def display_products(self, products):
        self.currently_displayed = products
        for widget in self.products_frame.winfo_children(): widget.destroy()
        self.product_widgets.clear()
        for product in products:
            product_name = product['name']
            product_card = ctk.CTkFrame(self.products_frame, fg_color="#3b3b3b", corner_radius=8);
            product_card.pack(fill="x", padx=5, pady=5)
            info_frame = ctk.CTkFrame(product_card, fg_color="transparent");
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            ctk.CTkLabel(info_frame, text=product["name"], text_color="white", font=("Segoe UI", 16, "bold"),
                         anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=product["description"], text_color="lightgray", font=("Segoe UI", 12),
                         anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"${product['price']}", text_color="white", font=("Segoe UI", 14, "bold"),
                         anchor="w").pack(fill="x", pady=(5, 0))
            controls_frame = ctk.CTkFrame(product_card, fg_color="transparent");
            controls_frame.pack(side="right", padx=10)
            add_btn = ctk.CTkButton(controls_frame, text="+", width=30, font=("Segoe UI", 18, "bold"),
                                    fg_color="transparent", hover_color="#48464f",
                                    command=lambda p=product: self.add_item(p));
            add_btn.pack(side="right", padx=5)
            count_label = ctk.CTkLabel(controls_frame, text="", width=25, font=("Segoe UI", 18))
            remove_btn = ctk.CTkButton(controls_frame, text="-", width=30, font=("Segoe UI", 18, "bold"),
                                       fg_color="transparent", hover_color="#48464f",
                                       command=lambda p=product: self.remove_item(p))
            quantity = self.item_quantities.get(product_name, 0)
            if quantity > 0:
                count_label.configure(text=str(quantity));
                remove_btn.pack(side="left", padx=5);
                count_label.pack(side="left", padx=5)
            self.product_widgets[product_name] = {'count_label': count_label, 'remove_btn': remove_btn}

    def filter_products(self, category):
        if category == "Home":
            filtered = self.all_products
        else:
            filtered = [p for p in self.all_products if p["category"].strip().lower() == category.strip().lower()]
        self.display_products(filtered)

    def add_item(self, product):
        product_name = product['name']
        current_quantity = self.item_quantities.get(product_name, 0)
        self.item_quantities[product_name] = current_quantity + 1
        if product not in self.cart_products:
            self.cart_products.append(product)
        widgets = self.product_widgets[product_name]
        widgets['count_label'].configure(text=str(self.item_quantities[product_name]))
        widgets['remove_btn'].pack(side="left", padx=5)
        widgets['count_label'].pack(side="left", padx=5)

    def remove_item(self, product):
        product_name = product['name']
        current_quantity = self.item_quantities.get(product_name, 0)
        if current_quantity <= 0: return
        self.item_quantities[product_name] = current_quantity - 1
        widgets = self.product_widgets[product_name]
        if self.item_quantities[product_name] == 0:
            self.cart_products = [p for p in self.cart_products if p['name'] != product_name]
            widgets['remove_btn'].pack_forget()
            widgets['count_label'].pack_forget()
        else:
            widgets['count_label'].configure(text=str(self.item_quantities[product_name]))

    def reset_item_quantity(self, product_name):
        if product_name in self.item_quantities:
            self.item_quantities.pop(product_name)
        self.cart_products = [p for p in self.cart_products if p['name'] != product_name]
        self.display_products(self.all_products)

    def go_to_cart(self):
        from cart_page import CartPage
        for product in self.cart_products:
            product['quantity'] = self.item_quantities.get(product['name'], 0)
        cart_page = self.controller.frames.get(CartPage)
        if cart_page:
            final_cart = [p for p in self.cart_products if p.get('quantity', 0) > 0]
            cart_page.update_cart(final_cart)
        self.controller.show_frame(CartPage)

    def go_to_profile(self):
        from profile_frame import ProfilePage
        profile_page = self.controller.frames.get(ProfilePage)
        if profile_page:
            profile_page.refresh_data()
        self.controller.show_frame(ProfilePage)

    def clear_cart_data(self):
        self.item_quantities.clear()
        self.cart_products.clear()
        self.display_products(self.all_products)