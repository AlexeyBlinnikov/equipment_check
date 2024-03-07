import sqlite3 as sq
from create_bot import bot
import pandas
from datetime import date, timedelta
from datetime import datetime

#_______Создаем бд________
# Добавить на какой срок
def sql_start():
    global base, cur
    base = sq.connect('equipment.db')
    cur = base.cursor()
    if base:
        print("Data connect")
    base.execute('CREATE TABLE IF NOT EXISTS equipment(equipment TEXT, name TEXT, date1 TEXT, date2 TEXT, price TEXT)')
    base.commit()

#________Команда добавления в бд_________
async def sql_add_command(values):
    cur.execute('INSERT INTO equipment VALUES (?, ?, ?, ?, ?)', tuple(values))
    base.commit()


#__________Читаем данные бд_____________
def sql_read_date1_today(date_today):
    return cur.execute(f'SELECT * FROM equipment WHERE date1 ==?', (date_today,)).fetchall()
def sql_read_date2_today(date_today):
    return cur.execute(f'SELECT * FROM equipment WHERE date2 ==?', (date_today,)).fetchall()

def sql_read():
    return cur.execute('SELECT * FROM equipment').fetchall()
def sql_read_date2(data):
    return cur.execute('SELECT date2 FROM equipment WHERE ROWID ==?', (data,)).fetchone()
def sql_read_rowid():
    return cur.execute('SELECT ROWID, * FROM equipment').fetchall()

def sql_read_date1_test(d):
    return cur.execute('SELECT date1 FROM equipment WHERE ROWID ==?', (d,)).fetchone()

# для календаря
def dict_factory(cursor, row):
    save_dict = {}
    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]
    return save_dict
def get_all_categories(**kwargs):
    with sq.connect('equipment.db') as con:
        con.row_factory = dict_factory
        sql = f"SELECT ROWID, * FROM equipment"#WHERE price = {shop_id}"
        return con.execute(sql).fetchall()

#____________Обновляем_____________
async def update_sql_extend(date2, rowid):
    cur.execute('UPDATE equipment SET date2 = ? WHERE ROWID ==?', (date2, rowid,))
    base.commit()
async def update_sql_pay(date2, rowid):
    cur.execute('UPDATE equipment SET price = ? WHERE ROWID ==?', (date2, rowid,))
    base.commit()

#____________Удаляем из бд_____________
async def del_sql(data):
    cur.execute('DELETE FROM equipment WHERE ROWID ==?', (data,))
    base.commit()







    # def sql_read_date():
#     # date = []
#     for ret in cur.execute('SELECT * FROM equipment').fetchall():
#         date1 = datetime.strptime(ret[2], '%d.%m.%Y')
#         date2 = datetime.strptime(ret[3], '%d.%m.%Y')
#         x = pandas.date_range(date1,date2-timedelta(days=1),freq='d')
#     return x
        # for i in x:
        # print(x.get_value)
        # await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\n Цена: {ret[-1]}')