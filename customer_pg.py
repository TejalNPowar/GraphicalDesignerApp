from tkinter import ttk
import sqlite3
from db import DB_NAME

def customer_page(parent):
    # Main frame
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Form frame
    form = ttk.LabelFrame(frame, text="Customer Bill", padding=10)
    form.pack(fill="x", pady=(0, 10))

    fields = ["Name", "Date", "Work", "Material", "Quantity", "Price", "Paid"]
    entries = {}

    # Create labels and entries
    for i, field in enumerate(fields):
        ttk.Label(form, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        e = ttk.Entry(form)
        e.grid(row=i, column=1, pady=2, padx=5)
        entries[field] = e

    # Buttons frame
    btn_frame = ttk.Frame(form)
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

    # Table
    columns = ("Name", "Work", "Total", "Paid", "Remaining")
    table = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=180)

    table.pack(fill="both", expand=True)

    # Function to load bills from DB
    def load_bills():
        table.delete(*table.get_children())
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT name, work, total, paid, remaining FROM customers")
        for row in cur.fetchall():
            table.insert("", "end", values=row)
        conn.close()

    # Function to add a bill
    def add_bill():
        try:
            qty = float(entries["Quantity"].get())
            price = float(entries["Price"].get())
            paid = float(entries["Paid"].get())
        except ValueError:
            print("Please enter valid numbers for Quantity, Price, and Paid")
            return

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

    # Function to delete selected bill
    def delete_bill():
        selected_item = table.selection()
        if not selected_item:
            return
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        for item in selected_item:
            values = table.item(item, "values")
            # Assuming 'name' and 'work' uniquely identify the row
            cur.execute("DELETE FROM customers WHERE name=? AND work=?", (values[0], values[1]))
        conn.commit()
        conn.close()
        load_bills()

    # Buttons
    ttk.Button(btn_frame, text="Add Bill", command=add_bill).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Delete Bill", command=delete_bill).pack(side="left", padx=5)

    # Initial load
    load_bills()
