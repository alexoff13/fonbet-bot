from config import fonbet_login, fonbet_password
from sender import Sender

sender = Sender(fonbet_login, fonbet_password)
print('Успешная авторизация')

history = sender.get_history_bets()
print(history)
# Закрываем браузер
sender.close()
