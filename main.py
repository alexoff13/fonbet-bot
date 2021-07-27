from config import fonbet_login, fonbet_password
from sender import Sender

sender = Sender(fonbet_login, fonbet_password)
print('Успешная авторизация')

# Закрываем браузер
sender.close()
