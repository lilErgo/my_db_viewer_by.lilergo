"""
    Модуль работы с my_sql
"""
# from tkinter import * # pyright: ignore[reportWildcardImportFromLibrary]
# pylint: disable=invalid-name
# pylint: disable=global-statement
# pylint: disable=global-variable-undefined
import re
from tkinter import (
    Tk, Frame, LabelFrame,
    Listbox, Entry, Button,
    Toplevel, StringVar, OptionMenu,
    BOTH, TOP, END, BOTTOM
)
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError
from mysql_conn import show_all_tables, query_request,  table_checker
import mysql_conn


LAST_QUERY_FOR_REFRESH = 'SHOW TABLES;'
first_column = None
second_column = None

ROOT = None


def test(event):
    """
        Тестировка
    """
    print(event)


def str_opt_response_first(event):
    """
        Задаёт значение константы, какой именно констынты смотерть по названию
        константы.
    """
    global first_column
    first_column = event


def str_opt_response_second(event):
    """
        Задаёт значение константы, какой именно констынты смотерть по названию
        константы.
    """
    global second_column
    second_column = event


def connection():
    """
        Подключение к mysql
    """
    stable_url = mysql_conn.engine

    try:
        connection_string = str(e_connection.get())
        mysql_conn.engine = create_engine(f'{connection_string}')
    except ArgumentError:
        print('Не правильная ссылка')
        mysql_conn.engine = stable_url
        return mysql_conn.engine


def e_clean():
    """
        Очищает окно ввода - е
    """
    e.delete(0, END)
    return


def onyly_space(string: str):
    """
        Проверяет на наличие пробела
    """
    space_checker = re.compile(r'[^\s]')
    if re.search(pattern=space_checker, string=string):
        return False
    return True


def mysql_error_checker(func, query):
    """
        Проверяет подключение к mysql
    """
    try:
        a = func(query)
        return a
    except mysql.connector.Error as er:
        print(f"MySQL error: {er}")
        return False
    except (ValueError, TypeError) as er:
        print(f"Value/Type error: {er}")
        return False


def table_finder():
    """
        Осуществляет поиск таблиц
    """
    try:
        information = str(e.get())
        tables = show_all_tables()
        if information == '' or onyly_space(string=information):
            if db_list_box is not None:
                db_list_box.delete(0, END)
            for table in tables:
                table = table[0]
                db_list_box.insert(0, table)
        else:
            check = mysql_error_checker(query_request, information)
            if check is not False:
                global LAST_QUERY_FOR_REFRESH
                LAST_QUERY_FOR_REFRESH = information
                if db_list_box is not None:
                    db_list_box.delete(0, END)
                for element in check:
                    element = element[0]
                    db_list_box.insert(0, element)
            else:
                print('Syntax error')
                return None
    except mysql.connector.Error as er:
        print(f"Ошибка базы данных: {er}")

    except (ValueError, TypeError, AttributeError) as er:
        print(f"Ошибка данных: {er}")

    except Exception as er:  # pylint: disable=broad-exception-caught
        print(f"Ошибка в table_finder: {er}")


def refresh():
    """
        Обновляет окно ввода - e
    """
    e.delete(0, END)
    e.insert(0, str(LAST_QUERY_FOR_REFRESH))
    table_finder()
    return


def get_db_list_box() -> str | None:
    """
        Возвращает результат по нажатому полю в db_list_box
    """
    try:
        selection = db_list_box.curselection()[0]
    except IndexError:
        print('Select the table, or promt will be empty')
        return None
    select = db_list_box.get(selection)
    return str(select)


def inspector():
    """
        Инспектирует таблицу
    """
    select = get_db_list_box()

    def inspector_interface(select):
        top_l = Toplevel(ROOT)
        inspect_db_list_box = Listbox(top_l)
        inspect_db_list_box.pack(fill=BOTH, expand=1)
        Button(top_l, text='close', command=top_l.destroy).pack()
        check = mysql_error_checker(table_checker, select)
        print(check)
        if check is not False and check is not None:
            for element in check:
                # Преобразуем все элементы в строки
                formatted = ' | '.join(str(item) for item in element)
                inspect_db_list_box.insert(0, formatted)
    return inspector_interface(select=select)


def settings():
    """
        Настройки
    """
    def open_color_window():
        color = Toplevel(settings_top_level)
        Button(color, text='закрыть', command=color.destroy).pack()
    settings_top_level = Toplevel(ROOT)
    settings_top_level.grab_set()
    settings_button = Button(settings_top_level, text='закрыть',
                             command=settings_top_level.destroy)
    settings_button.pack(side=BOTTOM)
    color_button = Button(settings_top_level, text='Цвет',
                          command=open_color_window)
    color_button.pack()
    return


def insert_to_cross_entry_first():
    """
        Вставляет данные в первое окно ввода для кросс таблицы
    """
    select = get_db_list_box()
    cross_entry_first.delete(0, END)
    cross_entry_first.insert(0, str(select))
    column_list_first()


def insert_to_cross_entry_second():
    """
        Вставляет данные во второе окно ввода для кросс таблицы
    """
    select = get_db_list_box()
    cross_entry_second.delete(0, END)
    cross_entry_second.insert(0, str(select))
    column_list_second()


def column_list_first():
    """
        Отображает все названия колонок в 2 выпадающем списке
    """
    result = cross_entry_first.get()
    response = mysql_error_checker(
        query_request,
        query=f'SHOW COLUMNS FROM {result}'
    )
    if isinstance(response, list):
        fromatted_response = [x[0] for x in response]
        var = StringVar(value='Не выбранно')
        cross_opt_menu_first = OptionMenu(
            cross_settings_frame, var,
            *fromatted_response, command=str_opt_response_first
        )
        cross_opt_menu_first.grid(row=0, column=0)


def column_list_second():
    """
        Отображает все названия колонок в 2 выпадающем списке
    """
    result = cross_entry_second.get()
    response = mysql_error_checker(
        query_request,
        query=(f'SHOW COLUMNS FROM {result}')
    )
    if isinstance(response, list):
        fromatted_response = [x[0] for x in response]
        var2 = StringVar(value='Не выбранно')
        cross_opt_menu_second = OptionMenu(
            cross_settings_frame, var2,
            *fromatted_response, command=str_opt_response_second
        )
        cross_opt_menu_second.grid(row=1, column=0)


def create_cross_table():
    """
        Создаёт кросс таблицу
    """
    my_query = f'SELECT * FROM {cross_entry_first.get()}\
                 LEFT JOIN {cross_entry_second.get()}\
                 ON {cross_entry_first.get()}.{first_column} = \
                 {cross_entry_second.get()}.{second_column}'

    def create_cross(select):
        top_l = Toplevel(ROOT)
        cross_table = Listbox(top_l)
        cross_table.pack(fill=BOTH, expand=1)
        Button(top_l, text='close', command=top_l.destroy).pack()
        check = mysql_error_checker(query_request, select)
        # print(check)
        if check is not False and check is not None:
            for element in check:
                # Преобразуем все элементы в строки
                formatted = ' | '.join(str(item) for item in element)
                cross_table.insert(0, formatted)
    return create_cross(select=my_query)


def main():
    """
        Запускатся как обычное приложение
    """
    global ROOT
    root = Tk()
    root.title('Мой дб вивер')
    root.geometry('1500x900')
    ROOT = root
    # # Создаем основной фрейм
    # main_frame = Frame(root)
    # main_frame.pack(fill=BOTH, expand=True)
    # # Создаем DB Viewer внутри основного фрейма
    create_db_viewer(root).pack(fill=BOTH, expand=1)
    root.mainloop()


def create_db_viewer(parent):
    """
        Запуск как модуль
    """
    global e, db_list_box, e_connection, ROOT
    global cross_entry_first, cross_entry_second, cross_settings_frame
    ROOT = parent
    main_frame = Frame(parent)

    e = Entry(main_frame)
    e.grid(row=0, column=1)

    db_list_box = Listbox(main_frame)
    db_list_box.grid(row=1, column=1)

    btn_connection_label = LabelFrame(main_frame, text='Подключение')
    btn_connection_label.grid(row=0, column=0,)

    e_connection = Entry(btn_connection_label)
    e_connection.pack(side=TOP)

    btn_connection = Button(btn_connection_label,
                            text='Соединение', command=connection)
    btn_connection.pack()

    btn_workig_label = LabelFrame(main_frame, text='Кнопки рабочие кнопки')
    btn_workig_label.grid(row=1, column=0)

    cross_settings_frame = LabelFrame(main_frame,
                                      text='Создание кросс таблицы')
    cross_settings_frame.grid(row=0, column=4)

    cross_entry_first = Entry(cross_settings_frame)
    cross_entry_first.grid(row=0, column=1)

    cross_entry_second = Entry(cross_settings_frame)
    cross_entry_second.grid(row=1, column=1)

    cross_btn_first = Button(cross_settings_frame,
                             text='Добавить значение в строку',
                             command=insert_to_cross_entry_first)
    cross_btn_first.grid(row=0, column=2)

    cross_btn_second = Button(cross_settings_frame,
                              text='Добавить значение в строку',
                              command=insert_to_cross_entry_second)
    cross_btn_second.grid(row=1, column=2)

    btn1 = Button(btn_workig_label,
                  text='Проинспектировать таблицу',
                  command=inspector)
    btn1.pack()

    btn2 = Button(btn_workig_label, text='Найти', command=table_finder)
    btn2.pack()

    btn3 = Button(btn_workig_label, text='Обновить', command=refresh)
    btn3.pack()

    btn4 = Button(btn_workig_label, text='Очистить', command=e_clean)
    btn4.pack()

    btn5 = Button(main_frame, text='Настройки', command=settings)
    btn5.grid(row=0, column=3, padx=10)

    btn6 = Button(cross_settings_frame,
                  text='Создать кросс таблицу', command=create_cross_table)
    btn6.grid(row=2, column=0, columnspan=2, sticky="nsew")

    return main_frame


if __name__ == '__main__':
    main()
