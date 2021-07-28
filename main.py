from config import fonbet_login, fonbet_password
from sender import Sender

sender = Sender(fonbet_login, fonbet_password)
print('Успешная авторизация')

# Тестирование фильтрации
events = [
    ('валидный матч',
     'https://www.fonbet.ru/sports/baseball/11676/29117722'
     ),
    (
        'невалидный матч',
        'https://www.fonbet.ru/sports/baseball/11676/29117717'
    )]
filtered_events = sender.filter_events(events)
print(filtered_events)
# Закрываем браузер
sender.close()
