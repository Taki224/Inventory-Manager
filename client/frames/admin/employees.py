from tkinter import *
from tkinter import ttk

import requests
import json


def open(mainframe, userdetails):
    root = Toplevel(mainframe)
    root.title("Employees")

    margin = Frame(root)
    margin.pack(padx=30, pady=30)

    table = ttk.Treeview(margin)

    table['columns'] = ("ID", "Username", "Email", "Permission")

    table.column("#0", width=0, stretch=NO)
    table.column("ID", anchor=CENTER, width=120)
    table.column("Username", anchor=CENTER, width=120)
    table.column("Email", anchor=CENTER, width=120)
    table.column("Permission", anchor=CENTER, width=120)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("ID", text="ID", anchor=CENTER)
    table.heading("Username", text="Userame", anchor=CENTER)
    table.heading("Email", text="Email", anchor=CENTER)
    table.heading("Permission", text="Permission", anchor=CENTER)

    url = "http://127.0.0.1:7890/employees"
    params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
    r = requests.get(url=url, params=params)
    employeesjson = json.loads(r.text)

    for i, e in enumerate(employeesjson):
        table.insert(parent='', index='end', iid=i, text='',
                     values=(e['id'], e['username'], e['email'], (
                         "Admin" if e['permission'] == 1 else ("Employee" if e['permission'] == 0 else "Customer"))))

    table.pack()
    mainloop()
