from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import frames.product.newproduct as newproduct
import frames.product.updateproduct as updateproduct
import frames.product.deleteproduct as deleteproduct
import frames.admin.newemployee as newemployee
import frames.admin.updateemployee as updateemployee
import frames.admin.employees as employees
import InventoryManagerApp as IMA
import frames.settings.changepwd as changepwd
import frames.settings.changeemail as change_email
import frames.stock.addtostock as addtostock
import frames.stock.removefromstock as removefromstock
import frames.category.addcategory as addcategory
import frames.category.removecategory as removecategory
import frames.admin.changes as changes
import requests
import json


def new_product(root, userdetails, table, margin2):
    def tablerefresh():
        refresh(userdetails, table, margin2)

    newproduct.open(root, userdetails, tablerefresh)


def update_product(userdetails, root):
    updateproduct.open(userdetails, root)


def delete_product(root, userdetails):
    deleteproduct.open(root, userdetails)


def new_employee(root, userdetails):
    newemployee.open(root, userdetails)


def update_employee(root, userdetails):
    updateemployee.open(root, userdetails)


def employeelist(root, userdetails):
    employees.open(root, userdetails)


def changepassword(root, userdetails):
    changepwd.open(root, userdetails)


def changeemail(root, userdetails):
    change_email.open(root, userdetails)


def add_to_stock(root, userdetails):
    addtostock.open(root, userdetails)


def remove_from_stock(root, userdetails):
    removefromstock.open(root, userdetails)


def load_products(userdetails):
    url = "http://127.0.0.1:7890/products"
    params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
    r = requests.get(url=url, params=params)
    productsjson = json.loads(r.text)
    products = []
    for product in productsjson['products']:
        products.append(product)
    return products


def load_categories(userdetails):
    URL = "http://127.0.0.1:7890/product/categories"
    params = {'auth_user': userdetails.get('username'), 'auth_password': userdetails.get('password')}
    r = requests.get(url=URL, params=params)
    categories = []
    for category in json.loads(r.text)['categories']:
        categories.append((category['id'], category['name']))
    return categories


def refresh(userdetails, table, margin2, entry_var=None):
    getNotifications(userdetails, margin2)
    table.delete(*table.get_children())
    products = load_products(userdetails)
    categories = load_categories(userdetails)
    for p in products:
        pcateg = next((c[1] for c in categories if c[0] == p['category']), 'No Category Set')
        if entry_var != None:
            serachtext = entry_var.get().lower()
            if serachtext in p['name'].lower() or serachtext in p['barcode'] or serachtext in pcateg.lower():
                table.insert(parent='', index='end', iid=p['id'], text='',
                             values=(p['id'],
                                     p['barcode'],
                                     p['name'],
                                     p['quantity'],
                                     pcateg,
                                     p['expiration'] if p['expiration'] != "-1" else 'No Expiration Set',
                                     p['notifexp'] if p['notifexp'] != -1 else 'No Notification Set',
                                     p['notifquan'] if p['notifquan'] != -1 else 'No Notification Set'
                                     ))
        else:
            table.insert(parent='', index='end', iid=p['id'], text='',
                         values=(p['id'],
                                 p['barcode'],
                                 p['name'],
                                 p['quantity'],
                                 next((c[1] for c in categories if c[0] == p['category']), 'No Category Set'),
                                 p['expiration'] if p['expiration'] != "-1" else 'No Expiration Set',
                                 p['notifexp'] if p['notifexp'] != -1 else 'No Notification Set',
                                 p['notifquan'] if p['notifquan'] != -1 else 'No Notification Set'
                                 ))


def new_category(root, userdetails):
    addcategory.open(root, userdetails)


def remove_category(root, userdetails):
    removecategory.open(root, userdetails)


def changelog(root, userdetails):
    changes.open(root, userdetails)


def getNotifications(userdetails, margin2):
    for widget in margin2.winfo_children():
        widget.destroy()
    notif_label = Label(margin2, text="Notifications:")
    notif_label.pack(side=TOP, anchor=W)
    url = "http://127.0.0.1:7890/products/getnotifications"
    params = {'auth_user': userdetails['username'], 'auth_password': userdetails['password']}
    r = requests.get(url=url, params=params)
    notifications = json.loads(r.text)
    notif_table = ttk.Treeview(margin2)
    notif_table['columns'] = (
        'ID', 'Barcode', 'Name', 'Qunatity', 'Category', 'Expiry Date', 'Expiry Notification', 'Quantity Notification')

    notif_table.column("#0", width=0, stretch=NO)
    notif_table.column("ID", anchor=CENTER, width=60)
    notif_table.column("Barcode", anchor=CENTER, width=120)
    notif_table.column("Name", anchor=CENTER, width=120)
    notif_table.column("Qunatity", anchor=CENTER, width=120)
    notif_table.column("Category", anchor=CENTER, width=120)
    notif_table.column("Expiry Date", anchor=CENTER, width=120)
    notif_table.column("Expiry Notification", anchor=CENTER, width=180)
    notif_table.column("Quantity Notification", anchor=CENTER, width=180)

    notif_table.heading("#0", text="", anchor=CENTER)
    notif_table.heading("ID", text="ID", anchor=CENTER)
    notif_table.heading("Barcode", text="Barcode", anchor=CENTER)
    notif_table.heading("Name", text="Name", anchor=CENTER)
    notif_table.heading("Qunatity", text="Qunatity", anchor=CENTER)
    notif_table.heading("Category", text="Category", anchor=CENTER)
    notif_table.heading("Expiry Date", text="Expiry Date", anchor=CENTER)
    notif_table.heading("Expiry Notification", text="Expiry Notification", anchor=CENTER)
    notif_table.heading("Quantity Notification", text="Quantity Notification", anchor=CENTER)
    if notifications['notifications'] != []:
        margin2.pack(padx=20, pady=30)
        categories = load_categories(userdetails)
        for notification in notifications['notifications']:
            pcateg = next((c[1] for c in categories if c[0] == notification['category']), 'No Category Set')
            notif_table.insert(parent='', index='end', iid=notification['id'], text='',
                               values=(notification['id'],
                                       notification['barcode'],
                                       notification['name'],
                                       notification['quantity'],
                                       pcateg,
                                       notification['expiration'] if notification[
                                                                         'expiration'] != "-1" else 'No Expiration Set',
                                       notification['notifexp'] if notification[
                                                                       'notifexp'] != -1 else 'No Notification Set',
                                       notification['notifquan'] if notification[
                                                                        'notifquan'] != -1 else 'No Notification Set'
                                       ))
        notif_table.pack()
    else:
        notif_table.pack_forget()
        margin2.pack_forget()


def open(userdetails):
    def logout(root):
        root.destroy()
        IMA.open()

    admin = False
    if userdetails.get('permission') == 1:
        admin = True
    root = Tk()
    root.title("Inventory Manager")
    w = 1400
    ws = root.winfo_screenwidth()
    h = 700
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))



    menubar = Menu(root)
    productmenu = Menu(menubar, tearoff=0)
    productmenu.add_command(label="Add new Product", command=lambda: new_product(root, userdetails, table, margin2))
    productmenu.add_command(label="Update Existing Product", command=lambda: update_product(userdetails, root))
    productmenu.add_command(label="Delete Product", command=lambda: delete_product(root, userdetails))
    menubar.add_cascade(label="Product", menu=productmenu)

    stockmenu = Menu(menubar, tearoff=0)
    stockmenu.add_command(label="New stock", command=lambda: add_to_stock(root, userdetails))
    stockmenu.add_command(label="Remove stock", command=lambda: remove_from_stock(root, userdetails))
    menubar.add_cascade(label="Stock", menu=stockmenu)

    settingsmenu = Menu(menubar, tearoff=0)
    settingsmenu.add_command(label="Change password", command=lambda: changepassword(root, userdetails))
    settingsmenu.add_command(label="Change email address", command=lambda: changeemail(root, userdetails))
    menubar.add_cascade(label="Settings", menu=settingsmenu)

    if admin:
        adminmenu = Menu(menubar, tearoff=0)
        adminmenu.add_command(label="Employees", command=lambda: employeelist(root, userdetails))
        adminmenu.add_separator()
        adminmenu.add_command(label="Add new employee", command=lambda: new_employee(root, userdetails))
        adminmenu.add_command(label="Update employee", command=lambda: update_employee(root, userdetails))
        adminmenu.add_separator()
        adminmenu.add_command(label="Changelog", command=lambda: changelog(root, userdetails))
        menubar.add_cascade(label="Admin", menu=adminmenu)

        categorymenu = Menu(menubar, tearoff=0)
        categorymenu.add_command(label="Add new category", command=lambda: new_category(root, userdetails))
        categorymenu.add_command(label="Remove category", command=lambda: remove_category(root, userdetails))
        menubar.add_cascade(label="Category", menu=categorymenu)

    logoutmenu = Menu(menubar, tearoff=0)
    logoutmenu.add_command(label="Logout", command=lambda: logout(root))
    menubar.add_cascade(label="Logout", menu=logoutmenu)

    root.config(menu=menubar)

    margin = Frame(root)
    margin.pack(padx=30, pady=30)
    margin2 = Frame(root)

    controls = Frame(margin)
    controls.pack(side=TOP, anchor=W)

    refreshButton = Button(controls, text="Refresh", command=lambda: refresh(userdetails, table, margin2))
    refreshButton.pack(side=LEFT, anchor=W)

    searchLabel = Label(controls, text="Search")
    searchLabel.pack(side=LEFT, anchor=W)
    entry_var = StringVar()
    entry_var.trace("w", lambda name, index, mode, entry_var=entry_var: refresh(userdetails, table, margin2, entry_var))
    searchBar = Entry(controls, textvariable=entry_var)
    searchBar.pack(side=LEFT, anchor=W)

    table = ttk.Treeview(margin)

    table['columns'] = (
        'ID', 'Barcode', 'Name', 'Qunatity', 'Category', 'Expiry Date', 'Expiry Notification', 'Quantity Notification')

    table.column("#0", width=0, stretch=NO)
    table.column("ID", anchor=CENTER, width=60)
    table.column("Barcode", anchor=CENTER, width=120)
    table.column("Name", anchor=CENTER, width=120)
    table.column("Qunatity", anchor=CENTER, width=120)
    table.column("Category", anchor=CENTER, width=120)
    table.column("Expiry Date", anchor=CENTER, width=120)
    table.column("Expiry Notification", anchor=CENTER, width=180)
    table.column("Quantity Notification", anchor=CENTER, width=180)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("ID", text="ID", anchor=CENTER)
    table.heading("Barcode", text="Barcode", anchor=CENTER)
    table.heading("Name", text="Name", anchor=CENTER)
    table.heading("Qunatity", text="Qunatity", anchor=CENTER)
    table.heading("Category", text="Category", anchor=CENTER)
    table.heading("Expiry Date", text="Expiry Date", anchor=CENTER)
    table.heading("Expiry Notification", text="Expiry Notification", anchor=CENTER)
    table.heading("Quantity Notification", text="Quantity Notification", anchor=CENTER)

    refresh(userdetails, table, margin2)

    table.pack()

    if userdetails.get('password') == userdetails.get('genpassword'):
        messagebox.showinfo("Password Change", "You are using a default password! Please change your password!")

    root.mainloop()
