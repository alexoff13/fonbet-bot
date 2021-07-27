from selenium import webdriver


class Sender:
    def __init__(self, login: str, password: str):
        driver = webdriver.Chrome('chromedriver')
        driver.get("https://www.fonbet.ru/")
        # переходим на страницу авторизации
        driver.find_element_by_class_name("header-btn").click()
        # получаем поля ввода
        login_in, password_in = driver.find_elements_by_class_name("ui__field")
        login_in.clear()
        password_in.clear()
        login_in.send_keys(login)
        password_in.send_keys(password)
        # завершаем авторизацию
        driver.find_element_by_xpath("//span[contains(text(),'Вход')]").click()

    def get_list_events(self):
        """
        функция для получения спискаматчей
        :return:
        """
        pass