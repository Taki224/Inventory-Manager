import requests
import tkinter as tk
from tkinter import ttk

import frames.selector.productselector as productselector
import json
from tkinter import messagebox


def open(main_window, userdetails):
    global selected_product_id
    selected_product_id = None

    def delete_product():
        global selected_product_id
        url = "http://127.0.0.1:7890/product/delete/" + str(selected_product_id)
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.delete(url=url, params=params)
        print(r.text)
        if r.status_code == 200:
            messagebox.showinfo("Success", "Product deleted successfully!")
            root.destroy()

    def load_product():
        productselector.ProductSelector(main_window, userdetails, load_product_callback)

    def load_product_callback(selected_product):
        infoText.grid_remove()
        global selected_product_id
        selected_product_id = selected_product
        url = "http://127.0.0.1:7890/product/" + str(selected_product_id)
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        print(r.text)
        product_data = json.loads(r.text)['product']

        infoText.config(
            text=f"ID:{product_data['id']}\nBarcode:{product_data['barcode']}\nProduct:{product_data['name']}\nQuantity:{product_data['quantity']}\n")  # = ttk.Label(root, text=f"ID:{product_data['id']}\nBarcode:{product_data['barcode']}\nProduct:{product_data['name']}\nQuantity:{product_data['quantity']}\n")
        infoText.grid(row=1, column=0, columnspan=2)
        delete_button.grid_remove()
        delete_button.grid(row=2, column=0, columnspan=2)
        delete_button.configure(state="normal")

    root = tk.Toplevel(main_window)
    root.title("Delete Product")

    w = 300
    ws = root.winfo_screenwidth()
    h = 250
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Center the form components
    root.columnconfigure(0, weight=1)

    load_text = ttk.Label(root, text="Load Product:")
    load_text.grid(row=0, column=0)
    load_button = ttk.Button(root, text="Load", command=load_product)
    load_button.grid(row=0, column=1)

    infoText = ttk.Label(root)

    # Delete Product Button
    delete_button = ttk.Button(root, text="Delete Product", command=delete_product)
    delete_button.grid(row=1, column=0, columnspan=2)
    delete_button.configure(state="disabled")

    root.mainloop()
