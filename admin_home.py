import customtkinter as ctk
from PIL import Image
import json
from tkinter import messagebox
from login_frame import LoginFrame
from theme import *

class AdminHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_widgets = {}
        self.editing_product_name = None

        # ================== Header Frame ==================
        header = ctk.CTkFrame(self, fg_color="#37353E", corner_radius=0)
        header.pack(side="top", fill="x")

        logo_label = ctk.CTkLabel(header, text="", image=ctk.CTkImage(dark_image=Image.open("images/header (2).png"),
                                                                      size=(250, 80)), fg_color="transparent")
        logo_label.grid(row=0, column=0)

        self.search_bar = ctk.CTkEntry(header, width=400, height=40, font=BUTTON_FONT, placeholder_text="Search...",
                                       fg_color="#1f1f1f", text_color="#D3DAD9")
        self.search_bar.grid(row=0, column=1, padx=(0, 5), pady=10, sticky="ew")

        search_btn = ctk.CTkButton(header, text="",
                                   image=ctk.CTkImage(dark_image=Image.open("images/magnifying-glass(2).png"),
                                                      size=(30, 30)), width=80, height=40, fg_color="transparent",
                                   hover_color="#48464f", command=self.perform_search)
        search_btn.grid(row=0, column=2, padx=(5, 3), pady=10)

        self.sort_by_combo = ctk.CTkComboBox(header, values=["Name", "Price"], width=140)
        self.sort_by_combo.grid(row=0, column=3, padx=(3, 10), pady=10)
        self.sort_by_combo.set("Sort by...")

        self.sort_order_combo = ctk.CTkComboBox(header, values=["Ascending", "Descending"], width=120)
        self.sort_order_combo.grid(row=0, column=4, padx=(3, 10), pady=10)
        self.sort_order_combo.set("Order")

        sort_btn = ctk.CTkButton(header, text="", image=ctk.CTkImage(dark_image=Image.open("images/up-and-down-arrow.png"), size=(30, 30)),
                                 width=60,fg_color="transparent", hover_color="#48464f", command=self.perform_sort)
        sort_btn.grid(row=0, column=5, padx=(3, 10), pady=10)

        signout_btn = ctk.CTkButton(header, text="", font=BUTTON_FONT,
                                    image=ctk.CTkImage(dark_image=Image.open("images/logout.png"), size=(35, 35)),
                                    width=80, height=40, fg_color="transparent", hover_color="#48464f",
                                    command=self.sign_out)
        signout_btn.grid(row=0, column=6, padx=(10, 20), pady=10)

        header.grid_columnconfigure(1, weight=1)

        # ================== Main frame ==================
        middle_frame = ctk.CTkFrame(self, fg_color="#44444E")
        middle_frame.pack(expand=True, fill="both")
        with open("products.json", "r") as f:
            self.products_data = json.load(f)

        self.currently_displayed = self.products_data

        # ================== Left Panel (Categories) ==================
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

        # ================== Right Panel (Products) ==================
        right_panel = ctk.CTkFrame(middle_frame, fg_color="#1f1f1f", corner_radius=10)
        right_panel.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.title_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.title_frame.grid_columnconfigure(1, weight=1)
        try:
            with open("user_data.json", "r") as f:
                user_count = len(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            user_count = 0
        user_count_label = ctk.CTkLabel(self.title_frame, text=f"Total Users: {user_count}",
                                        font=("Segoe UI", 18, "bold"))
        user_count_label.grid(row=0, column=0, sticky="w")
        self.title_label = ctk.CTkLabel(self.title_frame, text="Admin Homepage", font=("Segoe UI", 22, "bold"))
        self.title_label.grid(row=0, column=1, sticky="ew")
        add_product_btn = ctk.CTkButton(self.title_frame, text="Add Product +", font=("Segoe UI", 18, "bold"),
                                        fg_color="transparent", hover_color="#3b3b3b",
                                        command=self.toggle_add_product_frame)
        add_product_btn.grid(row=0, column=2, sticky="e")
        self.create_add_product_widgets(right_panel)
        self.products_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2d2d2d", corner_radius=10)
        self.products_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.display_products(self.products_data)

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
            self.display_products(self.products_data)
            return

        results = [p for p in self.products_data if search_term in p['name'].lower()]
        self.display_products(results)

    def display_products(self, products):
        self.currently_displayed = products
        for widget in self.products_frame.winfo_children(): widget.destroy()
        self.product_widgets.clear()
        for product in products:
            product_name = product['name']
            product_card = ctk.CTkFrame(self.products_frame, fg_color="#3b3b3b", corner_radius=8)
            product_card.pack(fill="x", padx=5, pady=5)
            display_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            display_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            ctk.CTkLabel(display_frame, text=product["name"], font=("Segoe UI", 16, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(display_frame, text=product["description"], font=("Segoe UI", 12), anchor="w").pack(fill="x")
            ctk.CTkLabel(display_frame, text=f"${product['price']}", font=("Segoe UI", 14, "bold"), anchor="w").pack(
                fill="x", pady=(5, 0))
            edit_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            name_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            name_entry.pack(fill="x", pady=2)
            desc_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            desc_entry.pack(fill="x", pady=2)
            price_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            price_entry.pack(fill="x", pady=2)
            controls_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            controls_frame.pack(side="right", padx=10)
            toggle_edit_btn = ctk.CTkButton(controls_frame, text="", width=30,
                                            image=ctk.CTkImage(dark_image=Image.open("images/pencil.png"),
                                                               size=(25, 25)),
                                            command=lambda name=product_name: self.on_toggle_button_click(name),
                                            fg_color="transparent", hover_color="#48464f")
            toggle_edit_btn.pack(pady=2)
            remove_btn = ctk.CTkButton(controls_frame, text="", width=30,
                                       image=ctk.CTkImage(dark_image=Image.open("images/trash.png"), size=(25, 25)),
                                       command=lambda p=product: self.remove_product(p), fg_color="transparent",
                                       hover_color="#48464f")
            remove_btn.pack(pady=2)
            cancel_btn = ctk.CTkButton(controls_frame, text="", width=30, fg_color="transparent", hover_color="#48464f",
                                       image=ctk.CTkImage(dark_image=Image.open("images/close (1).png"), size=(20, 20)),
                                       command=lambda name=product_name: self.exit_edit_mode(name))
            self.product_widgets[product_name] = {'original_product': product, 'display_frame': display_frame,
                                                  'edit_frame': edit_frame, 'name_entry': name_entry,
                                                  'desc_entry': desc_entry, 'price_entry': price_entry,
                                                  'toggle_edit_btn': toggle_edit_btn, 'remove_btn': remove_btn,
                                                  'cancel_btn': cancel_btn}

    def filter_products(self, category):
        if category == "Home":
            filtered = self.products_data
        else:
            filtered = [p for p in self.products_data if p["category"].strip().lower() == category.strip().lower()]
        self.display_products(filtered)


    def sign_out(self):
        from login_frame import LoginFrame
        messagebox.showinfo("Goodbye", "See you soon, Admin!")
        self.controller.show_frame(LoginFrame)

    def create_add_product_widgets(self, parent):
        self.add_product_frame = ctk.CTkFrame(parent, fg_color="#3b3b3b", corner_radius=8)
        self.add_product_frame.grid_columnconfigure(0, weight=1)
        entry_frame = ctk.CTkFrame(self.add_product_frame, fg_color="transparent")
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.new_name_entry = ctk.CTkEntry(entry_frame, placeholder_text="Product Name")
        self.new_name_entry.pack(fill="x", expand=True, pady=2)
        self.new_desc_entry = ctk.CTkEntry(entry_frame, placeholder_text="Description")
        self.new_desc_entry.pack(fill="x", expand=True, pady=2)
        self.new_price_entry = ctk.CTkEntry(entry_frame, placeholder_text="Price")
        self.new_price_entry.pack(fill="x", expand=True, pady=2)
        self.new_category_entry = ctk.CTkComboBox(entry_frame, values=self.categories_list[1:])
        self.new_category_entry.pack(fill="x", expand=True, pady=2)
        self.new_category_entry.set("Select Category")
        button_frame = ctk.CTkFrame(self.add_product_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        confirm_btn = ctk.CTkButton(button_frame, text="", fg_color="transparent", hover_color="#48464f",
                                    image=ctk.CTkImage(dark_image=Image.open("images/check.png"), size=(25, 25)),
                                    command=self.confirm_add_product)
        confirm_btn.pack(pady=2)
        cancel_btn = ctk.CTkButton(button_frame, text="", fg_color="transparent", hover_color="#48464f",
                                   image=ctk.CTkImage(dark_image=Image.open("images/close (1).png"), size=(20, 20)),
                                   command=self.toggle_add_product_frame)
        cancel_btn.pack(pady=2)

    def toggle_add_product_frame(self):
        if self.add_product_frame.winfo_viewable():
            self.add_product_frame.pack_forget()
        else:
            self.add_product_frame.pack(after=self.title_frame, fill="x", padx=10, pady=10)

    def confirm_add_product(self):
        name = self.new_name_entry.get()
        desc = self.new_desc_entry.get()
        price_str = self.new_price_entry.get()
        category = self.new_category_entry.get()
        if not all([name, desc, price_str, category != "Select Category"]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
            return
        new_product = {"name": name, "description": desc, "price": price, "orders": 0, "category": category}
        self.products_data.append(new_product)
        with open("products.json", "w") as f:
            json.dump(self.products_data, f, indent=4)
        self.display_products(self.products_data)
        self.new_name_entry.delete(0, "end")
        self.new_desc_entry.delete(0, "end")
        self.new_price_entry.delete(0, "end")
        self.new_category_entry.set("Select Category")
        self.toggle_add_product_frame()

    def on_toggle_button_click(self, product_name):
        if self.editing_product_name == product_name:
            self.save_product_changes(product_name)
        elif self.editing_product_name is None:
            self.enter_edit_mode(product_name)
        else:
            messagebox.showinfo("Action Required",
                                f"Please save or cancel your changes for\n'{self.editing_product_name}' first.")

    def enter_edit_mode(self, product_name):
        self.editing_product_name = product_name
        widgets = self.product_widgets[product_name]
        widgets['toggle_edit_btn'].configure(
            image=ctk.CTkImage(dark_image=Image.open("images/check.png"), size=(25, 25)))
        widgets['display_frame'].pack_forget()
        widgets['remove_btn'].pack_forget()
        widgets['edit_frame'].pack(side="left", fill="x", expand=True, padx=10, pady=5)
        widgets['cancel_btn'].pack(pady=2)
        product = widgets['original_product']
        widgets['name_entry'].delete(0, 'end')
        widgets['name_entry'].insert(0, product['name'])
        widgets['desc_entry'].delete(0, 'end')
        widgets['desc_entry'].insert(0, product['description'])
        widgets['price_entry'].delete(0, 'end')
        widgets['price_entry'].insert(0, product['price'])

    def exit_edit_mode(self, product_name):
        self.editing_product_name = None
        widgets = self.product_widgets[product_name]
        widgets['toggle_edit_btn'].configure(
            image=ctk.CTkImage(dark_image=Image.open("images/pencil.png"), size=(25, 25)))
        widgets['edit_frame'].pack_forget()
        widgets['cancel_btn'].pack_forget()
        widgets['display_frame'].pack(side="left", fill="x", expand=True, padx=10, pady=5)
        widgets['remove_btn'].pack(pady=2)

    def save_product_changes(self, old_product_name):
        widgets = self.product_widgets[old_product_name]
        try:
            new_price = float(widgets['price_entry'].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a valid number.")
            return
        for product in self.products_data:
            if product['name'] == old_product_name:
                product['name'], product['description'], product['price'] = widgets['name_entry'].get(), widgets[
                    'desc_entry'].get(), new_price
                break
        with open("products.json", "w") as f:
            json.dump(self.products_data, f, indent=4)
        self.editing_product_name = None
        self.display_products(self.products_data)

    def remove_product(self, product_to_remove):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove {product_to_remove['name']}?"):
            self.products_data = [p for p in self.products_data if p['name'] != product_to_remove['name']]
            with open("products.json", "w") as f: json.dump(self.products_data, f, indent=4)
            self.display_products(self.products_data)

    def display_products(self, products):
        for widget in self.products_frame.winfo_children(): widget.destroy()
        self.product_widgets.clear()
        for product in products:
            product_name = product['name']
            product_card = ctk.CTkFrame(self.products_frame, fg_color="#3b3b3b", corner_radius=8)
            product_card.pack(fill="x", padx=5, pady=5)
            display_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            display_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            ctk.CTkLabel(display_frame, text=product["name"], font=("Segoe UI", 16, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(display_frame, text=product["description"], font=("Segoe UI", 12), anchor="w").pack(fill="x")
            ctk.CTkLabel(display_frame, text=f"${product['price']}", font=("Segoe UI", 14, "bold"), anchor="w").pack(
                fill="x", pady=(5, 0))
            edit_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            name_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            name_entry.pack(fill="x", pady=2)
            desc_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            desc_entry.pack(fill="x", pady=2)
            price_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            price_entry.pack(fill="x", pady=2)
            controls_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            controls_frame.pack(side="right", padx=10)
            toggle_edit_btn = ctk.CTkButton(controls_frame, text="", width=30,
                                            image=ctk.CTkImage(dark_image=Image.open("images/pencil.png"),
                                                               size=(25, 25)),
                                            command=lambda name=product_name: self.on_toggle_button_click(name),
                                            fg_color="transparent", hover_color="#48464f")
            toggle_edit_btn.pack(pady=2)
            remove_btn = ctk.CTkButton(controls_frame, text="", width=30,
                                       image=ctk.CTkImage(dark_image=Image.open("images/trash.png"), size=(25, 25)),
                                       command=lambda p=product: self.remove_product(p), fg_color="transparent",
                                       hover_color="#48464f")
            remove_btn.pack(pady=2)
            cancel_btn = ctk.CTkButton(controls_frame, text="", width=30, fg_color="transparent", hover_color="#48464f",
                                       image=ctk.CTkImage(dark_image=Image.open("images/close (1).png"), size=(20, 20)),
                                       command=lambda name=product_name: self.exit_edit_mode(name))
            self.product_widgets[product_name] = {
                'original_product': product, 'display_frame': display_frame, 'edit_frame': edit_frame,
                'name_entry': name_entry, 'desc_entry': desc_entry, 'price_entry': price_entry,
                'toggle_edit_btn': toggle_edit_btn, 'remove_btn': remove_btn, 'cancel_btn': cancel_btn
            }

    def filter_products(self, category):
        if category == "Home":
            filtered = self.products_data
        else:
            filtered = [p for p in self.products_data if p["category"].strip().lower() == category.strip().lower()]
        self.display_products(filtered)

    def sign_out(self):
        messagebox.showinfo("Goodbye", "See you soon, Admin!")

        self.controller.show_frame(LoginFrame)

    def create_add_product_widgets(self, parent):
        self.add_product_frame = ctk.CTkFrame(parent, fg_color="#3b3b3b", corner_radius=8)
        self.add_product_frame.grid_columnconfigure(0, weight=1)
        entry_frame = ctk.CTkFrame(self.add_product_frame, fg_color="transparent")
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.new_name_entry = ctk.CTkEntry(entry_frame, placeholder_text="Product Name")
        self.new_name_entry.pack(fill="x", expand=True, pady=2)
        self.new_desc_entry = ctk.CTkEntry(entry_frame, placeholder_text="Description")
        self.new_desc_entry.pack(fill="x", expand=True, pady=2)
        self.new_price_entry = ctk.CTkEntry(entry_frame, placeholder_text="Price")
        self.new_price_entry.pack(fill="x", expand=True, pady=2)
        self.new_category_entry = ctk.CTkComboBox(entry_frame, values=self.categories_list[1:])
        self.new_category_entry.pack(fill="x", expand=True, pady=2)
        self.new_category_entry.set("Select Category")
        button_frame = ctk.CTkFrame(self.add_product_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        confirm_btn = ctk.CTkButton(button_frame, text="", fg_color="transparent", hover_color="#48464f",
                                    image= ctk.CTkImage(dark_image=Image.open("images/check.png"), size=(25, 25)),command=self.confirm_add_product)
        confirm_btn.pack(pady=2)
        cancel_btn = ctk.CTkButton(button_frame, text="", fg_color="transparent", hover_color="#48464f",
                                   image=ctk.CTkImage(dark_image=Image.open("images/close (1).png"), size=(20, 20)), command=self.toggle_add_product_frame)
        cancel_btn.pack(pady=2)

    def toggle_add_product_frame(self):
        if self.add_product_frame.winfo_viewable():
            self.add_product_frame.pack_forget()
        else:
            self.add_product_frame.pack(after=self.title_frame, fill="x", padx=10, pady=10)

    def confirm_add_product(self):
        name = self.new_name_entry.get()
        desc = self.new_desc_entry.get()
        price_str = self.new_price_entry.get()
        category = self.new_category_entry.get()
        if not all([name, desc, price_str, category != "Select Category"]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
            return
        new_product = {"name": name, "description": desc, "price": price, "orders": 0, "category": category}
        self.products_data.append(new_product)
        with open("products.json", "w") as f:
            json.dump(self.products_data, f, indent=4)
        self.display_products(self.products_data)
        self.new_name_entry.delete(0, "end")
        self.new_desc_entry.delete(0, "end")
        self.new_price_entry.delete(0, "end")
        self.new_category_entry.set("Select Category")
        self.toggle_add_product_frame()

    def on_toggle_button_click(self, product_name):
        if self.editing_product_name == product_name:
            self.save_product_changes(product_name)
        elif self.editing_product_name is None:
            self.enter_edit_mode(product_name)
        else:
            messagebox.showinfo("Action Required",
                                f"Please save or cancel your changes for\n'{self.editing_product_name}' first.")

    def enter_edit_mode(self, product_name):
        self.editing_product_name = product_name
        widgets = self.product_widgets[product_name]
        widgets['toggle_edit_btn'].configure(image= ctk.CTkImage(dark_image=Image.open("images/check.png"), size=(25, 25)))
        widgets['display_frame'].pack_forget()
        widgets['remove_btn'].pack_forget()
        widgets['edit_frame'].pack(side="left", fill="x", expand=True, padx=10, pady=5)
        widgets['cancel_btn'].pack(pady=2)
        product = widgets['original_product']
        widgets['name_entry'].delete(0, 'end')
        widgets['name_entry'].insert(0, product['name'])
        widgets['desc_entry'].delete(0, 'end')
        widgets['desc_entry'].insert(0, product['description'])
        widgets['price_entry'].delete(0, 'end')
        widgets['price_entry'].insert(0, product['price'])

    def exit_edit_mode(self, product_name):
        self.editing_product_name = None
        widgets = self.product_widgets[product_name]
        widgets['toggle_edit_btn'].configure(image=ctk.CTkImage(dark_image=Image.open("images/pencil.png"), size=(25, 25)))
        widgets['edit_frame'].pack_forget()
        widgets['cancel_btn'].pack_forget()
        widgets['display_frame'].pack(side="left", fill="x", expand=True, padx=10, pady=5)
        widgets['remove_btn'].pack(pady=2)

    def save_product_changes(self, old_product_name):
        widgets = self.product_widgets[old_product_name]
        try:
            new_price = float(widgets['price_entry'].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a valid number.")
            return
        for product in self.products_data:
            if product['name'] == old_product_name:
                product['name'], product['description'], product['price'] = widgets['name_entry'].get(), widgets[
                    'desc_entry'].get(), new_price
                break
        with open("products.json", "w") as f:
            json.dump(self.products_data, f, indent=4)
        self.editing_product_name = None
        self.display_products(self.products_data)

    def remove_product(self, product_to_remove):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove {product_to_remove['name']}?"):
            self.products_data = [p for p in self.products_data if p['name'] != product_to_remove['name']]
            with open("products.json", "w") as f: json.dump(self.products_data, f, indent=4)
            self.display_products(self.products_data)

    def display_products(self, products):
        for widget in self.products_frame.winfo_children(): widget.destroy()
        self.product_widgets.clear()
        for product in products:
            product_name = product['name']
            product_card = ctk.CTkFrame(self.products_frame, fg_color="#3b3b3b", corner_radius=8)
            product_card.pack(fill="x", padx=5, pady=5)
            display_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            display_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            ctk.CTkLabel(display_frame, text=product["name"], font=("Segoe UI", 16, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(display_frame, text=product["description"], font=("Segoe UI", 12), anchor="w").pack(fill="x")
            ctk.CTkLabel(display_frame, text=f"${product['price']}", font=("Segoe UI", 14, "bold"), anchor="w").pack(
                fill="x", pady=(5, 0))
            edit_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            name_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            name_entry.pack(fill="x", pady=2)
            desc_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            desc_entry.pack(fill="x", pady=2)
            price_entry = ctk.CTkEntry(edit_frame, font=("Segoe UI", 12))
            price_entry.pack(fill="x", pady=2)
            controls_frame = ctk.CTkFrame(product_card, fg_color="transparent")
            controls_frame.pack(side="right", padx=10)
            toggle_edit_btn = ctk.CTkButton(controls_frame, text="", width=30, image=ctk.CTkImage(dark_image=Image.open("images/pencil.png"), size=(25, 25)),
                                            command=lambda name=product_name: self.on_toggle_button_click(name),
                                            fg_color="transparent", hover_color="#48464f")
            toggle_edit_btn.pack(pady=2)
            remove_btn = ctk.CTkButton(controls_frame, text="", width=30,
                                       image=ctk.CTkImage(dark_image=Image.open("images/trash.png"), size=(25, 25)),
                                       command=lambda p=product: self.remove_product(p), fg_color="transparent",
                                       hover_color="#48464f")
            remove_btn.pack(pady=2)
            cancel_btn = ctk.CTkButton(controls_frame, text="", width=30, fg_color="transparent", hover_color="#48464f",
                                       image=ctk.CTkImage(dark_image=Image.open("images/close (1).png"), size=(20, 20)),
                                       command=lambda name=product_name: self.exit_edit_mode(name))
            self.product_widgets[product_name] = {
                'original_product': product, 'display_frame': display_frame, 'edit_frame': edit_frame,
                'name_entry': name_entry, 'desc_entry': desc_entry, 'price_entry': price_entry,
                'toggle_edit_btn': toggle_edit_btn, 'remove_btn': remove_btn, 'cancel_btn': cancel_btn
            }

    def filter_products(self, category):
        if category == "Home":
            filtered = self.products_data
        else:
            filtered = [p for p in self.products_data if p["category"].strip().lower() == category.strip().lower()]
        self.display_products(filtered)