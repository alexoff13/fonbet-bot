from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class Sender:
    def __init__(self, login: str, password: str):
        self.__driver = webdriver.Chrome('chromedriver')
        self.__driver.get("https://www.fonbet.ru/")
        # переходим на страницу авторизации
        self.__driver.find_element_by_class_name("header-btn").click()
        # получаем поля ввода
        login_in, password_in = self.__driver.find_elements_by_class_name("ui__field")
        login_in.clear()
        password_in.clear()
        login_in.send_keys(login)
        password_in.send_keys(password)
        # завершаем авторизацию
        self.__driver.find_element_by_xpath("//span[contains(text(),'Вход')]").click()

    def get_list_events(self) -> list[tuple]:
        """
        функция для получения списка матчей
        return: list(tuple(arg1:str, arg2:str))
        arg1 - имя_матча
        arg2 - ссылка_на_матч
        """
        events = []
        elements = self.__driver.find_elements_by_class_name("sport-base-event__main--Zg9I0")
        for elem in elements:
            elem = elem.find_element_by_tag_name('a')
            name, href = elem.text, elem.get_attribute('href')
            events.append((name, href))
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
                filtered_events.append(event)
            except Exception:
                continue
        return filtered_events

    def close(self):
        self.__driver.close()
