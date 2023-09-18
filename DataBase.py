import sqlite3
import json
from aiogram import types

class DataBase:
    def __init__(self) -> None:
        self.db = sqlite3.connect('./DataFrame.db')
        self.cdb = self.db.cursor()

    def create_table(self, name_table, name_columns) -> None:
        self.cdb.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({name_columns})')
        self.db.commit()

    def select(self, select, froms, where=None) -> None:
        if where is not None:
            self.cdb.execute(f'SELECT {select} FROM {froms} WHERE {where}')
        else:
            self.cdb.execute(f'SELECT {select} FROM {froms}')
        self.db.commit()

    def insert(self, insert, select=None, values=None):
        if values is None:
            self.cdb.execute(f'INSERT INTO {insert} SELECT {select}')
        elif select is None:
            self.cdb.execute(f"INSERT INTO {insert} VALUES {values}")
        self.db.commit()

    def update(self, update, set, where=None):
        if where is not None:
            self.cdb.execute (f"UPDATE {update} SET {set} WHERE {where}")
        else:
            self.cdb.execute (f"UPDATE {update} SET {set}")
        self.db.commit()

    def fetchone(self) -> tuple:
        return self.cdb.fetchone()

    def fetchall(self) -> tuple:
        return self.cdb.fetchall()

    def data_save(self, message: types.Message, message_id: str = None) -> list:
        self.select(select='user_id', froms='user', where=f'user_id = {message.chat.id}')
        if self.fetchone() is None:
            self.insert(insert='user (user_id, user_first_name, user_username, user_message_id)', 
                        values=(message.chat.id, 
                                message.chat.first_name if message.chat.first_name is not None else 'null', 
                                message.chat.username if message.chat.username is not None else 'null', 
                                message_id if message_id is not None else 'null'))
        else:
            self.update(update='user', set=f'user_id = {message.chat.id}, user_first_name = "{message.chat.first_name}", user_username = "{message.chat.username}"', where=f'user_id = {message.chat.id}')
        if message_id is not None:
            self.update (update='user', set=f'user_message_id = "{message_id}"', where=f'user_id = {message.chat.id}')
        self.db.commit()
        self.select(select='*', froms='user', where=f'user_id = {message.chat.id}')
        return self.fetchone()

    def plan_save(self, message: types.Message, plan_title: dict = None, plan_title_cor: str = None, plan_date: str = None, plan_date_notif: int = None) -> list: 
        '''
        message - Передаём сообщение идентефикатор\n
        plan_title - Словарь с темой и списком задач. Пример: {"Поесть":["Вкусно", "И точка"]}\n
        plan_date - Когда нужно выполнить список задач\n
        plan_date_notif - Установка времени для напоминания\n\n
        Вывод: (plan_id, user_id, plan_title, plan_title_cor, plan_date, plan_date_notif)
        '''
        self.select(select='user_id', froms='plan', where=f'user_id = {message.chat.id}')
        if self.fetchone() is None:
            self.insert(insert='plan (user_id)', select=f'user_id FROM user WHERE user_id = {message.chat.id}')
            self.update (update='plan', set=f'plan_title = "{new_plan}"', where=f'user_id = {message.chat.id}')
        if plan_title is not None:
            self.update (update='plan', set=f'plan_title = "{plan_title}"', where=f'user_id = {message.chat.id}')
        if plan_title_cor is not None:
            if plan_title_cor == 'None':
                self.update (update='plan', set=f'plan_title_cor = NULL')
            self.update (update='plan', set=f'plan_title_cor = "{plan_title_cor}"', where=f'user_id = {message.chat.id}')
        if plan_date is not None:
            self.update (update='plan', set=f'plan_date = "{plan_date}"', where=f'user_id = {message.chat.id}')
        if plan_date_notif is not None:
            self.update (update='plan', set=f'plan_date_notif = {plan_date_notif}', where=f'user_id = {message.chat.id}')
        self.db.commit()
        self.select(select='*', froms='plan', where=f'user_id = {message.chat.id}')
        exist = list(self.fetchone())
        try:
            exist[2] = eval(exist[2])
            return exist 
        except AttributeError as e:
            print('Ошибка атрибута: ' + str(e))
        except TypeError as e:
            return None

new_plan = {'🧹Бытовуха': ['🪒Побриться', '🪣Помыть машину', '🛏Заправить кровать', '🩺Сходить к врачу', '💊Купить таблеток'], '🍽Купить еды': ['🍣Роллы', '🥐Круассан', '🍞Хлеб', '🍑Персик', '🥝Киви']}
database = DataBase()

database.create_table('user', '''id	            INTEGER,
                            user_id	        BIGINT,
                            user_first_name	TEXT,
                            user_username	TEXT,
                            user_message_id	TEXT,
                            PRIMARY KEY(id AUTOINCREMENT)''')
database.create_table('plan', '''plan_id	        INTEGER ,
                            user_id	        BIGINT,
                            plan_title  	TEXT,
                            plan_title_cor 	TEXT,
                            plan_date   	TEXT,
                            plan_date_notif	INTEGER,
                            PRIMARY KEY(plan_id AUTOINCREMENT),
                            FOREIGN KEY(user_id) REFERENCES user (user_id)''')
