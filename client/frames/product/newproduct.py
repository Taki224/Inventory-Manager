import requests
import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox


def open(main_window, userdetails, tablerefresh):
    def add_product():
        barcode = barcode_entry.get()
        name = name_entry.get()
        quantity = quantity_entry.get()
        category = category_combobox.get()
        expiration_date = expiration_date_entry.get()
        no_expiration = no_expiration_var.get()
        notify_low_quantity = notify_low_quantity_var.get()
        notify_near_expiration = notify_near_expiration_var.get()
        near_expiration = near_e_entry.get()
        low_q = low_q_entry.get()
        new_product = {
            "barcode": barcode,
            "name": name,
            "quantity": quantity,
            "category": category,
            "expiration": expiration_date if not no_expiration else "-1",
            "notifexp": near_expiration if notify_near_expiration else "-1",
            "notifquan": low_q if notify_low_quantity else "-1"
        }
        url = "http://127.0.0.1:7890/product/create"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        data = {'new_product': new_product}
        r = requests.post(url=url, params=params, json=data)
        if r.status_code == 200:
            print(json.loads(r.text))
            if json.loads(r.text)['success'] == False:
                messagebox.showwarning("Warning", "Product with this barcode and expiration date already exists!")
                return
            messagebox.showinfo("Success", "Product added successfully!")
            tablerefresh()
            # Clear the form fields
            barcode_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            category_combobox.current(0)
            expiration_date_entry.delete(0, tk.END)
            expiration_date_entry.insert(0, "YYYY.MM.DD")
            no_expiration_check.deselect()
            notify_low_quantity_check.deselect()
            notify_near_expiration_check.deselect()
        else:
            messagebox.showerror("Error", "Error adding product!")

    def no_expiration_check_changed():
        if no_expiration_var.get():
            expiration_date_entry.delete(0, tk.END)
            expiration_date_entry.config(state=tk.DISABLED)
            notify_near_expiration_check.deselect()
            notify_near_expiration_check.config(state=tk.DISABLED)
            near_e_label.grid_remove()
            near_e_entry.grid_remove()
        else:
            expiration_date_entry.config(state=tk.NORMAL)
            expiration_date_entry.insert(0, "YYYY.MM.DD")
            notify_near_expiration_check.config(state=tk.NORMAL)

    def near_expiration_change():
        if notify_near_expiration_var.get():
            near_e_label.grid(row=7, column=2)
            near_e_entry.grid(row=7, column=3)
        else:
            near_e_entry.grid_remove()
            near_e_label.grid_remove()

    def low_quantity_change():
        if notify_low_quantity_var.get():
            low_q_label.grid(row=6, column=2)
            low_q_entry.grid(row=6, column=3)
        else:
            low_q_entry.grid_remove()
            low_q_label.grid_remove()

    def load_categories():
        URL = "http://127.0.0.1:7890/product/categories"
        params = {'auth_user': userdetails.get('username'), 'auth_password': userdetails.get('password')}
        r = requests.get(url=URL, params=params)
        categories = []
        for category in json.loads(r.text)['categories']:
            categories.append(category['name'])
        category_combobox['values'] = categories

    root = tk.Toplevel(main_window)
    root.title("Add New Product")

    w = 700
    ws = root.winfo_screenwidth()
    h = 250
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Center the form components
    root.columnconfigure(0, weight=1)
    root.columnconfigure(2, weight=1)

    # Barcode
    barcode_label = ttk.Label(root, text="Barcode:")
    barcode_label.grid(row=0, column=1)
    barcode_entry = ttk.Entry(root)
    barcode_entry.grid(row=0, column=2)

    # Name
    name_label = ttk.Label(root, text="Name:")
    name_label.grid(row=1, column=1)
    name_entry = ttk.Entry(root)
    name_entry.grid(row=1, column=2)

    # Quantity
    quantity_label = ttk.Label(root, text="Quantity:")
    quantity_label.grid(row=2, column=1)
    quantity_entry = ttk.Entry(root)
    quantity_entry.grid(row=2, column=2)

    # Category
    category_label = ttk.Label(root, text="Category:")
    category_label.grid(row=3, column=1)

    category_combobox = ttk.Combobox(root)
    category_combobox.grid(row=3, column=2)
    load_categories()
    category_combobox.current(0)

    # Expiration Date
    expiration_date_label = ttk.Label(root, text="Expiration Date:")
    expiration_date_label.grid(row=4, column=1)
    expiration_date_entry = ttk.Entry(root)
    expiration_date_entry.grid(row=4, column=2)
    expiration_date_entry.insert(0, "YYYY.MM.DD")

    # No Expiration Checkbox
    no_expiration_var = tk.BooleanVar(value=False)
    no_expiration_check = tk.Checkbutton(root, text="No Expiration", variable=no_expiration_var,
                                         command=no_expiration_check_changed)
    # no_expiration_check.deselect()  # set the checkbutton state to unchecked
    no_expiration_check.grid(row=5, column=1, columnspan=2, sticky="w")

    # Notify Low Quantity Checkbox
    notify_low_quantity_var = tk.BooleanVar(value=False)
    notify_low_quantity_check = tk.Checkbutton(root, text="Notify Low Quantity", variable=notify_low_quantity_var,
                                               command=low_quantity_change)
    notify_low_quantity_check.grid(row=6, column=1, columnspan=2, sticky="w")

    # Low quantity entry
    low_q_label = ttk.Label(root, text="Under this quantity:")
    low_q_entry = ttk.Entry(root)

    # Notify Near Expiration Checkbox
    notify_near_expiration_var = tk.BooleanVar(value=False)
    notify_near_expiration_check = tk.Checkbutton(root, text="Notify Near Expiration",
                                                  variable=notify_near_expiration_var, command=near_expiration_change)
    notify_near_expiration_check.grid(row=7, column=1, columnspan=2, sticky="w")

    # Near expiration entry
    near_e_label = ttk.Label(root, text="Days before expiration:")
    near_e_entry = ttk.Entry(root)

    # Add Product Button
    add_button = ttk.Button(root, text="Add Product", command=add_product)
    add_button.grid(row=8, column=1, columnspan=2)

    root.mainloop()
