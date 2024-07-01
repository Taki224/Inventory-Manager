from tkinter import *
from tkinter import ttk
import requests
import json


def open(mainframe, userdetails):
    def getChanges():
        url = "http://127.0.0.1:7890/employees/getchanges"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        print(r.text)
        changes = json.loads(r.text)['changes']
        for i, change in enumerate(changes):
            table.insert(parent='', index='end', iid=i, text="",
                         values=(change['id'], change['employee'], change['datetime'], change['action']))

    root = Toplevel(mainframe)
    root.title("Changes")
    root.geometry("900x400")

    margin = Frame(root)
    margin.pack(padx=30, pady=30)

    table = ttk.Treeview(margin)

    table['columns'] = ('ID', 'Employee', 'Date, Time', 'Action')

    table.column("#0", width=0, stretch=NO)
    table.column("ID", anchor=CENTER, width=40)
    table.column("Employee", anchor=CENTER, width=80)
    table.column("Date, Time", anchor=CENTER, width=160)
    table.column("Action", anchor=CENTER, width=500)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("ID", text="ID", anchor=CENTER)
    table.heading("Employee", text="Employee", anchor=CENTER)
    table.heading("Date, Time", text="Date, Time", anchor=CENTER)
    table.heading("Action", text="Action", anchor=CENTER)

    getChanges()

    table.pack()

    root.mainloop()
