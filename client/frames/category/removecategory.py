from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import requests
import json


def open(mainframe, userdetails):
    def delete_category():
        selected_category = category_combobox.get()
        category_id = selected_category.split(" - ")[0]
        URL = "http://127.0.0.1:7890/category/delete"
        params = {'auth_user': userdetails.get('username'), 'auth_password': userdetails.get('password'),
                  'id': category_id}
        r = requests.delete(url=URL, params=params)
        if r.status_code == 200:
            print(r.text)
            if json.loads(r.text)['success'] == False:
                messagebox.showwarning("Warning", "There are product(s) that has this category!")
                return
            messagebox.showinfo("Success", "Category deleted successfully!")
            root.destroy()

    def load_categories():
        URL = "http://127.0.0.1:7890/product/categories"
        params = {'auth_user': userdetails.get('username'), 'auth_password': userdetails.get('password')}
        r = requests.get(url=URL, params=params)
        categories = []
        for category in json.loads(r.text)['categories']:
            categories.append(f"{category['id']} - {category['name']}")
        category_combobox['values'] = categories

    root = Toplevel(mainframe)
    root.title("Delete Category")

    # Create the label and combobox for category selection
    category_label = Label(root, text="Select Category:")
    category_label.pack()
    category_combobox = ttk.Combobox(root)
    category_combobox.pack()
    load_categories()

    # Create the button to delete the category
    delete_button = Button(root, text="Delete Category", command=delete_category)
    delete_button.pack()

    root.mainloop()
