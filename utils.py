import tkinter as tk
from tkinter import ttk
from theme import *
import customtkinter as ctk
from PIL import Image
import json
import os

# Standardized the filename to the one used in your other files
USERS_FILE = "user_data.json"


def load_users():
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return []
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_users(users_list):
    """Saves the entire list of users back to the file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users_list, f, indent=4)


def validate_login(email, password):
    if email == "admin@gmail.com" and password == "admin123":
        return "admin"
    users = load_users()
    for user in users:
        # --- FIXED: Correctly checks the email field ---
        if user.get("email") == email and user.get("password") == password:
            return user
    return None


# ===============   SORTING & SEARCHING   ======================

# --- IMPROVED: Now handles descending order directly ---
def merge_sort(arr, key, reverse=False):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)
    return merge(left, right, key, reverse)


def merge(left, right, key, reverse):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Comparison logic changes based on the 'reverse' flag
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


# --- IMPROVED: Case-insensitive search, returns the item itself ---
def binary_search(sorted_arr, target, key):
    low, high = 0, len(sorted_arr) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_arr[mid])

        # Case-insensitive comparison
        if mid_val.lower() < target.lower():
            low = mid + 1
        elif mid_val.lower() > target.lower():
            high = mid - 1
        else:
            return sorted_arr[mid]  # Return the found item
    return None  # Return None if not found
# ===============   CART TOTAL CALCULATION   ===================


def calculate_cart_total(cart_items, delivery_fee=50):
    """
    cart_items: list of dicts [{ "name": "item1", "price": 100 }, ...]
    """
    total = sum(item["price"] for item in cart_items)
    return {
        "cart_total": total,
        "delivery": delivery_fee,
        "final_total": total + delivery_fee
    }
