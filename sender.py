from selenium import webdriver


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

    def get_list_events(self):
        """
        функция для получения спискаматчей
        :return:
        """
        pass

    def close(self):
        self.__driver.close()
