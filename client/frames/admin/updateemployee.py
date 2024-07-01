import random
import string
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames.selector.employeeselector as employeeselector

import json

from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()

def open(mainframe, userdetails):
    selecteduser = None
    url = "http://127.0.0.1:7890/employees"
    params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
    r = requests.get(url=url, params=params)
    employeesjson = json.loads(r.text)
    employees = []
    for employee in employeesjson:
        employees.append(f"{employee['id']} - {employee['username']}")

    def clearSelection():
        email_entry.delete(0, tk.END)
        permission_dropdown.set("")
        generate_password_button.config(state="disabled")
        email_entry.config(state="disabled")
        update_email_button.config(state="disabled")
        update_permission_button.config(state="disabled")
        permission_dropdown.config(state="disabled")

    def load_employee_callback(selected_employee_id):
        print(selected_employee_id)
        url = "http://127.0.0.1:7890/employee/" + selected_employee_id
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        employeejson = json.loads(r.text)
        print(employeejson)
        global selecteduser
        selecteduser = selected_employee_id
        generate_password_button.config(state="normal")
        email_entry.config(state="normal")
        update_email_button.config(state="normal")
        update_permission_button.config(state="normal")
        permission_dropdown.config(state="normal")
        email_entry.delete(0, tk.END)
        email_entry.insert(0, employeejson.get('email'))
        permission_dropdown.current(int(employeejson.get('permission')))

    def load_employee():
        employeeselector.EmployeeSelector(mainframe, userdetails, load_employee_callback)

    def generate_password():
        global selecteduser
        password = ''.join(random.choices(string.digits, k=6))
        url = "http://127.0.0.1:7890/employee/" + selecteduser
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'], 'password': hash(password)}
        r = requests.put(url=url, params=params)
        if r.status_code != 200:
            messagebox.showerror("Error", "An error occurred while updating the user.")
            return
        messagebox.showinfo("Success", f"User password updated successfully! New password: {password}")
        clearSelection()

    def update_email():
        new_email = email_entry.get()
        global selecteduser
        url = "http://127.0.0.1:7890/employee/" + selecteduser
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'], 'email': new_email}
        r = requests.put(url=url, params=params)
        if r.status_code != 200:
            messagebox.showerror("Error", "An error occurred while updating the user.")
            return
        messagebox.showinfo("Success", f"User email updated successfully!")
        clearSelection()

    def update_permission():
        new_permission = permission_dropdown.current()
        global selecteduser
        url = "http://127.0.0.1:7890/employee/" + selecteduser
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'],
                  'permission': new_permission}
        r = requests.put(url=url, params=params)
        if r.status_code != 200:
            messagebox.showerror("Error", "An error occurred while updating the user.")
            return
        messagebox.showinfo("Success", f"User permission updated successfully!")
        clearSelection()

    root = tk.Toplevel(mainframe)
    root.title("Update Employee")

    # Employee Dropdown
    employee_label = ttk.Label(root, text="Select Employee:")
    employee_label.grid(row=0, column=0)

    # Load Button
    load_button = ttk.Button(root, text="Load", command=load_employee)
    load_button.grid(row=0, column=1)

    # Password Field
    password_label = ttk.Label(root, text="Password:")
    password_label.grid(row=1, column=0)
    generate_password_button = ttk.Button(root, text="Generate New Password", command=generate_password)
    generate_password_button.grid(row=1, column=1)
    generate_password_button.config(state="disabled")

    # Email Field
    email_label = ttk.Label(root, text="Email:")
    email_label.grid(row=2, column=0)
    email_entry = ttk.Entry(root, state="disabled")
    email_entry.grid(row=2, column=1)
    update_email_button = ttk.Button(root, text="Change Email", command=update_email)
    update_email_button.grid(row=2, column=2)
    update_email_button.config(state="disabled")

    # Permission Field
    permission_label = ttk.Label(root, text="Permission:")
    permission_label.grid(row=3, column=0)
    permission_dropdown = ttk.Combobox(root, state="disabled", values=["User", "Admin", "Suspended"])
    permission_dropdown.grid(row=3, column=1)
    update_permission_button = ttk.Button(root, text="Change Permission", command=update_permission)
    update_permission_button.grid(row=3, column=2)
    update_permission_button.config(state="disabled")

    root.mainloop()
