"""tkinter GUI"""
from tkinter import Tk, Label, LabelFrame, Button, BOTH, LEFT, X

import my_db_viewer


def show_menu(number: int) -> None:
    """
        Функция итерации для перехода между окнами
    """
    for child in label_menu_bottom.pack_slaves():
        child.pack_forget()
    labels[number - 1].pack(fill=BOTH, expand=True)


root = Tk()
root.geometry('1300x300')

label_menu_top = LabelFrame(root, background='green', text='Menu')
label_menu_top.pack(fill=X)

label_menu_bottom = LabelFrame(root, background='green', text='Информация')
label_menu_bottom.pack(fill=BOTH, expand=True)

labels = [
    my_db_viewer.create_db_viewer(label_menu_bottom),
    Label(label_menu_bottom, text='2', font=('Arial', 50)),
    Label(label_menu_bottom, text='3', font=('Arial', 50)),
    Label(label_menu_bottom, text='4', font=('Arial', 50)),
    Label(label_menu_bottom, text='5', font=('Arial', 50)),
    Label(label_menu_bottom, text='6', font=('Arial', 50))
]

btn_menu1 = Button(label_menu_top, text='Первая кнопка меню',
                   command=lambda: show_menu(1))
btn_menu1.pack(side=LEFT, fill='x', expand=True, pady=10)

btn_menu2 = Button(label_menu_top, text='Вторая кнопка меню',
                   command=lambda: show_menu(2))
btn_menu2.pack(side=LEFT, fill='x', expand=True, pady=10)

btn_menu3 = Button(label_menu_top, text='Третья кнопка меню',
                   command=lambda: show_menu(3))
btn_menu3.pack(side=LEFT, fill='x', expand=True, pady=10)

btn_menu4 = Button(label_menu_top, text='Четврертая кнопка меню',
                   command=lambda: show_menu(4)
                   )
btn_menu4.pack(side=LEFT, fill='x', expand=True, pady=10)

btn_menu5 = Button(label_menu_top, text='Пятая кнопка меню',
                   command=lambda: show_menu(5))
btn_menu5.pack(side=LEFT, fill='x', expand=True, pady=10)

btn_menu6 = Button(label_menu_top, text='Шестая кнопка меню',
                   command=lambda: show_menu(6))
btn_menu6.pack(side=LEFT, fill='x', expand=True, pady=10)

root.mainloop()
