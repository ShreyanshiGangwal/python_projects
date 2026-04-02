import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

# ---------- MAIN WINDOW ----------
root = ctk.CTk()
root.title('Smart To-Do App')
root.geometry('1000x600')

#---------- THEME ----------
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# Create empty task list..
tasks = []

# ---------- FUNCTIONS ----------
def save_task():
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

def load_task():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            global tasks
            tasks = json.load(file)

load_task()

# ------ CHECK DATES FUNCTION -------
def check_dates():
    today = datetime.now().strftime("%d-%m-%Y")

    for task in tasks:
        if task['date'] == today and not task['done']:
            messagebox.showinfo('Reminder 🔔', f"Task Due Today:\n{task['title']}")
            task["notified"] = True
            save_task()

# ------- ADD TASK FUNCTION --------
def add_task():
    title = title_bar.get()
    desc = desc_bar.get('1.0', 'end').strip()
    date = date_bar.get()
    priority = priority_bar.get()

    if title == '':
        messagebox.showwarning('Warning', 'Task title required!')
        return
    
    task ={
        'title': title,
        'desc': desc,
        'date': date,
        'priority': priority,
        'done': False
    }

    tasks.append(task)
    show_task()
    save_task()

    title_bar.delete(0, 'end')
    desc_bar.delete('1.0', 'end')
    date_bar.delete(0, 'end')

# -------- DELETE TASK FUNCTION ---------
def delete_task(index):
    tasks.pop(index)
    show_task()
    save_task()

# -------- MARK DONE FUNCTION ---------
def mark_done(index):
    if not tasks[index]['done']:
        tasks[index]['done'] = True
        show_task()
        save_task()

# -------- EDIT TASK FUNCTION --------
def edit_task(index):
    edit_win = ctk.CTkToplevel(root)     # Create Edit Window
    edit_win.title('Edit Task')
    edit_win.geometry('300x350')
    edit_win.transient(root)             # Edit Window will remain above the root window.
    edit_win.grab_set()                  # Focus locked on this window
    edit_win.focus()                     # This provides a direct focus

    task = tasks[index]

    title = ctk.CTkEntry(edit_win)
    title.insert(0, task['title'])
    title.pack(pady=5)

    desc = ctk.CTkTextbox(edit_win, height=80)
    desc.insert('1.0', task['desc'])
    desc.pack(pady=5)

    date = ctk.CTkEntry(edit_win)
    date.insert(0, task['date'])
    date.pack(pady=5)

    priority = ctk.StringVar(value=task['priority'])
    ctk.CTkOptionMenu(
        edit_win,
        variable=priority,
        values=['Low', 'Medium', 'High']
    ).pack(pady=5)
    
    # ---- SAVE EDIT FUNCTION ----
    def save_edit():
        task['title'] = title.get()
        task['desc'] = desc.get('1.0', 'end').strip()
        task['date'] = date.get()
        task['priority'] = priority.get()

        save_task()
        show_task()
        edit_win.destroy()

    ctk.CTkButton(edit_win, text='Save', command=save_edit).pack(pady=10)

# -------- SEARCH FUNCTION ---------
def search_task():
    keyword = search_bar.get().lower()
    show_task(new_keyword=keyword)

# -------- SHOW TASK FUNCTION --------
def show_task(new_keyword=''):
    [cards.destroy() for cards in scroll_task.winfo_children()]

    index = 0

    for task in tasks:
        if new_keyword != '':
            if new_keyword not in task['title'].lower():
                continue

        task_card(task, index)
        index += 1

    # Progress bar function
    done_tasks = 0
    for t in tasks:
        if t["done"]:
            done_tasks += 1

    total_tasks = len(tasks)

    progress_bar.configure(text=f"✅ {done_tasks}/{total_tasks}")

# -------- CREATE TASK CARDS FUNCTION -------
def task_card(task, index):
    color = '#2a2d2e' if not task['done'] else '#383B6D'

    # card frame
    card = ctk.CTkFrame(scroll_task, corner_radius=10, fg_color=color)
    card.pack(fill='x', padx=5, pady=5)

    title = f"✔ {task['title']}" if task['done'] else f"• {task['title']}"
    ctk.CTkLabel(
        card,
        text=title,
        font=("Arial", 16, "bold")
    ).pack(anchor='w', padx=10, pady=2)
    
    ctk.CTkLabel(
        card,
        text=f"📅 {task['date']}  |  {task['priority']}"
    ).pack(anchor='w', padx=10)

    ctk.CTkLabel(
        card,
        text=f'📝 {task['desc']}'
    ).pack(anchor='w',padx=10, pady=5)

    btn_frame = ctk.CTkFrame(card, fg_color='transparent')
    btn_frame.pack(anchor='e', padx=10, pady=5)

    # ---- DONE, DELETE & EDIT BTNs ----
    ctk.CTkButton(btn_frame, text='Done', width=70, command=lambda: mark_done(index)).pack(side='left', padx=5)
    ctk.CTkButton(btn_frame, text='Delete', width=70, fg_color='red', command=lambda: delete_task(index)).pack(side='left', padx=5)
    ctk.CTkButton(btn_frame, text='Edit', width=70, command=lambda: edit_task(index)).pack(side='left', padx=5)

# ---------- LEFT PANEL ----------
left_frame = ctk.CTkFrame(root, width=300)
left_frame.pack(side='left', fill='y', padx=10, pady=10)

# Create headline .....
ctk.CTkLabel(
    left_frame,
    text='Create Task',
    font=('Arial', 18, 'bold')
).pack(pady=10)

# Create title....
ctk.CTkLabel(left_frame, text='Title').pack()

title_bar = ctk.CTkEntry(left_frame)
title_bar.pack(pady=5)

# Create description....
ctk.CTkLabel(left_frame, text='Description').pack()

desc_bar = ctk.CTkTextbox(left_frame, height=80)
desc_bar.pack(pady=5)

# Create priority field.....
ctk.CTkLabel(left_frame, text='Priority').pack()

priority_bar = ctk.StringVar(value='Medium')
ctk.CTkOptionMenu(
    left_frame,
    variable=priority_bar,
    values=['Low', 'Medium', 'High']
).pack(pady=5)

# Create date.....
ctk.CTkLabel(left_frame, text='Date').pack()

date_bar = ctk.CTkEntry(left_frame, placeholder_text='00-00-0000')
date_bar.pack(pady=5)

# Add button create....
ctk.CTkButton(
    left_frame,
    text='Add Task',
    command=add_task
).pack(pady=20)

# ---------- RIGHT PANEL ----------
right_frame = ctk.CTkFrame(root)
right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

# -------- SEARCH AREA -----------
top_frame = ctk.CTkFrame(right_frame)
top_frame.pack(fill='x', pady=10)

# Create search entrybox + buttons...
search_bar = ctk.CTkEntry(top_frame, placeholder_text='Search...')
search_bar.pack(side='left', padx=10)

ctk.CTkButton(top_frame, text='Search', command=search_task).pack(side='left')
ctk.CTkButton(top_frame, text='Show All', command=show_task).pack(side='left', padx=5)

# Create progress area...
progress_bar = ctk.CTkLabel(top_frame, text='')
progress_bar.pack(side="right", padx=10)

# ------- Scrollable Task Area -------
scroll_task = ctk.CTkScrollableFrame(right_frame)
scroll_task.pack(fill='both', expand=True, padx=10, pady=10)

show_task()
check_dates()

root.mainloop()