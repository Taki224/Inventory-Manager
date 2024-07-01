import tkinter as tk
from tkinter import messagebox
# import helper_methods.hasher as hasher

import json

import frames.mainPage as mainPage
import requests

from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()

def open():
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        URL = "http://127.0.0.1:7890/employee/login"
        PARAMS = {'username':username, 'password':hash(password)}
        r = requests.post(url = URL, params = PARAMS)
        # Check if username and password are valid
        try:
            response_data = r.json()  # Attempt to decode the JSON response
            # Check if username and password are valid
            if response_data.get('message') == "Login successful!":
                window.destroy()
                userdetails = response_data.get('user')
                mainPage.open(userdetails)
            else:
                messagebox.showerror("Login", "Invalid username or password or user is suspended!")

        except json.JSONDecodeError:
            messagebox.showerror("Login", "Invalid response from the server!")

        except Exception as e:
            messagebox.showerror("Login", f"An error occurred: {str(e)}")

    # Create the main window
    window = tk.Tk()
    window.title("Login")

    w = 500
    ws = window.winfo_screenwidth()
    h = 250
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Create and pack the username label and entry
    username_label = tk.Label(window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(window)
    username_entry.pack()
    username_entry.focus_set()

    # Create and pack the password label and entry
    password_label = tk.Label(window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    # Create and pack the login button
    login_button = tk.Button(window, text="Login", command=validate_login)
    login_button.pack()

    window.bind('<Return>', lambda event: login_button.invoke())


    # Run the main event loop
    window.mainloop()

if __name__ == "__main__":
    open()