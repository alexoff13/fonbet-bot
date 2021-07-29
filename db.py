import sqlite3

#examples:
# 1. object_class_db = Db(path='/home/zak/PycharmProjects/fonbet-bot/', name='bets')
# 2. object_class_db.insert_bets([(12312332, 'https://www.fonbet.ru/sports/baseball/11676/29152512', 1)])
# 3. object_class_db.update_bets(12312332, -1)

class Db:
    def __init__(self, path: str, name: str):
        try:
            self.__connect = sqlite3.connect(f'{path}{name}.db')
        except:
            print('Подключение не удалось')
            return
        self.__cursor = self.__connect.cursor()

    def close(self): self.__connect.close()

    def insert_bets(self, data: list[tuple]):
        q = 'insert into bets values (?, ?, ?)'
        self.__cursor.executemany(q, data)
        self.__connect.commit()

    def update_bets(self, id: int, is_actual: int):
        q = f'update bets set is_actual = {is_actual} where id = {id}'
        self.__cursor.execute(q)
        self.__connect.commit()

    def insert_history(self, data: list[tuple]):
        q = 'insert into history values (?, ?, ?, ?, ?)'
        self.__cursor.executemany(q, data)
        self.__connect.commit()

    def insert_shedule(self, data: list[tuple]):
        q = 'insert into shedule values (?, ?, ?)'
        self.__cursor.executemany(q, data)
        self.__connect.commit()






