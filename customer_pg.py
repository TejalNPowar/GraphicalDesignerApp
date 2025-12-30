from tkinter import ttk
import sqlite3
from db import DB_NAME

def customer_page(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    form = ttk.LabelFrame(frame, text="Customer Bill", padding=10)
    form.pack(fill="x")

    fields = ["Name", "Date", "Work", "Material", "Quantity", "Price", "Paid"]
    entries = {}

    for i, field in enumerate(fields):
        ttk.Label(form, text=field).grid(row=i, column=0, sticky="w")
        e = ttk.Entry(form)
        e.grid(row=i, column=1, pady=2)
        entries[field] = e

    columns = ("Name", "Work", "Total", "Paid", "Remaining")
    table = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=180)

    table.pack(fill="both", expand=True, pady=10)

    def load_bills():
        table.delete(*table.get_children())
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        for row in cur.execute("SELECT name, work, total, paid, remaining FROM customers"):
            table.insert("", "end", values=row)
        conn.close()

    def add_bill():
        qty = float(entries["Quantity"].get())
        price = float(entries["Price"].get())
        paid = float(entries["Paid"].get())
        total = qty * price
        remaining = total - paid

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO customers VALUES (NULL,?,?,?,?,?,?,?,?,?)
        """, (
            entries["Name"].get(),
            entries["Date"].get(),
            entries["Work"].get(),
            entries["Material"].get(),
            qty, price, total, paid, remaining
        ))
        conn.commit()
        conn.close()
        load_bills()

    ttk.Button(left, text="Add Bill", command=add_bill)\
   .pack(fill="x", pady=(10, 5))

    ttk.Button(left, text="Delete Bill", command=delete_bill)\
   .pack(fill="x", pady=5)


    load_bills()
