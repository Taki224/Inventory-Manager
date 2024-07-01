from tkinter import *
import requests
import json
from tkinter import messagebox


def open(mainframe, userdetails):
    def add_category():
        category_name = name_entry.get()
        url = "http://127.0.0.1:7890/category/create"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password'], 'name': category_name}
        r = requests.post(url=url, params=params)
        if r.status_code == 200:
            print(r.text)
            if json.loads(r.text)['success'] == False:
                messagebox.showwarning("Warning", "Category already exists!")
                return
            messagebox.showinfo("Success", "Category added successfully!")
            root.destroy()

    root = Toplevel(mainframe)
    root.title("Create Category")

    # Create the label and entry for category name
    name_label = Label(root, text="Category Name:")
    name_label.pack()
    name_entry = Entry(root)
    name_entry.pack()

    # Create the button to add the category
    add_button = Button(root, text="Add Category", command=add_category)
    add_button.pack()

    root.mainloop()
