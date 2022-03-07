import sqlite3 as sql
from datetime import datetime, timedelta

conn = sql.connect ('bd/bd.db')
cursor = conn.cursor()

def how_many_days (datetime1):
    dt1 = datetime.strptime (str(datetime1), "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow()
    return (now - dt1).days

def get_user (chat_id, user_id):
    return cursor.execute (f"SELECT * FROM users WHERE Chat = '{chat_id}' AND person='{user_id}'").fetchone()

def get_base (chat_id):
    return cursor.execute (f"SELECT * FROM chatlist WHERE Chat_id = '{chat_id}'").fetchone()

def normalizetime(chat_id, user_id):
    person = cursor.execute (f"SELECT * FROM users WHERE Chat = '{chat_id}' AND person='{user_id}'").fetchone()
    group = cursor.execute (f"SELECT * FROM chatlist WHERE Chat_id = '{chat_id}'").fetchone()
    value = datetime.strptime (str(person[2]), "%Y-%m-%d %H:%M:%S") - timedelta(days=group[1]+1)
    cursor.execute ("UPDATE users set Join_date = \'{}\' where Chat = \'{}\' AND person=\'{}\'".format (value, chat_id, user_id))
    conn.commit()

def add_new_user (chat_id, user_id):
    cursor.execute(f"INSERT into users ('Chat', 'person') values ('{chat_id}', '{user_id}') ")
    conn.commit()

def add_new_base (chat_id):
    cursor.execute(f"INSERT into chatlist ('Chat_id') values ('{chat_id}')")
    conn.commit()

def delete_entry (chat_id, user_id):
    cursor.execute (f"DELETE FROM users WHERE Chat = (?) AND person= (?)", (chat_id, user_id,))
    conn.commit()

def update_user (chat_id, user_id, value):
    cursor.execute ("UPDATE users set Reports = \'{}\' where Chat = \'{}\' AND person=\'{}\'".format (value, chat_id, user_id))
    conn.commit()

def update_base (chat_id, AntiBotLimitation, NeedReportsForBan, Lang, NeedMentioneBot):

    cursor.execute ("UPDATE chatlist set AntiBotLimitation = {}, NeedReportsForBan = {}, Language__ = \'{}\', NeedMentioneBot = {} where Chat_id = \'{}\'".format(AntiBotLimitation, NeedReportsForBan, Lang, NeedMentioneBot, chat_id))
    conn.commit()
