from config import fonbet_login, fonbet_password
from sender import Sender
from db import Db

sender = Sender(fonbet_login, fonbet_password)
print('Успешная авторизация')

history = sender.get_history_bets()
print(history)
# Закрываем браузер
sender.close()

db_worker = Db(path='/home/zak/PycharmProjects/fonbet-bot/', name='bets')
db_worker.insert_bets([(123, 'https://www.fonbet.ru/sports/baseball/11676/29152512', 1), (321, 'https://www.fonbet.ru/sports/baseball/11676/29152512', 1)])
db_worker.update_bets(321, -1)
