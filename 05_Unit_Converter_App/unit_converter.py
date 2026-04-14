import customtkinter as ctk

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title('Unit Converter')
root.geometry("420x450")
root.configure(fg_color="#250235")

title = ctk.CTkLabel(root, text="🔄 Unit Converter", font=("Arial", 24, "bold"), text_color="#C5A2D4")
title.pack(pady=20)

category = ctk.CTkComboBox(
    root,
    values=["Length", "Weight", "Temperature"],
    text_color="#EACCF7",
    fg_color="#2E0D3B",
    dropdown_fg_color="#260B31",
    dropdown_hover_color="#442352",
    border_color="#3F1650",
    button_hover_color="#442352",
    button_color="#3F1650"
)
category.pack(pady=10)
category.set("Length")

entry = ctk.CTkEntry(
    root,
    placeholder_text="Enter the value...",
    height=40, 
    font=("Arial", 16),
    text_color='#EACCF7',
    fg_color="#2E0D3B",
    border_color="#3F1650"
)
entry.pack(pady=10,padx=40,fill='x')

frame = ctk.CTkFrame(root, fg_color='transparent')
frame.pack(pady=10)

from_unit = ctk.CTkComboBox(
    frame,
    values=["m", "km", "cm"],
    width=120,
    text_color='#EACCF7',
    fg_color="#2E0D3B",
    dropdown_fg_color="#260B31",
    dropdown_hover_color="#442352",
    border_color="#3F1650",
    button_hover_color="#442352",
    button_color="#3F1650"
)
from_unit.grid(row=0, column=0, padx=10, pady=10)
from_unit.set("m")

to_unit = ctk.CTkComboBox(
    frame,
    values=["m", "km", "cm"],
    width=120,
    text_color='#EACCF7',
    fg_color="#2E0D3B",
    dropdown_hover_color="#442352",
    dropdown_fg_color="#260B31",
    button_hover_color="#442352",
    border_color="#3F1650",
    button_color="#3F1650"
)
to_unit.grid(row=0, column=1, padx=10, pady=10)
to_unit.set("cm")

result = ctk.CTkLabel(root, text="Result will appear here", font=("Arial", 16), text_color="#C5A2D4")
result.pack(pady=20)

def update_units(choice):
    if choice == "Length":
        units = ["m", "km", "cm"]
    elif choice == "Weight":
        units = ["kg", "g"]
    elif choice == "Temperature":
        units = ["C", "F"]

    from_unit.configure(values=units)
    to_unit.configure(values=units)

    from_unit.set(units[0])
    to_unit.set(units[1])

category.configure(command=update_units)

def convert_length(value, from_unit, to_unit):
    units = {
        "m": 1,
        "km": 1000,
        "cm": 0.01
    }

    # Convert to meters first
    value_in_meters = value * units[from_unit]

    # Convert to target
    return value_in_meters / units[to_unit]

def convert_temp(value, from_unit, to_unit):
    if from_unit == "C" and to_unit == "F":
        return (value * 9/5) + 32
    elif from_unit == "F" and to_unit == "C":
        return (value - 32) * 5/9
    return value

# ------ CONVERT FUNCTION -------
def convert():
    try:
        val = float(entry.get())
        cat = category.get()

        if cat == "Length":
            res = convert_length(val, from_unit.get(), to_unit.get())

        elif cat == "Weight":
            units = {
                "kg": 1,
                "g": 0.001
            }
            value_in_kg = val * units[from_unit.get()]
            res = value_in_kg / units[to_unit.get()]

        elif cat == "Temperature":
            res = convert_temp(val, from_unit.get(), to_unit.get())

        result.configure(text=f"{res:.2f} {to_unit.get()}")

    except:
        result.configure(text="Invalid input ❌")

    result.configure(text=f"{val} {from_unit.get()} = {res:.2f} {to_unit.get()}")

# ------ REVERSE UNITS FUNCTION & BUTTON -------
def swap_units():
    from_val = from_unit.get()
    to_val = to_unit.get()
    from_unit.set(to_val)
    to_unit.set(from_val)

swap_btn = ctk.CTkButton(
    root,
    text="↔ Swap",
    width=100,
    fg_color="#680692",
    hover_color="#9B30FF",
    command=swap_units
)
swap_btn.pack(pady=5)

# ----- CONVERT BUTTON -----
btn = ctk.CTkButton(root, text="Convert", fg_color="#680692", hover_color='#9B30FF', command=convert)
btn.pack(pady=10)

root.mainloop()