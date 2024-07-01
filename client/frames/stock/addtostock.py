import json

import requests
import tkinter as tk
from tkinter import ttk
import frames.selector.productselector as productselector
from tkinter import messagebox


def open(mainframe, userdetails):
    global seleted_id
    selected_id = None

    def add_to_stock():
        global selected_id
        if selected_id is None:
            infoText.config(text="Please select a product!")
            return
        if quantity_entry.get() == "":
            infoText.config(text="Please enter a quantity!")
            return
        url = "http://127.0.0.1:7890/product/" + str(selected_id) + "/updatestock"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'],
                  'change': quantity_entry.get()}
        r = requests.put(url=url, params=params)
        if r.status_code == 200:
            if json.loads(r.text)['success']:
                messagebox.showinfo("Success", "Product added to stock!")
                selected_id = None
                infoText.config(text="")
                quantity_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Quantity not right!")

    def load_product():
        productselector.ProductSelector(mainframe, userdetails, load_product_callback)

    def load_product_callback(selected_product):
        global selected_id
        selected_id = selected_product
        url = "http://127.0.0.1:7890/product/" + str(selected_product)
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        print(r.text)
        product_data = json.loads(r.text)['product']

        infoText.config(
            text=f"ID:{product_data['id']}\nBarcode:{product_data['barcode']}\nProduct:{product_data['name']}\nQuantity:{product_data['quantity']}\n")
        infoText.grid(row=1, column=0, columnspan=2)
        add_button.grid_remove()
        add_button.grid(row=3, column=0, columnspan=2)
        add_button.configure(state="normal")

        quantity_label.grid(row=2, column=0)
        quantity_entry.grid(row=2, column=1)

    root = tk.Toplevel(mainframe)
    root.title("Add to Stock")

    # Center the form components
    root.columnconfigure(0, weight=1)

    # Product ID
    load_button = ttk.Button(root, text="Load", command=load_product)
    load_button.grid(row=0, column=1)

    infoText = ttk.Label(root)

    # Quantity
    quantity_label = ttk.Label(root, text="Quantity:")
    quantity_label.grid(row=1, column=0)
    quantity_entry = ttk.Entry(root)
    quantity_entry.grid(row=1, column=1)

    # Add to Stock Button
    add_button = ttk.Button(root, text="Add to Stock", command=add_to_stock)
    add_button.grid(row=2, column=0, columnspan=2)

    root.mainloop()
