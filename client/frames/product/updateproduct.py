import requests
import tkinter as tk
from tkinter import ttk
import frames.selector.productselector as productselector
import json
from tkinter import messagebox

from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()


def open(userdetails, main_window):
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
        return categories, json.loads(r.text)['categories']

    def load_product():
        productselector.ProductSelector(main_window, userdetails, load_product_callback)

    global selected_product_id
    selected_product_id = None

    def load_product_callback(selected_product):
        clear_form()
        global selected_product_id
        selected_product_id = selected_product
        # Retrieve the product data from the database
        url = "http://127.0.0.1:7890/product/" + str(selected_product_id)
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        print(r.text)

        product_data = json.loads(r.text)['product']

        update_button.config(state=tk.NORMAL)

        name_entry.config(state=tk.NORMAL)
        name_entry.delete(0, tk.END)
        name_entry.insert(0, product_data["name"])

        quantity_entry.config(state=tk.NORMAL)
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, product_data["quantity"])

        category_combobox.config(state=tk.NORMAL)
        for c in load_categories()[1]:
            if c['id'] == product_data['category']:
                category_combobox.set(c['name'])

        notify_near_expiration_check.config(state=tk.NORMAL)
        if product_data["notifexp"] != -1:
            near_e_label.grid(row=7, column=2)
            near_e_entry.grid(row=7, column=3)
            notify_near_expiration_check.select()
            near_e_entry.delete(0, tk.END)
            near_e_entry.insert(0, product_data["notifexp"])
        else:
            no_expiration_check.deselect()
            near_e_entry.grid_remove()
            near_e_label.grid_remove()

        notify_low_quantity_check.config(state=tk.NORMAL)
        if product_data["notifquan"] != -1:
            low_q_label.grid(row=6, column=2)
            low_q_entry.grid(row=6, column=3)
            notify_low_quantity_check.select()
            low_q_entry.delete(0, tk.END)
            low_q_entry.insert(0, product_data["notifquan"])
        else:
            notify_low_quantity_check.deselect()
            low_q_entry.grid_remove()
            low_q_label.grid_remove()

        no_expiration_check.config(state=tk.NORMAL)
        if product_data["expiration"] == "-1":
            no_expiration_check.select()
            expiration_date_entry.delete(0, tk.END)
            expiration_date_entry.config(state=tk.DISABLED)
        else:
            expiration_date_entry.config(state=tk.NORMAL)
            expiration_date_entry.delete(0, tk.END)
            expiration_date_entry.insert(0, product_data["expiration"])

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

    def clear_form():
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        category_combobox.set("")
        expiration_date_entry.delete(0, tk.END)
        no_expiration_check.deselect()
        notify_low_quantity_check.deselect()
        notify_near_expiration_check.deselect()
        near_e_label.grid_remove()
        near_e_entry.grid_remove()
        low_q_label.grid_remove()
        low_q_entry.grid_remove()
        global selected_product_id
        selected_product_id = None

    def update_product():
        global selected_product_id
        if selected_product_id is None:
            messagebox.showerror("Error", "Please select a product first!")
            return

        name = name_entry.get()
        quantity = quantity_entry.get()
        category = category_combobox.get()
        expiration_date = expiration_date_entry.get()
        no_expiration = no_expiration_var.get()
        notify_low_quantity = notify_low_quantity_var.get()
        notify_near_expiration = notify_near_expiration_var.get()
        near_expiration = near_e_entry.get()
        low_q = low_q_entry.get()
        product = {
            "name": name,
            "quantity": quantity,
            "category": category,
            "expiration": expiration_date if not no_expiration else "-1",
            "notifexp": near_expiration if notify_near_expiration else "-1",
            "notifquan": low_q if notify_low_quantity else "-1"
        }
        url = "http://127.0.0.1:7890/product/update" + "/" + str(selected_product_id)
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        data = {'product': product}
        r = requests.put(url=url, params=params, json=data)
        if r.status_code == 200:
            print(json.loads(r.text))
            if json.loads(r.text)['success'] == False:
                messagebox.showwarning("Warning", "Product with this barcode and expiration date already exists!")
                return
            messagebox.showinfo("Success", "Product updated successfully!")
        clear_form()

    root = tk.Toplevel(main_window)
    root.title("Update Product")

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
    barcode_label = ttk.Label(root, text="Product:")
    barcode_label.grid(row=0, column=0)

    # Load Button
    load_button = ttk.Button(root, text="Load", command=load_product)
    load_button.grid(row=0, column=1)

    # Name
    name_label = ttk.Label(root, text="Name:")
    name_label.grid(row=1, column=0)
    name_entry = ttk.Entry(root)
    name_entry.grid(row=1, column=1)
    name_entry.config(state="disabled")

    # Quantity
    quantity_label = ttk.Label(root, text="Quantity:")
    quantity_label.grid(row=2, column=0)
    quantity_entry = ttk.Entry(root)
    quantity_entry.grid(row=2, column=1)
    quantity_entry.config(state="disabled")

    # Category
    category_label = ttk.Label(root, text="Category:")
    category_label.grid(row=3, column=0)
    categories = load_categories()[0]
    category_combobox = ttk.Combobox(root, values=categories)
    category_combobox.grid(row=3, column=1)
    category_combobox.config(state="disabled")

    # Expiration Date
    expiration_date_label = ttk.Label(root, text="Expiration Date:")
    expiration_date_label.grid(row=4, column=0)
    expiration_date_entry = ttk.Entry(root)
    expiration_date_entry.grid(row=4, column=1)
    expiration_date_entry.config(state="disabled")

    # No Expiration Checkbox
    no_expiration_var = tk.BooleanVar()
    no_expiration_check = tk.Checkbutton(root, text="No Expiration", variable=no_expiration_var,
                                         command=no_expiration_check_changed)
    no_expiration_check.grid(row=5, column=0, columnspan=2, sticky="w")
    no_expiration_check.deselect()
    no_expiration_check.config(state="disabled")

    # Notify Low Quantity Checkbox
    notify_low_quantity_var = tk.BooleanVar()
    notify_low_quantity_check = tk.Checkbutton(root, text="Notify Low Quantity", variable=notify_low_quantity_var,
                                               command=low_quantity_change)
    notify_low_quantity_check.grid(row=6, column=0, columnspan=2, sticky="w")
    notify_low_quantity_check.deselect()
    notify_low_quantity_check.config(state="disabled")

    # Low quantity entry
    low_q_label = ttk.Label(root, text="Under this quantity:")
    low_q_entry = ttk.Entry(root)

    # Notify Near Expiration Checkbox
    notify_near_expiration_var = tk.BooleanVar()
    notify_near_expiration_check = tk.Checkbutton(root, text="Notify Near Expiration",
                                                  variable=notify_near_expiration_var, command=near_expiration_change)
    notify_near_expiration_check.grid(row=7, column=0, columnspan=2, sticky="w")
    notify_near_expiration_check.deselect()
    notify_near_expiration_check.config(state="disabled")

    # Near expiration entry
    near_e_label = ttk.Label(root, text="Days before expiration:")
    near_e_entry = ttk.Entry(root)

    # Update Product Button
    update_button = ttk.Button(root, text="Update Product", command=update_product)
    update_button.grid(row=8, column=0, columnspan=2)
    update_button.config(state="disabled")

    root.mainloop()
