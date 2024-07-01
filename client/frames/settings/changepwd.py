import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()

def open(mainframe, userdetails):
    def change_password():
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()
        new_password_again = new_password_again_entry.get()
        if new_password != new_password_again:
            messagebox.showerror("Error", "New passwords do not match!")
            return
        if userdetails['password'] != hash(old_password):
            messagebox.showerror("Error", "Old password is incorrect!")
            return
        url = "http://127.0.0.1:7890/employee/changepassword"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'],
                  'old_password': hash(old_password), 'new_password': hash(new_password)}
        r = requests.put(url=url, params=params)
        if r.status_code == 200:
            messagebox.showinfo("Success", "Password changed successfully!")
            old_password_entry.delete(0, tk.END)
            new_password_entry.delete(0, tk.END)
            new_password_again_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "An error occurred while changing the password.")

    root = tk.Toplevel(mainframe)
    root.title("Change Password")

    # Center the form components
    root.columnconfigure(0, weight=1)

    # Old Password
    old_password_label = ttk.Label(root, text="Old Password:")
    old_password_label.grid(row=0, column=0)
    old_password_entry = ttk.Entry(root, show="*")
    old_password_entry.grid(row=0, column=1)

    # New Password
    new_password_label = ttk.Label(root, text="New Password:")
    new_password_label.grid(row=1, column=0)
    new_password_entry = ttk.Entry(root, show="*")
    new_password_entry.grid(row=1, column=1)

    # New Password again
    new_password_again_label = ttk.Label(root, text="New Password again:")
    new_password_again_label.grid(row=2, column=0)
    new_password_again_entry = ttk.Entry(root, show="*")
    new_password_again_entry.grid(row=2, column=1)

    # Change Password Button
    change_button = ttk.Button(root, text="Change Password", command=change_password)
    change_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()
