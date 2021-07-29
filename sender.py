from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class Sender:
    def __init__(self, login: str, password: str):
        self.__driver = webdriver.Chrome('chromedriver')
        self.__driver.get("https://www.fonbet.ru/sports/baseball")
        # переходим на страницу авторизации
        element = WebDriverWait(self.__driver, 7).until(
            ec.presence_of_element_located((
                By.XPATH,
                "//a[contains(text(), 'Вход')]"
            ))
        )
        self.__driver.find_element_by_xpath("//a[contains(text(), 'Вход')]").click()
        # получаем поля ввода
        login_in, password_in = self.__driver.find_elements_by_class_name("ui__field")
        login_in.clear()
        password_in.clear()
        login_in.send_keys(login)
        password_in.send_keys(password)
        # завершаем авторизацию
        self.__driver.find_element_by_xpath("//span[contains(text(),'Вход')]").click()

    def bet(self, href: str, quantity: int) -> int:
        """
        :param href: ссылка_на_матч (str)
        :param quantity: размер_ставки (str)
        :return: id ставки
        """
        element = WebDriverWait(self.__driver, 10).until(self.__driver.get(href))
        buttons = element.find_elements_by_xpath(".//div[starts-with(@class, 'row-common--')]")
        buttons[0].find_elements_by_xpath(".//div[starts-with(@class, 'cell-wrap')]")[-1].click()
        input_sum = self.__driver.find_element_by_xpath("//input[starts-with(@class, 'sum-panel__input--')]")
        input_sum.clear()
        input_sum.send_keys(str(quantity))
        try:
            self.__driver.find_element_by_xpath("//div[starts-with(@class, 'place-button__inner--')]").click()
        except:
            print('Поставить не удалось')
            pass
        self.__driver.find_element_by_xpath("//span[starts-with(text(), 'История')]").click()
        id_ = self.__driver.find_element_by_xpath("//div[starts-with(@class, 'caption--')]").text.split()[1]
        return id_


    def get_list_events(self) -> list[tuple]:
        """
        функция для получения списка матчей
        return: list(tuple(arg1:str, arg2:str))
        arg1 - имя_матча
        arg2 - ссылка_на_матч
        """
        events = []
        element = WebDriverWait(self.__driver, 10).until(
            ec.presence_of_element_located((
                By.XPATH,
                "//div[starts-with(@class,'sport-base-event__main--')]"
            ))
        )
        elements = self.__driver.find_elements_by_xpath("//div[starts-with(@class,'sport-base-event__main--')]")
        for elem in elements:
            elem1 = elem.find_element_by_tag_name('a')
            name, href = elem1.text, elem1.get_attribute('href')
            try:
                time = elem.find_element_by_xpath(".//span[starts-with(@class, 'event-block-planned-time__time')]").text
                time_parts = time.split(' ')
                if time_parts[0] == 'Завтра':
                    day = str(datetime.today().date() + timedelta(days=1))
                elif time_parts[0] == 'Сегодня':
                    day = str(datetime.today().date())
                event_time = day + ' ' + time_parts[2]
                events.append((name, href, datetime.strptime(event_time, "%Y-%m-%d %H:%M")))
            except:
                continue
        return events

    def filter_events(self, events: list[tuple]) -> list[tuple]:
        """
        Функция для фильтрации матчей, отбирает только те матчи,
         в которых можно поставить на иннинг
         :param events: Список матчей
         :return: Список отфильтрованных матчей
        """
        filtered_events = []
        for event in events:
            self.__driver.get(event[1])
            try:
                # ожидание полной загрузки страницы, максимально ждем 5 секунд
                element = WebDriverWait(self.__driver, 5).until(
                    ec.presence_of_element_located((
                        By.XPATH,
                        "//div[contains(text(), 'Победа в матче')]"
                    ))
                )
                self.__driver.find_element_by_xpath("//div[contains(text(), 'Кто выиграет иннинг N')]")
                # т.к. начинать ставить мы будем только с первого иннинга
                self.__driver.find_element_by_xpath("//div[contains(text(), 'Иннинг 1')]")
                filtered_events.append(event)
            except Exception:
                continue
        return filtered_events

    def get_history_bets(self):
        """
        Функция для получения истории ставок
        :return: Список диктов с полями:
                    - time - Время ставки
                    - id - Уникальный номер ставки
                    - sum - Сумма ставкки
                    - result - Результат ставки (Выигрыш, Проигрыш)
        """
        self.__driver.get('https://www.fonbet.ru/account/history/bets')
        element = WebDriverWait(self.__driver, 5).until(
            ec.presence_of_element_located((
                By.CLASS_NAME,
                "bets-list__data"
            ))
        )
        bets = self.__driver.find_element_by_class_name('bets-list__data')
        history_bets = bets.find_elements_by_xpath("//div[starts-with(@class, 'operation-row')]")
        history_results = list()
        for i, bet in enumerate(history_bets, 1):
            # если мы находим ячейку с датой не для первого элемента, значит дальше ставки за другой день
            # и нас они не интересуют
            # возможно стоит запоминать время первой ставки из таблицы и сохранять,
            # чтобы при последующем просмотре истории не просматривать старые матчи
            if i != 1:
                try:
                    bet.find_element_by_class_name('column column-1 _hasDate')
                    break
                except:
                    pass
            time = bet.find_element_by_xpath(".//div[contains(@class, 'column column-2')]").text
            id_ = bet.find_element_by_xpath(".//div[contains(@class, 'column column-3')]").text
            sum_ = bet.find_element_by_xpath(".//div[contains(@class, 'column column-5')]").text
            res = bet.find_element_by_xpath(".//div[contains(@class, 'column column-6')]").text
            history_results.append({
                'time': time,
                'id': id_,
                'sum': sum_,
                'result': res
            })

        return history_results

    def close(self):
        self.__driver.close()
