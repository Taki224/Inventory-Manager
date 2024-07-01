import random
import requests
import string
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()


def open(mainframe, userdetails):
    def create_new_user():
        username = username_entry.get()
        email = email_entry.get()
        is_admin = admin_var.get()

        # Validate inputs
        if not username or not email:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        password = generate_random_password()

        url = "http://127.0.0.1:7890/employee/create"
        params = {'username': username, 'password': hash(password), 'email': email, 'is_admin': is_admin,
                  'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.post(url=url, params=params)
        if r.status_code != 200:
            messagebox.showerror("Error", "An error occurred while creating the user.")
            return
        response_data = r.json()
        if response_data.get('message') == "username_exists":
            messagebox.showerror("Error", "Username already exists!")
            return
        messagebox.showinfo("Success", f"User created successfully with password:{password}!")

        # Clear the form fields
        username_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        admin_checkbox.deselect()

    def generate_random_password():
        # Generate a random password of 6 numbers
        password = ''.join(random.choices(string.digits, k=6))
        return password

    def validate_email(email):
        # Simple email format check using regular expression
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    root = tk.Toplevel(mainframe)
    root.title("New User")

    # Username
    username_label = ttk.Label(root, text="Username:")
    username_label.pack()
    username_entry = ttk.Entry(root)
    username_entry.pack()

    # Email
    email_label = ttk.Label(root, text="Email:")
    email_label.pack()
    email_entry = ttk.Entry(root)
    email_entry.pack()

    # Admin Checkbox
    admin_var = tk.BooleanVar(value=False)
    admin_checkbox = tk.Checkbutton(root, text="Admin", variable=admin_var)
    admin_checkbox.pack()

    # Create User Button
    create_button = ttk.Button(root, text="Create User", command=create_new_user)
    create_button.pack()

    root.mainloop()
