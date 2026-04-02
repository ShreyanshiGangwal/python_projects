import tkinter as tk

root = tk.Tk()
root.title("Calculator")
root.geometry("320x550+500+100")

# ---------------- THEME ----------------
is_dark = False
all_buttons = []

# ------- SET THEME FUNCTION -------
def set_theme():
    global bg, fg, btn_bg, op_bg

    if is_dark:
        bg = "#1E1E1E"
        fg = "white"
        btn_bg = "#2E2E2E"
        op_bg = "#F4A261"
    else:
        bg = "#F5E6CC"
        fg = "black"
        btn_bg = "#EFD9A7"
        op_bg = "#F4A261"

    root.configure(bg=bg)
    display.configure(bg=bg, fg=fg)
    history_label.configure(bg=bg, fg=fg)

    for btn in all_buttons:
        text = btn['text']
        if text in ['/', '*', '-', '+', '=']:
            btn.configure(bg=op_bg, fg="black")
        else:
            btn.configure(bg=btn_bg, fg="black")

    toggle_btn.configure(bg=btn_bg, fg=fg)

# ---------------- DISPLAY ----------------
history_label = tk.Label(root, text="", anchor="e", font=("Arial", 12))
history_label.pack(fill="both", padx=10)

display = tk.Entry(root, font=("Arial", 24), bd=1, relief='ridge', justify="right")
display.pack(fill="both", ipadx=8, ipady=20, padx=10, pady=10)

# ---------------- CLICK FUNCTION ----------------
def click(value):
    if value == "=":
        try:
            result = eval(display.get())

            history_label.config(text=display.get())
            display.delete(0, tk.END)
            display.insert(tk.END, result)
        except:
            display.delete(0, tk.END)
            display.insert(tk.END, "Error")

    elif value == "C":
        display.delete(0, tk.END)
        history_label.config(text="")

    elif value == "+/-":
        try:
            value = float(display.get())
            display.delete(0, tk.END)
            display.insert(0, str(-value))
        except:
            pass

    else:
        display.insert(tk.END, value)

# ---------------- HOVER EFFECT ----------------
def on_enter(e):
    e.widget['bg'] = "#FFD580"
    e.widget['cursor'] = "hand2"

def on_leave(e):
    text = e.widget['text']
    if text in ['/', '*', '-', '+', '=']:
        e.widget['bg'] = op_bg
    else:
        e.widget['bg'] = btn_bg


# -------- BUTTONS & FUNCTION ---------
frame = tk.Frame(root)
frame.pack()

buttons = [
    ['C', '(', ')', '/'],
    ['1', '2', '3', '*'],
    ['4', '5', '6', '-'],
    ['7', '8', '9', '+'],
    ['+/-', '0', '.', '=']
]

def create_buttons():
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            val = buttons[i][j]

            color = op_bg if val in ['/', '*', '-', '+', '=']else btn_bg

            btn = tk.Button(
                frame,
                text=val,
                font=("Arial", 14),
                width=5,
                height=2,
                bg=color,
                fg="black",
                command=lambda v=val: click(v)
            )

            btn.grid(row=i, column=j, padx=5, pady=5)

            # Hover effect
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            # Store buttons
            all_buttons.append(btn)

# ---------------- THEME TOGGLE ----------------
def toggle_theme():
    global is_dark
    is_dark = not is_dark
    set_theme()

toggle_btn = tk.Button(root, text="🌙 ",bg='gray', command=toggle_theme)
toggle_btn.place(x=280, y=490)

# ---------------- INIT ----------------
set_theme()
create_buttons()

root.mainloop()