from tkinter import ttk
import sqlite3
from db import DB_NAME

def stock_page(parent):
    main = ttk.Frame(parent)
    main.pack(fill="both", expand=True)

    # ---------------- LEFT PANEL ----------------
    left = ttk.Frame(main, width=320, padding=10)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    ttk.Label(left, text="Add Stock", font=("Segoe UI", 11, "bold")).pack(anchor="w")

    ttk.Label(left, text="Date (YYYY-MM-DD)").pack(anchor="w")
    date_entry = ttk.Entry(left)
    date_entry.pack(fill="x", pady=3)

    materials = [
        "Flex Banner (sq.ft)", "Vinyl Sheet (sq.ft)",
        "Photo Paper (A4)", "Photo Paper (A3)",
        "Sunboard Sheet", "Foam Board",
        "Sticker Sheet", "Lamination Roll (m)",
        "Ink Black (ml)", "Ink Cyan (ml)",
        "Ink Magenta (ml)", "Ink Yellow (ml)"
    ]

    ttk.Label(left, text="Material").pack(anchor="w")
    material_cb = ttk.Combobox(left, values=materials)
    material_cb.pack(fill="x", pady=3)

    ttk.Label(left, text="Quantity").pack(anchor="w")
    qty_entry = ttk.Entry(left)
    qty_entry.pack(fill="x", pady=3)

    ttk.Label(left, text="Cost (₹)").pack(anchor="w")
    cost_entry = ttk.Entry(left)
    cost_entry.pack(fill="x", pady=3)

    # ---------------- RIGHT PANEL ----------------
    right = ttk.Frame(main, padding=10)
    right.pack(side="right", fill="both", expand=True)

    columns = ("ID","Date", "Material", "Quantity", "Cost")
    table = ttk.Treeview(right, columns=columns, show="headings")

    table.heading("ID", text="ID")
    table.heading("Date", text="Date")
    table.heading("Material", text="Material")
    table.heading("Quantity", text="Quantity")
    table.heading("Cost", text="Cost")

    table.column("ID", width=0, stretch=False)  # hide ID
    table.column("Date", width=120)
    table.column("Material", width=200)
    table.column("Quantity", width=100)
    table.column("Cost", width=100)

    table.pack(fill="both", expand=True)

    table.pack(fill="both", expand=True)

    # ---------------- FUNCTIONS ----------------
    def load_stock():
        table.delete(*table.get_children())
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        for row in cur.execute("SELECT id, date, material, quantity, cost FROM stock"):
            table.insert("", "end", values=row)
        
        conn.close()


    def add_stock():
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO stock VALUES (NULL, ?, ?, ?, ?)",
            (
                date_entry.get(),
                material_cb.get(),
                float(qty_entry.get()),
                float(cost_entry.get())
            )
        )
        conn.commit()
        conn.close()
        load_stock()
    
    def delete_stock():
        selected = table.focus()
        if not selected:
            return

        values = table.item(selected, "values")
        stock_id = values[0]  # hidden ID

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("DELETE FROM stock WHERE id = ?", (stock_id,))
        conn.commit()
        conn.close()

        load_stock()

    ttk.Button(left, text="Add Stock", command=add_stock).pack(fill="x", pady=10)
    ttk.Button(left, text="Delete Selected Stock", command=delete_stock)\
   .pack(fill="x", pady=5)

    load_stock()



# columns = ("ID", "Date", "Material", "Quantity", "Cost")
# table = ttk.Treeview(right, columns=columns, show="headings")


# table.column("ID", width=0, stretch=False)
