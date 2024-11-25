import tkinter as tk
from tkinter import ttk
import functional as func

# Створення головного вікна
root = tk.Tk()

root.title("Auto exit from Windows")
root.geometry("330x230")
root.resizable(width=False, height=False)
ACTIONS = ["Перезавантаження", "Вимкнення"]

add_lable1 = ttk.Label(root, text="Оберіть необхідні клавіші: ")
add_lable1.place(x=12, y=0)

add_bind1 = ttk.Entry(root, width=22)
add_bind1.place(x=15, y=20)

action_label = ttk.Label(root, text="Виберіть дію:")
action_label.place(x=175, y=0)

action_combobox = ttk.Combobox(root, values=ACTIONS, state="readonly")
action_combobox.place(x=175, y=20)

add_btn1 = ttk.Button(root, text="Додати ShortCut", command=lambda: func.insert_data(list_of_command1,add_bind1, action_combobox))
add_btn1.place(x=183, y=110)

clear_Entry = ttk.Button(root, text = "Очистити поле", command= lambda: func.clear_text(add_bind1, action_combobox))
clear_Entry.place(x=15, y=45)

list_of_command1 = tk.Listbox(root, height=4, width=25)
list_of_command1.place(x=15, y=100)

delete_btn1 = ttk.Button(root, text="Видалити ShortCut", command = lambda: func.delete_data(list_of_command1))
delete_btn1.place(x=183, y=140)

exit_btn1 = ttk.Button(root, text="Вихід", command=root.destroy)
exit_btn1.place(x=15, y=185)

save_btn1 = ttk.Button(root, text="Зберегти", command = lambda: func.save_to_file_with_new_command(list_of_command1))
save_btn1.place(x=90, y=185)

# Прив'язуємо обробники натискання і відпускання клавіш
root.bind("<KeyPress>", lambda event: func.key_press(event,add_bind1))
root.bind("<KeyRelease>", lambda event: func.key_release(event,add_bind1))

func.load_settings_from_file(list_of_command1)
root.mainloop()