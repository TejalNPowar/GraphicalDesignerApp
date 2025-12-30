import tkinter as tk
from tkinter import ttk
from db import create_tables
from stock_pg import stock_page
from customer_pg import customer_page
from report_pg import report_page

create_tables()

root = tk.Tk()
root.title("Graphic Designer Management System")
root.geometry("1200x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

stock_tab = ttk.Frame(notebook)
customer_tab = ttk.Frame(notebook)
report_tab = ttk.Frame(notebook)

notebook.add(stock_tab, text="Stock Management")
notebook.add(customer_tab, text="Customer Billing")
notebook.add(report_tab, text="Reports")

stock_page(stock_tab)
customer_page(customer_tab)
report_page(report_tab)

root.mainloop()
