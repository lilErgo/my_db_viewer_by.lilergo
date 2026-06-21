"""
    Модуль подключения к бд,
    c библиотекой sqlalchemy,
    для создания подключения и использоваения orm для бд.
"""
from sqlalchemy import create_engine, text


engine = create_engine("mysql+pymysql://root:1782@127.0.0.1:3306/lil_db")


def show_all_tables():
    """
        Метод, который по стандарту показывает все таблицы
    """
    with engine.connect() as conn:
        result = conn.execute(text('SHOW TABLES;'))
    return result.all()


def query_request(query: str):
    """
        Метод в который пишется запрос,
        он уже сам окрывает и закрывает подключение
    """
    with engine.connect() as conn:
        result = conn.execute(text(f'{query}'))
    return result.all()


def table_checker(name_of_table):
    """
        Метод для кнопки(btn1) инспекции таблицы,
        применяется в функции - 'inspector'
    """
    if name_of_table is not None:
        with engine.connect() as conn:
            result = conn.execute(text(f'SELECT * from {name_of_table}'))
        return result.all()


# def ff():
#     try:
#         a = query('select VERSION()')
#         return a
#     except Exception as e:
#         return False
# if ff() != False:
#    print('is  not false')
