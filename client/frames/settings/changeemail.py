import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def open(mainframe, userdetails):
    def change_email_address():
        new_email = email_entry.get()
        url = "http://127.0.0.1:7890/employee/changeemail"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'],
                  'new_email': new_email}
        r = requests.put(url=url, params=params)
        if r.status_code == 200:
            messagebox.showinfo("Success", "Email Address Changed")
            email_entry.delete(0, tk.END)

    root = tk.Toplevel(mainframe)
    root.title("Change Email Address")

    # Center the form components
    root.columnconfigure(0, weight=1)

    # New Email Address
    email_label = ttk.Label(root, text="New Email Address:")
    email_label.grid(row=0, column=0)
    email_entry = ttk.Entry(root)
    email_entry.grid(row=0, column=1)

    # Change Email Address Button
    change_button = ttk.Button(root, text="Change Email Address", command=change_email_address)
    change_button.grid(row=1, column=0, columnspan=2)

    root.mainloop()
