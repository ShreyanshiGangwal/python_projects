import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import json
import os

root = ctk.CTk()
root.title('💰 Expense Tracker')
root.geometry('650x680')

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

# -------- TITLE ---------
title = ctk.CTkLabel(root, text='Expense Tracker', font=('Segoe UI', 34, 'bold'))
title.pack(pady=10)

# -------- FRAMES ---------
first_frame = ctk.CTkFrame(root, corner_radius=15, width=630,height=230)
first_frame.pack(pady=10)
first_frame.pack_propagate(False)

second_frame = ctk.CTkFrame(root, corner_radius=15, width=630, height=190)
second_frame.pack(anchor='center', pady=10)

third_frame = ctk.CTkFrame(root, corner_radius=15, width=580, height=70)
third_frame.pack(side='bottom', pady=10)
third_frame.pack_propagate(False)

# -------- NUMBER FRAME --------
three_frame = ctk.CTkFrame(first_frame, fg_color='transparent')
three_frame.pack(fill='x', side='bottom', pady=10)

one_frame = ctk.CTkFrame(first_frame, fg_color='transparent', width=295)
one_frame.pack(side='right',anchor='n', padx=10)

two_frame = ctk.CTkFrame(first_frame, fg_color='transparent', width=295)
two_frame.pack(side='left',anchor='n', padx=10)

# -------- EXPENSE NAME & AMOUNT FIELD ---------
exp_name = ctk.CTkLabel(two_frame, text='Expense Name', font=('Segoe UI', 15, 'bold'))
exp_name.pack(padx=10,pady=10,anchor='w')

exp_name_entry = ctk.CTkEntry(two_frame, font=("Verdana", 13), placeholder_text='Enter Expenses...', corner_radius=10, width=250, height=34)
exp_name_entry.pack(padx=10,anchor='w')

amount = ctk.CTkLabel(two_frame, text='Amount', font=('Segoe UI', 15, 'bold'))
amount.pack(padx=10,pady=10,anchor='w')

amount_entry = ctk.CTkEntry(two_frame, font=("Verdana", 13), placeholder_text='Enter amount...', corner_radius=10, width=250, height=34)
amount_entry.pack(padx=10,anchor='w')

# -------- CATEGORY & DATE FIELD ---------
category = ctk.CTkLabel(one_frame, text='Category', font=('Segoe UI', 15, 'bold'))
category.pack(padx=10,pady=10,anchor='w')

category_entry = ctk.CTkEntry(one_frame, font=("Verdana", 13), placeholder_text='Enter category...', corner_radius=10, width=250, height=34)
category_entry.pack(padx=10,anchor='w')

date = ctk.CTkLabel(one_frame, text='Date', font=('Segoe UI', 15, 'bold'))
date.pack(padx=10,pady=10,anchor='w')

date_entry = ctk.CTkEntry(one_frame, font=("Verdana", 13), placeholder_text='dd-mm-yyyy', corner_radius=10, width=250, height=34)
date_entry.pack(padx=10,anchor='w')

# -------- ADD BUTTON ---------
add_btn = ctk.CTkButton(
    three_frame,
    text='Add Expense',
    height=35,
    corner_radius=12,
    width=250,
    font=("Segoe UI", 14, "bold"),
    text_color='black',
    fg_color="#00D150",
    hover_color="#0C5725"
)
add_btn.pack(pady=5)

# -------- TOTAL BALANCE --------
balance_frame = ctk.CTkFrame(third_frame, fg_color='transparent')
balance_frame.pack(fill='x', padx=20,pady=10)

balance = ctk.CTkLabel(balance_frame, text='💵 Total Balance: ₹0',text_color='#00D150', font=('Segoe UI', 24))
balance.pack(side='left', padx=10, pady=5)

# ------- SHOW GRAPH BUTTON --------
graph_btn = ctk.CTkButton(
    balance_frame,
    text="Show Graph",
    height=35,
    width=150,
    corner_radius=10,
    text_color='black',
    font=("Segoe UI", 12, "bold"),
    fg_color="#00DD6F",
    hover_color="#146935"
)
graph_btn.pack(side="right", padx=10, pady=10)

# -------- SCROLL EXPENSE ---------
scroll_bar = ctk.CTkScrollableFrame(second_frame, width=580, height=220)
scroll_bar.pack(fill='both', expand=True, padx=10, pady=10)

# ------- EMPTY FIELD -------
empty_label = ctk.CTkLabel(
            scroll_bar,
            text="No expenses yet",
            font=("Segoe UI", 15)
)
empty_label.pack(pady=50)

# -------- ADD EXPENSE FUNCTION ---------
expenses = []

def add_expense():
    names = exp_name_entry.get()
    amnt = amount_entry.get()
    catg = category_entry.get()
    dte = date_entry.get() 

    # ---- messagebox show if error ----
    if names == '' or amnt == '' or catg == '' or dte == '':
        messagebox.showwarning('Warning', 'Please fill all the entries!')
        return
    
    if len(dte) != 10 or dte[2] != '-' or dte[5] != '-':
        messagebox.showerror("Error", "Date must be in format dd-mm-yyyy")
        return

    expense = {'expense name': names, 'category': catg,'amount': int(amnt),'date':dte}
    expenses.append(expense)

    exp_name_entry.delete(0, 'end')
    amount_entry.delete(0, 'end')
    category_entry.delete(0, 'end')
    date_entry.delete(0, 'end')

    show_expenses()
    save_cards()

# -------- SHOW EXPENSE FUNCTION ---------
def show_expenses():
    for cards in scroll_bar.winfo_children():
        cards.destroy()

    # ---- After deleting process ----
    if len(expenses) == 0:
        balance.configure(text="💵 Total Balance: ₹0")

        empty_label = ctk.CTkLabel(
            scroll_bar,
            text="No expenses yet",
            font=("Segoe UI", 15)
        )
        empty_label.pack(pady=50)

        return

    # ---- Making cards and buttons ----
    total = 0

    for i, exp in enumerate(expenses):
        total += exp['amount']

        card = ctk.CTkFrame(scroll_bar, corner_radius=10)
        card.pack(fill='x', pady=6, padx=8)

        label = ctk.CTkLabel(
            card,
            text=f'{exp["expense name"]} | ₹{exp["amount"]} | {exp["category"]} | {exp["date"]}',
            font=("Segoe UI", 15)
        )
        label.pack(side="left", padx=10, pady=5)

        delete_btn = ctk.CTkButton(
            card,
            text='❌',
            width=40,
            command=lambda i=i: delete_expense(i)
        )
        delete_btn.pack(side="right", padx=5)

    balance.configure(text=f"💵 Total Balance: ₹{total}")
    save_cards()

add_btn.configure(command=add_expense)

# -------- DELETE FUNCTION ----------
def delete_expense(index):
    expenses.pop(index)
    show_expenses()
    save_cards()

# ------- SAVE CARDS IN JSON --------
def save_cards():
    with open('Cards.json', 'w')as file:
        json.dump(expenses, file)

def load_cards():
    if os.path.exists('Cards.json'):
        with open('Cards.json', 'r') as file:
            global expenses
            expenses = json.load(file)

load_cards()
show_expenses()

# ------ GRAPH FUNCTION ------
# def show_graph():
#     if len(expenses) == 0:
#         messagebox.showinfo('Info', 'No data to show!')
#         return
    
#     data = {}

#     # ---- Category-wise total ----
#     for exp in expenses:
#         catg = exp['category']
#         amt = exp['amount']

#         if catg in data:
#             data[catg] += amt
#         else:
#             data[catg] = amt

#     categories = list(data.keys())
#     amounts = list(data.values())

#     # ---- Plot use here ----
#     plt.figure()
#     plt.bar(categories, amounts)
#     plt.title('Expense by Category')
#     plt.xlabel("Category")
#     plt.ylabel("Amount")
#     plt.show()

# graph_btn.configure(command=show_graph)

def show_pie_chart():
    if len(expenses) == 0:
        messagebox.showinfo("Info", "No data to show!")
        return

    data = {}

    # ---- Category-wise total ----
    for exp in expenses:
        cat = exp["category"]
        amt = exp["amount"]

        if cat in data:
            data[cat] += amt
        else:
            data[cat] = amt

    categories = list(data.keys())
    amounts = list(data.values())

    # ---- Pie Chart ----
    plt.figure()
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expense Distribution")
    plt.show()

graph_btn.configure(command=show_pie_chart)

root.mainloop()