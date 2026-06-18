from sqlalchemy import create_engine, text


engine = create_engine("")

def show_all_tables():      
    with engine.connect()  as conn:
        result = conn.execute(text('SHOW TABLES;'))
    return result.all()

def query(query:str):
    with engine.connect() as conn:
        result = conn.execute(text(f'{query}'))
    return result.all()

def table_checker(name_of_table):
    if name_of_table != None:
        with engine.connect()  as conn:
            result = conn.execute(text(f'SELECT * from {name_of_table}'))
        return result.all()



def ff():
    try:
        a = query('select VERSION()')
        return a
    except Exception as e:
        return False
        
if ff() != False:
    print('is  not false')