import customtkinter as ctk
import random
import string
import pyperclip

# -------- MAIN WINDOW ---------
root = ctk.CTk()
root.title('🔐 Password Generator')
root.geometry('800x650')
# -------- THEME ---------
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue') 

root.configure(fg_color="#0f172a")

# -------- PASSWORD FIELD ---------
frame = ctk.CTkFrame(
    root,
    width=350,
    height=500,
    corner_radius=25,
    fg_color="#1e1b4b",
    border_width=2,
    border_color="#38bdf8"
)
frame.place(relx=0.5, rely=0.5, anchor='center')

title = ctk.CTkLabel(frame, text="     PASSWORD GENERATOR     ", font=('Arial', 20, 'bold'), text_color="#38bdf8")
title.pack(pady=25)

pass_box = ctk.CTkEntry(
    frame,
    width=260,
    height=45,
    corner_radius=12,
    fg_color="#374151",
    text_color="#f7fdff",
    border_color="#38bdf8",
    border_width=1
)
pass_box.pack(pady=15)

# -------- PASSWORD LENGTH ---------
length_frame = ctk.CTkFrame(frame, fg_color='transparent')
length_frame.pack(pady=15)

length = ctk.CTkLabel(length_frame, text='Password Length:', font=('Arial',14, 'bold'))
length.pack()

# -------- FUNCTION to UPDATE LENGTH VALUE ---------
def update_length(value):
    length.configure(text = f'Password Length: {int(value)}')

## -------- CREATE SLIDER ---------
slider = ctk.CTkSlider(
    length_frame,
    from_= 4,
    to=20,
    number_of_steps=16,
    command=update_length,
    width=250,
    progress_color="#38bdf8",
    button_color="#38bdf8"
)
slider.set(11)
update_length(11)
slider.pack(pady=15)

# -------- MAKING CHECKBOXES ---------
upper = ctk.BooleanVar()
lower = ctk.BooleanVar()
digits = ctk.BooleanVar()
symbols = ctk.BooleanVar()

check_frame = ctk.CTkFrame(frame, fg_color="transparent")
check_frame.pack(pady=10)

ctk.CTkCheckBox(
    check_frame,
    text='Includes Uppercase letters',
    variable=upper,
    fg_color="#38bdf8"
).pack(anchor='w', pady=3)

ctk.CTkCheckBox(
    check_frame,
    text='Includes Lowercase letters',
    variable=lower,
    fg_color="#38bdf8"
).pack(anchor='w', pady=3)

ctk.CTkCheckBox(
    check_frame,
    text='Includes Numbers',
    variable=digits,
    fg_color="#38bdf8"
).pack(anchor='w', pady=3)

ctk.CTkCheckBox(
    check_frame,
    text='Includes Symbols',
    variable=symbols,
    fg_color="#38bdf8"
).pack(anchor='w', pady=3)

strength_lbl = ctk.CTkLabel(
    frame,
    text="Strength",
    font=("Arial", 14)
)
strength_lbl.pack(pady=(10,5))

strength_bar = ctk.CTkProgressBar(
    frame,
    width=180,
    height=6,
    corner_radius=10
)
strength_bar.pack(pady=2)

strength_bar.set(0)

# -------- GENERATE PASSWORD --------
def generate_password():
    length_val = int(slider.get())
    char = ''

    if upper.get():
        char += string.ascii_uppercase
    if lower.get():
        char += string.ascii_lowercase
    if digits.get():
        char += string.digits
    if symbols.get():
        char += string.punctuation

    if char == '':
        pass_box.delete(0, 'end')
        pass_box.insert(0, 'Select options!')
        return
    
    password = ''.join(random.choice(char) for _ in range(length_val))

    pass_box.delete(0, 'end')
    pass_box.insert(0, password)

    strength = check_strength(password)

    # Progress value (0 to 1)
    progress = strength / 5
    strength_bar.set(progress)

    # Color change
    if strength <= 2:
        strength_bar.configure(progress_color="#ef4444")  # red
    elif strength == 3:
        strength_bar.configure(progress_color="#facc15")  # yellow
    else:
        strength_bar.configure(progress_color="#22c55e")  # green
        
# ------- COPY BUTTON --------
btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
btn_frame.pack(pady=20)

def copy_password():
    pyperclip.copy(pass_box.get())
    strength_lbl.configure(text="Copied! ✅", text_color='white')
    root.after(2000, lambda: strength_lbl.configure(text="Strength"))

copy_btn = ctk.CTkButton(btn_frame, text="Copy", command=copy_password, width=140, fg_color='#1e293b', hover_color='#334155', border_color='#38bdf8', border_width=0.8)
copy_btn.pack(pady=5)

# ------- GENERATE BUTTON --------
gen_btn = ctk.CTkButton(
    btn_frame,
    text='GENERATE PASSWORD',
    command=generate_password,
    height=45,
    corner_radius=12,
    width=220,
    fg_color="#38bdf8",
    hover_color="#0ea5e9",
    text_color="black"
)
gen_btn.pack(pady=10)

# -------- CHECK FUNCTION ---------
def check_strength(password):
    strength = 0

    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1
    if len(password) >= 12:
        strength += 1

    return strength

root.mainloop()