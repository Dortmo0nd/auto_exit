import tkinter as tk
from tkinter import ttk
import functional as func


# Створення головного вікна
root = tk.Tk()

root.title("Auto exit from Windows")
root.geometry("310x300")
root.resizable(width=False, height=False)

add_lable1 = ttk.Label(root, text="Введіть необхідні клавіші: ")
add_lable1.place(x=12, y=0)

add_bind1 = ttk.Entry(root, width=22)
add_bind1.place(x=15, y=20)

add_btn1 = ttk.Button(root, text="Додати ShortCut")
add_btn1.place(x=183, y=15)

clear_Entry = ttk.Button(root, text = "Очистити поле", command= lambda: func.clear_text(add_bind1))
clear_Entry.place(x=15, y=45)

list_of_command1 = tk.Listbox(root, height=4, width=25)
list_of_command1.place(x=15, y=100)

delete_btn1 = ttk.Button(root, text="Видалити ShortCut")
delete_btn1.place(x=183, y=140)

select_btn1 = ttk.Button(root, text="Обрати ShortCut")
select_btn1.place(x=183, y=100)

exit_btn1 = ttk.Button(root, text="Вихід", command=root.destroy)
exit_btn1.place(x=15, y=185)

save_btn1 = ttk.Button(root, text="Зберегти")
save_btn1.place(x=75, y=185)

# Прив'язуємо обробники натискання і відпускання клавіш
root.bind("<KeyPress>", lambda event: func.key_press(event,add_bind1))
root.bind("<KeyRelease>", lambda event: func.key_release(event,add_bind1))

root.mainloop()
