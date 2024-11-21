import tkinter as tk
from tkinter import messagebox
import os
import keyboard as kb

pressed_keys = [] #список для збереження натиснутих клавіш

def format_key(keysym):
    """
    Приводить `keysym` у формат, що розуміє бібліотека keyboard.
    Наприклад:
      - "Control_L" -> "ctrl"
      - "Alt_L" -> "alt"
      - "Return" -> "enter"
    """
    mapping = {
        "Control_L": "ctrl",
        "Control_R": "ctrl",
        "Alt_L": "alt",
        "Alt_R": "alt",
        "Shift_L": "shift",
        "Shift_R": "shift",
        "Return": "enter",
        "Escape": "esc",
        "BackSpace": "backspace",
        "Delete": "delete",
        "End": "end",
        "Home": "home",
        "Insert": "insert",
        "Page_Up": "pageup",
        "Page_Down": "pagedown",
        "Left": "left",
        "Right": "right",
        "Up": "up",
        "Down": "down",
        "Tab": "tab",
        "Caps_Lock": "capslock",
        "Space": "space",

        "Control_L": "ctrl",
        "Control_R": "ctrl",
        "Alt_L": "alt",
        "Alt_R": "alt",
        "Shift_L": "shift",
        "Shift_R": "shift",
        "Caps_Lock": "capslock",

        # Навігація
        "Tab": "tab",
        "Enter": "enter",
        "Return": "enter",
        "Escape": "esc",
        "BackSpace": "backspace",
        "Delete": "delete",
        "Insert": "insert",
        "Home": "home",
        "End": "end",
        "Page_Up": "pageup",
        "Page_Down": "pagedown",

        # Стрілки
        "Left": "left",
        "Right": "right",
        "Up": "up",
        "Down": "down",

        # Функціональні клавіші
        "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5",
        "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10",
        "F11": "f11", "F12": "f12",

        # Цифровий блок
        "KP_0": "num0", "KP_1": "num1", "KP_2": "num2", "KP_3": "num3",
        "KP_4": "num4", "KP_5": "num5", "KP_6": "num6", "KP_7": "num7",
        "KP_8": "num8", "KP_9": "num9",
        "KP_Divide": "num/", "KP_Multiply": "num*", "KP_Subtract": "num-",
        "KP_Add": "num+", "KP_Enter": "enter", "KP_Decimal": "num.",

        # Символи
        "Space": "space",
        "Exclam": "!", "At": "@", "Hash": "#", "Dollar": "$", "Percent": "%",
        "Caret": "^", "Ampersand": "&", "Asterisk": "*", "ParenLeft": "(",
        "ParenRight": ")", "Minus": "-", "Underscore": "_", "Equal": "=",
        "Plus": "+", "BracketLeft": "[", "BraceLeft": "{", "BracketRight": "]",
        "BraceRight": "}", "BackSlash": "\\", "Bar": "|", "Semicolon": ";",
        "Colon": ":", "Apostrophe": "'", "QuoteDbl": '"', "Comma": ",",
        "Less": "<", "Period": ".", "Greater": ">", "Slash": "/", "Question": "?",
        "Grave": "`", "Tilde": "~",

        # Літери та цифри
        **{f"Key_{chr(i)}": chr(i).lower() for i in range(65, 91)},  # A-Z
        **{f"{i}": str(i) for i in range(10)},  # 0-9
    }
    # Перетворюємо keysym на відповідний формат або повертаємо його без змін
    return mapping.get(keysym, keysym.lower())

def clear_text(btn):
    btn.delete(0,tk.END)
    pressed_keys.clear()

def key_press(event, entry_field):
    key = format_key(event.keysym)

    if key not in pressed_keys:
        pressed_keys.append(key)

    combo = "+".join(pressed_keys)
    entry_field.delete(0, tk.END)#виводимо комбінацію в текстове поле
    entry_field.insert(0,combo)

def key_release(event, entry_field1):
    key = format_key(event.keysym)
    if key in pressed_keys:
        pressed_keys.remove(event.keysym)  # Видаляємо клавішу, коли вона відпущена

def insert_data(list_of_com, input_data):
    data = input_data.get()
    list_of_com.insert(tk.END, data)

def delete_data(list_of_com):
    selected = list_of_com.curselection()

    for i in selected[::-1]:
        list_of_com.delete(i)

def save_to_file(list_of_com):
    try:
        with open("command_file", 'w', encoding='utf-8') as file:
            items = list_of_com.get(0, tk.END)
            for i in items:
                file.write(i + "\n")
        file.close()
    except Exception:
        messagebox.showerror("Сталась помилка")

def load_from_file(list_of_com):
    try:
        with open("command_file", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i in lines:
                shortcut = i.strip()
                list_of_com.insert(tk.END, shortcut)
            try:
                kb.add_hotkey(shortcut, lambda: lambda: os.system("shutdown /s /t 1"))
            except ValueError as e:
                messagebox.showerror("Помилка", f"Неможливо додати комбінацію {shortcut}")
        file.close()

    except FileNotFoundError:
        messagebox.showerror("Файл не знайдено")

def set_command(list_of_com):
    selected_index =list_of_com.curselection()

    if not selected_index:
        messagebox.showerror("Оберіть команду")
        return

    selected_text = list_of_com.get(selected_index[0])
    try:
        kb.add_hotkey(selected_text, lambda: os.system("shutdown /s /t 1"))
        #kb.add_hotkey(selected_text, lambda: messagebox.showinfo("hello"))
    except ValueError as e:
        messagebox.showerror(e)