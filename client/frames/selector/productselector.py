from tkinter import *
from tkinter import ttk

import requests
import json


class ProductSelector:
    def __init__(self, mainframe, userdetails, select_product_callback):
        self.root = Toplevel(mainframe)
        self.root.title("Product Selector")
        self.userdetails = userdetails
        self.select_product_callback = select_product_callback

        margin = Frame(self.root)
        margin.pack(padx=30, pady=30)

        self.table = ttk.Treeview(margin)

        self.table['columns'] = (
            'ID', 'Barcode', 'Name', 'Quantity', 'Category', 'Expiry Date', 'Expiry Notification',
            'Quantity Notification')

        self.table.column("#0", width=0, stretch=NO)
        self.table.column("ID", anchor=CENTER, width=60)
        self.table.column("Barcode", anchor=CENTER, width=120)
        self.table.column("Name", anchor=CENTER, width=120)
        self.table.column("Quantity", anchor=CENTER, width=120)
        self.table.column("Category", anchor=CENTER, width=120)
        self.table.column("Expiry Date", anchor=CENTER, width=120)
        self.table.column("Expiry Notification", anchor=CENTER, width=180)
        self.table.column("Quantity Notification", anchor=CENTER, width=180)

        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("ID", text="ID", anchor=CENTER)
        self.table.heading("Barcode", text="Barcode", anchor=CENTER)
        self.table.heading("Name", text="Name", anchor=CENTER)
        self.table.heading("Quantity", text="Quantity", anchor=CENTER)
        self.table.heading("Category", text="Category", anchor=CENTER)
        self.table.heading("Expiry Date", text="Expiry Date", anchor=CENTER)
        self.table.heading("Expiry Notification", text="Expiry Notification", anchor=CENTER)
        self.table.heading("Quantity Notification", text="Quantity Notification", anchor=CENTER)

        self.table.bind("<Double-1>", self.selectProduct)

        self.refresh(userdetails)

        self.table.pack(side=TOP, anchor=W)

        self.root.mainloop()

    def selectProduct(self, event):
        item = self.table.selection()
        values = self.table.item(item, 'values')
        selected_product_id = values[0]
        self.select_product_callback(selected_product_id)
        self.root.destroy()

    def refresh(self, userdetails):
        self.table.delete(*self.table.get_children())
        products = self.load_products(userdetails)
        categories = self.load_categories(userdetails)
        for p in products:
            pcateg = next((c[1] for c in categories if c[0] == p['category']), 'No Category Set')
            self.table.insert(parent='', index='end', iid=p['id'], text='',
                              values=(p['id'],
                                      p['barcode'],
                                      p['name'],
                                      p['quantity'],
                                      pcateg,
                                      p['expiration'] if p['expiration'] != "-1" else 'No Expiration Set',
                                      p['notifexp'] if p['notifexp'] != -1 else 'No Notification Set',
                                      p['notifquan'] if p['notifquan'] != -1 else 'No Notification Set'
                                      ))

    def load_products(self, userdetails):
        url = "http://127.0.0.1:7890/products"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        productsjson = json.loads(r.text)
        products = []
        for product in productsjson['products']:
            products.append(product)
        return products

    def load_categories(self, userdetails):
        URL = "http://127.0.0.1:7890/product/categories"
        params = {'auth_user': userdetails.get('username'), 'auth_password': userdetails.get('password')}
        r = requests.get(url=URL, params=params)
        categories = []
        for category in json.loads(r.text)['categories']:
            categories.append((category['id'], category['name']))
        return categories


def on_double_click(selected_product_id):
    print("Selected Product ID:", selected_product_id)
