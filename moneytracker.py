import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import csv

# File to save financial data
FILE_NAME = 'financial_data.csv'

# Create the CSV file with headers if it does not exist
def create_file_if_not_exists():
    try:
        with open(FILE_NAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Description', 'Category', 'Amount'])
    except FileExistsError:
        pass

# Save a transaction into the CSV file
def add_transaction(date, description, category, amount):
    try:
        with open(FILE_NAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, description, category, amount])
        messagebox.showinfo("Success", "Transaction added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add transaction: {e}")

# Display the transactions from the CSV file in a new window
def view_transactions():
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            messagebox.showinfo("No Data", "No transactions found. Please add a transaction first.")
            return

        view_window = tk.Toplevel(root)
        view_window.title("View Transactions")
        view_window.geometry("600x400")

        tree = ttk.Treeview(view_window, columns=('Date', 'Description', 'Category', 'Amount'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Description', text='Description')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=(row['Date'], row['Description'], row['Category'], row['Amount']))

        tree.pack(fill=tk.BOTH, expand=True)
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No transactions found. Please add a transaction first.")

# Plot the transactions based on the categories
def plot_transactions():
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            messagebox.showinfo("No Data", "No transactions found. Please add a transaction first.")
            return

        df['Date'] = pd.to_datetime(df['Date'])
        grouped = df.groupby(['Category'])['Amount'].sum()

        plt.figure(figsize=(10, 6))
        plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', colors=plt.get_cmap('tab20').colors)
        plt.title('Total Expenditure by Category')
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No transactions found. Please add a transaction first.")

# Main application window
root = tk.Tk()
root.title("Financial Tracker")
root.geometry("400x350")

# Creating the file if not exists
create_file_if_not_exists()

# Input fields and labels
date_label = tk.Label(root, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
date_entry = DateEntry(root, format='yyyy-mm-dd')
date_entry.grid(row=0, column=1, padx=10, pady=5)

description_label = tk.Label(root, text="Description:")
description_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
category_options = ['Food', 'Housing', 'Bills', 'Fitness', 'Electronics', 'Education', 'Transport', 'Entertainment', 'Health', 'Animals', 'Charity']
category_var = tk.StringVar(value=category_options[0])
category_menu = ttk.Combobox(root, textvariable=category_var, values=category_options)
category_menu.grid(row=2, column=1, padx=10, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1, padx=10, pady=5)

# Button to add transaction
add_button = tk.Button(root, text="Add Transaction", command=lambda: add_transaction(
    date_entry.get(), description_entry.get(), category_var.get(), amount_entry.get()))
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Button to view transactions
view_button = tk.Button(root, text="View Transactions", command=view_transactions)
view_button.grid(row=5, column=0, columnspan=2, pady=5)

# Button to plot transactions
plot_button = tk.Button(root, text="Plot Transactions", command=plot_transactions)
plot_button.grid(row=6, column=0, columnspan=2, pady=5)

# Run the application
root.mainloop()
