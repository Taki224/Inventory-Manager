from datetime import datetime

import sqlite3
from model.Employee import Employee

import datetime

class Shop():
    def __init__(self, inventory):
        self.employees = []
        self.Inventory = inventory
        self.loadEmployees()
        self.getCategories()
        inventory.setShop(self)

    def loadEmployees(self):
        self.employees = []
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        rows = c.fetchall()
        for row in rows:
            e = Employee(row[0], row[1], row[2], row[3], row[4], row[5])
            self.employees.append(e)

    def authenticate_employee(self, username, password):
        for e in self.employees:
            if e.username == username and e.password == password:
                return e
        return None

    def create_employee(self, username, email, password, genpassword, permission, creator):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO employees (username, email, password, genpassword, permission) VALUES (?, ?, ?, ?, ?)", (username, email, password, genpassword, permission))
        conn.commit()
        conn.close()
        self.loadEmployees()
        self.logChange(creator, "Created employee: " + username)
        return True

    def employee_by_username(self, username):
        for e in self.employees:
            if e.username == username:
                return e
        return None

    def employee_by_id(self, id):
        for e in self.employees:
            if e.id == id:
                return e
        return None

    def update_employee(self, id, args, creator):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        if 'email' in args:
            c.execute("UPDATE employees SET email = ? WHERE id = ?", (args['email'], id))
        if 'password' in args:
            c.execute("UPDATE employees SET password = ?, genpassword = ? WHERE id = ?", (args['password'],args['password'], id))
        if 'permission' in args:
            c.execute("UPDATE employees SET permission = ? WHERE id = ?", (args['permission'], id))
        conn.commit()
        conn.close()
        self.loadEmployees()
        self.logChange(creator, "Updated employee: " + self.employee_by_id(int(id)).username)
        return True

    def update_employee_password(self, id, password):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("UPDATE employees SET password = ? WHERE id = ?", (password, id))
        conn.commit()
        conn.close()
        self.loadEmployees()
        return True

    def update_employee_email(self, id, email):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("UPDATE employees SET email = ? WHERE id = ?", (email, id))
        conn.commit()
        conn.close()
        self.loadEmployees()
        return True

    def getCategories(self):
        return self.Inventory.getCategories()

    def getProducts(self):
        products = []
        for p in self.Inventory.products:
            products.append(p.to_json())
        return products

    def logChange(self, employee, action):
        #employee id by name
        eid = None
        for e in self.employees:
            if e.username == employee:
                eid = e.id
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO Changes (employee, datetime, action) VALUES (?, ?, ?)", (eid,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action))
        conn.commit()
        conn.close()
        return True

    def getChanges(self):
        changes = []
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Changes")
        rows = c.fetchall()
        for row in rows:
            changes.append(row)
        changes2 = []
        for c in changes:
            changes2.append({'id':c[0], 'employee': self.employee_by_id(c[1]).username, 'datetime': c[2], 'action': c[3]})
        return changes2

