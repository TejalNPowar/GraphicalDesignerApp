from tkinter import ttk
import sqlite3
from db import DB_NAME

def report_page(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    box = ttk.LabelFrame(frame, text="Business Report", padding=20)
    box.pack()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT SUM(quantity) FROM stock")
    total_stock = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(cost) FROM stock")
    invested = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(total) FROM customers")
    income = cur.fetchone()[0] or 0

    conn.close()

    ttk.Label(box, text=f"Total Stock Added: {total_stock}").pack(anchor="w")
    ttk.Label(box, text=f"Total Investment: ₹{invested}").pack(anchor="w")
    ttk.Label(box, text=f"Total Income: ₹{income}").pack(anchor="w")
