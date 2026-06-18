from tkinter import * # pyright: ignore[reportWildcardImportFromLibrary]

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError
from mysql_conn import show_all_tables, query,  table_checker
import mysql_conn


LAST_QUERY_FOR_REFRESH = 'SHOW TABLES;'
FIRST_COLUMN = None
SECOND_COLUMN = None

def test(event):
    """
        Тестировка
    """
    print(event)


def str_opt_response_first(event):
    global FIRST_COLUMN
    FIRST_COLUMN = event


def str_opt_response_second(event):
    global SECOND_COLUMN
    SECOND_COLUMN = event


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
    e.delete(0,END)
    return


def onyly_space(str:str):
    import re
    space_checker = re.compile(r'[^\s]')
    if re.search(pattern=space_checker,string=str):
        return False
    return True


def mysql_error_checker(func,query) :
    try:
        a = func(query)
        return a
    except Exception:
        return False


def table_finder():
    try:
        information = str(e.get())
        tables  = show_all_tables()
        if (information == '' or onyly_space(str=information)) == True:
            if db_list_box != None:
                db_list_box.delete(0,END)
            for table in tables:
                table = table[0]
                db_list_box.insert(0,table)
        else:
            check = mysql_error_checker(query,information)
            if check != False:
                global LAST_QUERY_FOR_REFRESH
                LAST_QUERY_FOR_REFRESH = information
                if db_list_box != None:
                    db_list_box.delete(0,END)
                for element in check:
                    element = element[0]
                    db_list_box.insert(0,element)
            else:
                print('Syntax error')
                return None
    except Exception:
        print('Error in table_finder func')


def refresh():
    e.delete(0, END)
    e.insert(0,str(LAST_QUERY_FOR_REFRESH))
    table_finder()
    return


def get_db_list_box():
    try:
        selection = db_list_box.curselection()[0]
    except IndexError:
        return print('Select the table, or promt will be empty')
    select = db_list_box.get(selection)
    return select


def inspector():
    select = get_db_list_box()
    def inspector_interface(select):
        top_l = Toplevel(root)
        inspect_db_list_box = Listbox(top_l)
        inspect_db_list_box.pack(fill=BOTH,expand=1)
        Button(top_l,text='close', command=top_l.destroy).pack()
        check = mysql_error_checker(table_checker,select)
        print(check)
        if check != False  and check  != None:
            for element in check:
                # Преобразуем все элементы в строки
                formatted = ' | '.join(str(item) for item in element)
                inspect_db_list_box.insert(0, formatted)

    return inspector_interface(select=select)

def settings():
    def open_color_window():
        color = Toplevel(settings_top_level)
        Button(color, text='закрыть', command=color.destroy).pack()
    settings_top_level = Toplevel(root)
    settings_top_level.grab_set()
    settings_button = Button(settings_top_level, text='закрыть',
                             command=settings_top_level.destroy)
    settings_button.pack(side=BOTTOM)
    color_button = Button(settings_top_level, text='Цвет',
                          command=open_color_window)
    color_button.pack()
    return


def insert_to_cross_entry_first():
    select = get_db_list_box()
    cross_entry_first.delete(0,END)
    cross_entry_first.insert(0,select)
    column_list_first()
    

def insert_to_cross_entry_second():
    select = get_db_list_box()
    cross_entry_second.delete(0,END)
    cross_entry_second.insert(0,select)
    column_list_second()


def column_list_first():
    result = cross_entry_first.get()
    response = mysql_error_checker(query,query=(f'SHOW COLUMNS FROM {result}'))
    fromatted_response = [x[0] for x in response]
    var = StringVar(value='Не выбранно')
    cross_opt_menu_first = OptionMenu(cross_settings_frame, var ,*fromatted_response, command=str_opt_response_first)
    cross_opt_menu_first.grid(row=0, column=0)
    
    

def column_list_second():
    result = cross_entry_second.get()
    response = mysql_error_checker(query,query=(f'SHOW COLUMNS FROM {result}'))
    fromatted_response =[x[0] for x in response]
    var2 = StringVar(value='Не выбранно')
    cross_opt_menu_second = OptionMenu(cross_settings_frame, var2,*fromatted_response, command=str_opt_response_second)
    cross_opt_menu_second.grid(row=1, column=0)
    


def create_cross_table():
    my_query = f'SELECT * FROM {cross_entry_first.get()} LEFT JOIN {cross_entry_second.get()} ON {cross_entry_first.get()}.{FIRST_COLUMN} = {cross_entry_second.get()}.{SECOND_COLUMN}'
    def create_cross(select):
        top_l = Toplevel(root)
        cross_table = Listbox(top_l)
        cross_table.pack(fill=BOTH,expand=1)
        Button(top_l,text='close', command=top_l.destroy).pack()
        check = mysql_error_checker(query,select)
        # print(check)
        if check != False  and check  != None:
            for element in check:
                # Преобразуем все элементы в строки
                formatted = ' | '.join(str(item) for item in element)
                cross_table.insert(0, formatted)

    return create_cross(select=my_query)
    

def main():
    global root 
    root = Tk()
    root.title('Мой дб вивер')
    root.geometry('1500x900')
    
    # # Создаем основной фрейм
    # main_frame = Frame(root)
    # main_frame.pack(fill=BOTH, expand=True)
    
    # # Создаем DB Viewer внутри основного фрейма
    create_db_viewer(root)
    
    root.mainloop()

def create_db_viewer(parent):
    global e, db_list_box, e_connection, root, cross_entry_first, cross_entry_second, cross_settings_frame
    

    main_frame = Frame(parent)
    # main_frame.pack(fill=BOTH, expand=1) #Раскоментировать если надо запустить программу (вывести интерфейс)  этого файла
    root = parent

    e = Entry(main_frame)
    e.grid(row=0, column=1)

    db_list_box = Listbox(main_frame)
    db_list_box.grid(row=1, column=1)

    btn_connection_label = LabelFrame(main_frame, text='Подключение')
    btn_connection_label.grid(row=0, column=0,)

    e_connection = Entry(btn_connection_label) 
    e_connection.pack(side=TOP)

    btn_connection = Button(btn_connection_label, text='Соединение', command=connection)
    btn_connection.pack()

    btn_workig_label = LabelFrame(main_frame, text='Кнопки рабочие кнопки')
    btn_workig_label.grid(row=1, column=0)

    cross_settings_frame = LabelFrame(main_frame, text='Создание кросс таблицы')
    cross_settings_frame.grid(row=0, column=4)   

    cross_entry_first = Entry(cross_settings_frame)
    cross_entry_first.grid(row=0, column=1)

    cross_entry_second = Entry(cross_settings_frame)
    cross_entry_second.grid(row=1, column=1)

    cross_btn_first = Button(cross_settings_frame, text='Добавить значение в строку', command=insert_to_cross_entry_first)
    cross_btn_first.grid(row=0, column=2)

    cross_btn_second = Button(cross_settings_frame, text='Добавить значение в строку', command=insert_to_cross_entry_second)
    cross_btn_second.grid(row=1, column=2)

    btn1 = Button(btn_workig_label, text='Проинспектировать таблицу', command=inspector)
    btn1.pack()

    btn2 = Button(btn_workig_label, text='Найти', command=table_finder)
    btn2.pack()

    btn3 = Button(btn_workig_label, text='Обновить', command=refresh)
    btn3.pack()

    btn4 = Button(btn_workig_label, text='Очистить', command=e_clean)
    btn4.pack()

    btn5 = Button(main_frame, text='Настройки', command=settings)
    btn5.grid(row=0, column=3, padx=10)

    btn6 = Button(cross_settings_frame, text='Создать кросс таблицу', command=create_cross_table)
    btn6.grid(row=2, column=0, columnspan=2, sticky="nsew")

    return main_frame


if __name__ == '__main__':
    main()