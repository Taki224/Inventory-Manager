from tkinter import *
from tkinter import ttk

import requests
import json


class EmployeeSelector:
    def __init__(self, mainframe, userdetails, load_employee_callback):
        self.root = Toplevel(mainframe)
        self.root.title("Employee selector")
        self.userdetails = userdetails
        self.load_employee_callback = load_employee_callback

        margin = Frame(self.root)
        margin.pack(padx=30, pady=30)

        self.table = ttk.Treeview(margin)

        self.table['columns'] = ("ID", "Username", "Email", "Permission")

        self.table.column("#0", width=0, stretch=NO)
        self.table.column("ID", anchor=CENTER, width=120)
        self.table.column("Username", anchor=CENTER, width=120)
        self.table.column("Email", anchor=CENTER, width=120)
        self.table.column("Permission", anchor=CENTER, width=120)

        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("ID", text="ID", anchor=CENTER)
        self.table.heading("Username", text="Userame", anchor=CENTER)
        self.table.heading("Email", text="Email", anchor=CENTER)
        self.table.heading("Permission", text="Permission", anchor=CENTER)

        self.table.bind("<Double-1>", self.selectEmployee)

        self.load_employees(userdetails)

    def selectEmployee(self, event):
        item = self.table.selection()
        values = self.table.item(item, 'values')
        selected_employee_id = values[0]
        self.load_employee_callback(selected_employee_id)
        self.root.destroy()

    def load_employees(self, userdetails):
        url = "http://127.0.0.1:7890/employees"
        params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
        r = requests.get(url=url, params=params)
        employeesjson = json.loads(r.text)
        employees = []

        for i, e in enumerate(employeesjson):
            self.table.insert(parent='', index='end', iid=i, text='',
                              values=(e['id'], e['username'], e['email'],
                                      "Admin" if e['permission'] == 1 else (
                                          "Employee" if e['permission'] == 0 else "Customer")))

        self.table.pack()
        self.root.mainloop()
