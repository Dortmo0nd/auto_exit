import tkinter as tk
from tkinter import messagebox
import os
import keyboard as kb
import json

pressed_keys = [] #список для збереження натиснутих клавіш
added_hotkeys = set()  # Це буде містити всі вже додані гарячі клавіші
SETTINGS_FILE = "settings.json"

SYSTEM_SHORTCUTS = {
    # Робота з текстом
    "ctrl+c",  # Копіювати
    "ctrl+v",  # Вставити
    "ctrl+x",  # Вирізати
    "ctrl+z",  # Скасувати
    "ctrl+y",  # Повернути дію
    "ctrl+a",  # Виділити все
    "ctrl+s",  # Зберегти
    "ctrl+p",  # Друк

    # Робота з файлами
    "ctrl+n",  # Новий файл
    "ctrl+o",  # Відкрити файл
    "ctrl+shift+s",  # Зберегти як
    "ctrl+w",  # Закрити вікно/вкладку
    "ctrl+q",  # Вийти з програми

    # Навігація
    "alt+tab",  # Перемикання між вікнами
    "alt+f4",  # Закрити активне вікно
    "win+tab",  # Перемикання між задачами
    "ctrl+tab",  # Перемикання між вкладками
    "ctrl+shift+tab",  # Перемикання назад між вкладками

    # Системні комбінації
    "ctrl+alt+delete",  # Виклик меню системи
    "ctrl+shift+esc",  # Виклик диспетчера задач
    "win+e",  # Провідник
    "win+d",  # Показати/приховати робочий стіл
    "win+r",  # Виконати
    "win+pause",  # Властивості системи
    "win+l",  # Блокування комп'ютера
    "win+shift+s",  # Знімок екрана

    # Інтернет браузери
    "ctrl+t",  # Нова вкладка
    "ctrl+w",  # Закрити вкладку
    "ctrl+shift+t",  # Відкрити закриту вкладку
    "ctrl+l",  # Виділити адресний рядок
    "ctrl+d",  # Додати в закладки
    "ctrl+h",  # Історія
    "ctrl+j",  # Завантаження

    # Редагування
    "ctrl+f",  # Пошук
    "ctrl+h",  # Заміна
    "ctrl+g",  # Перейти до рядка/позиції

    # Медіа
    "media_play_pause",  # Відтворення/пауза
    "media_next",  # Наступний трек
    "media_prev",  # Попередній трек
    "volume_up",  # Збільшення гучності
    "volume_down",  # Зменшення гучності
    "volume_mute",  # Вимкнути звук
    "shift+alt",
}

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

def is_system_shortCut(shortcut):
    return shortcut.lower() in SYSTEM_SHORTCUTS

def clear_text(btn, combo_b):
    btn.delete(0,tk.END)
    combo_b.set('')
    pressed_keys.clear()

def key_press(event, entry_field):
    key = format_key(event.keysym)

    if key not in pressed_keys:
        pressed_keys.append(key)

    combo = "+".join(pressed_keys)
    entry_field.delete(0, tk.END)#виводимо комбінацію в текстове поле
    entry_field.insert(0,combo)

def key_release(event, entry_field):
    key = format_key(event.keysym)
    if key in pressed_keys:
        pressed_keys.remove(key)  # Видаляємо клавішу, коли вона відпущена

def insert_data(list_of_com, input_data, action_combobox):
    data = input_data.get().strip()
    action = action_combobox.get()  # Отримуємо значення з ComboBox

    if not action:
        messagebox.showerror("Помилка", "Оберіть дію для комбінації")
        return

    if is_system_shortCut(data):
        messagebox.showerror("Помилка", f"Комбінація '{data}' є системною та не може бути використана")
        return

    if data in list_of_com.get(0, tk.END):
        messagebox.showinfo("Увага", f"Комбінація '{data}' вже є у списку")
        return

    # Додаємо комбінацію та дію до списку
    list_of_com.insert(tk.END, (data, action))
    kb.add_hotkey(data, lambda sc=data, action=action: execute_command(sc, action))

def delete_data(list_of_com):
    selected = list_of_com.curselection()

    for i in selected[::-1]:
        key_action_pair = list_of_com.get(i)
        shortcut = key_action_pair[0]

        # Видалення гарячої клавіші з реєстрації
        kb.remove_hotkey(shortcut)

        # Видалення комбінації з файлу
        remove_command_from_file(shortcut)

        # Видалення комбінації з списку
        list_of_com.delete(i)

def remove_command_from_file(command):
    try:
        with open("settings.json", "r", encoding="utf-8") as file:
            commands = file.read().splitlines()

        # Видаляємо команду зі списку
        commands = [cmd for cmd in commands if cmd != command]

        # Записуємо оновлений список команд назад у файл
        with open("settings.json", "w", encoding="utf-8") as file:
            for cmd in commands:
                file.write(cmd + "\n")
    except FileNotFoundError:
        messagebox.showerror("Файл не знайдено", "Файл команд відсутній.")

def save_to_file_with_new_command(list_of_com):
    settings = []
    for i in range(list_of_com.size()):
        key_action_pair = list_of_com.get(i)
        settings.append({"keys": key_action_pair[0], "action": key_action_pair[1]})

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)
    messagebox.showinfo("Успіх", "Налаштування успішно збережено")

def load_settings_from_file(list_of_com):
    if not os.path.exists(SETTINGS_FILE):
        return  # Якщо файл не існує, нічого не завантажуємо

    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)

    for setting in settings:
        list_of_com.insert(tk.END, (setting["keys"], setting["action"]))
        kb.add_hotkey(setting["keys"], lambda sc=setting["keys"], action=setting["action"]: execute_command(sc, action))

def execute_command(shortcut, action):
    if shortcut and action:
        if action == "Перезавантаження":
            os.system("shutdown /r /t 1")  # Перезавантаження комп'ютера
            #messagebox.showinfo("Перезавантаження", "Перезавантаження комп'ютера виконано успішно")
        elif action == "Вимкнення":
            os.system("shutdown /s /t 1")  # Вимкнення комп'ютера
            #messagebox.showinfo("Вимкнення", "Вимкнення комп'ютера виконано успішно")
        else:
            messagebox.showinfo("Команда", f"Комбінація {shortcut} з дією '{action}' натискана.")
    else:
        messagebox.showerror("Помилка", "Не визначена комбінація чи дія")

def check_command_in_file(command):
    """
    Перевіряє, чи є команда у файлі. Якщо команди немає, повертає False.
    """
    try:
        with open("command_file.txt", "r", encoding="utf-8") as file:
            commands = file.read().splitlines()
            return command in commands
    except FileNotFoundError:
        return False