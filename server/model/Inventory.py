from datetime import datetime

from model.Category import Category
import sqlite3
from model.Product import Product

class Inventory:
    def __init__(self):
        self.products = []
        self.categories = []
        self.shop = None
        self.loadCategories()
        self.loadProducts()

    def setShop(self, shop):
        self.shop = shop

    def loadCategories(self):
        self.categories = []
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Categories")
        rows = c.fetchall()
        for row in rows:
            c = Category(row[0], row[1])
            self.categories.append(c)

    def getCategories(self):
        categorylist = []
        for c in self.categories:
            categorylist.append(c.to_json())
        return categorylist

    def newProduct(self, barcode, name, quantity, category, expiration, notifexp, notifquan, creator):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        category = c.execute("SELECT id FROM Categories WHERE name = ?", (category,)).fetchone()[0]
        c.execute("INSERT INTO Products (barcode, name, quantity, category, expiration, notifexp, notifquan) VALUES (?, ?, ?, ?, ?, ?, ?)", (barcode, name, quantity, category, expiration, notifexp, notifquan))
        conn.commit()
        conn.close()
        self.loadProducts()
        self.logChange(creator, "Created product with barcode: " + barcode)
        return True

    def loadProducts(self):
        self.products = []
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Products")
        rows = c.fetchall()
        for row in rows:
            p = Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            self.products.append(p)

    def checkProduct(self, barcode, expiration):
        for p in self.products:
            if p.barcode == barcode and p.expiration == expiration:
                return p
        return None

    def getProduct(self, id):
        for p in self.products:
            if p.id == int(id):
                return p
        return None

    def updateProduct(self, id, product, creator):
        name = product['name']
        quantity = product['quantity']
        category = product['category']
        expiration = product['expiration']
        notifexp = product['notifexp']
        notifquan = product['notifquan']
        conn = sqlite3.connect('inventory.db')
        category = conn.execute("SELECT id FROM Categories WHERE name = ?", (category,)).fetchone()[0]
        c = conn.cursor()
        c.execute("UPDATE Products SET name = ?, quantity = ?, category = ?, expiration = ?, notifexp = ?, notifquan = ? WHERE id = ?", (name, quantity, category, expiration, notifexp, notifquan, id))
        barcode = c.execute("SELECT barcode FROM Products WHERE id = ?", (id,)).fetchone()[0]
        conn.commit()
        conn.close()
        self.loadProducts()
        self.logChange(creator, "Updated product with barcode: " + barcode)

        return True

    def deleteProduct(self, id):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("DELETE FROM Products WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        self.loadProducts()
        return True

    def updateStock(self, id, change, creator):
        change = int(change)
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        current = c.execute("SELECT quantity FROM Products WHERE id = ?", (id,)).fetchone()[0]
        if current + change < 0:
            return False
        new = current + change
        c.execute("UPDATE Products SET quantity = ? WHERE id = ?", (new, id))
        barcode = c.execute("SELECT barcode FROM Products WHERE id = ?", (id,)).fetchone()[0]
        conn.commit()
        conn.close()
        self.loadProducts()
        self.logChange(creator, "Updated stock of product with barcode: " + barcode + " by " + str(change))
        return True

    def addCategory(self, name):
        #check if category exists
        for c in self.categories:
            if c.name == name:
                return False
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO Categories (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        self.loadCategories()
        return True

    def removeCategory(self, id):
        #check if any product is in the category
        for p in self.products:
            if p.category == int(id):
                return False
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("DELETE FROM Categories WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        self.loadCategories()
        return True

    def logChange(self, employee, action):
        #employee id by name
        eid = None
        for e in self.shop.employees:
            if e.username == employee:
                eid = e.id
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO Changes (employee, datetime, action) VALUES (?, ?, ?)", (eid,datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action))
        conn.commit()
        conn.close()
        return True

    def getNotifications(self):
        notifications = []
        for p in self.products:
            if p.notifexp != -1:
                if p.expiration != "-1":
                    current_date = datetime.now()
                    expiration_date = datetime.strptime(p.expiration, "%Y.%m.%d")
                    if int((expiration_date - current_date).days) < int(p.notifexp):
                        notifications.append(p.to_json())
            if p.notifquan != -1:
                if p.quantity < p.notifquan:
                    notifications.append(p.to_json())
        return notifications