import tkinter as tk
import os as sys
import keyboard as kb

pressed_keys = [] #список для збереження натиснутих клавіш

# def create_shortCut():
#     kb.add_hotkey()
#     kb.wait()

def clear_text(btn):
    btn.delete(0,tk.END)
    pressed_keys.clear()

def key_press(event, entry_field):
    pressed_keys.append(event.keysym) #додаємо натиснуті клавіши до множини
    combo = "+".join(pressed_keys)# формуємо строку
    entry_field.delete(0, tk.END)#виводимо комбінацію в текстове поле
    entry_field.insert(0,combo)

def key_release(event, entry_field1):
    pressed_keys.remove(event.keysym)  # Видаляємо клавішу, коли вона відпущена

