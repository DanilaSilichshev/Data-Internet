from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from pymongo import MongoClient
from time import sleep


def parse_message(message):
    """Функция для парсинга сообщения"""
    title = message.find_element(By.CLASS_NAME, "thread-subject").text
    sender = message.find_element(By.CLASS_NAME, "letter-contact").text
    time = message.find_element(By.CLASS_NAME, "letter__date").text
    body = message.find_element(By.CLASS_NAME, "letter__body").get_attribute("innerHTML")
    return {"title": title, "sender": sender, "time": time, "body": body}


# Подключение к БД
client = MongoClient("localhost", 27017)
db = client["messages"]
messages = db.messages

# Перенаправление к целевому сайту
driver = webdriver.Chrome()
URL = "https://account.mail.ru/login"
driver.get(URL)

try:
    assert "Авторизация" in driver.title
    # Заполнение формы авторизации
    user_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username")))
    user_input.send_keys(input("Введите почтовый адрес: "))
    user_input.send_keys(Keys.ENTER)
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(input("Введите пароль: "))

    # Авторизация, перенаправление на страницу с входящими сообщениями
    password_input.send_keys(Keys.ENTER)

    print(driver.title)
    WebDriverWait(driver, 20).until(
        EC.title_contains("Входящие"))
    print(driver.title)

    # Получение html-элемента первого письма
    sleep(1)
    first_message_block = driver.find_element(By.CSS_SELECTOR, "a.llc")
    first_message_block.click()

    # Обход всех писем
    i = 1
    while True:
        try:
            sleep(1)
            print(f"Начало парсинга {i} письма")

            # Парсинг письма
            message_info = parse_message(driver)

            # Добавление новой записи в БД
            id_field = hash(message_info.get("title") + message_info.get("time") + message_info.get("sender"))
            if messages.find_one({"_id": id_field}) is None:
                messages.insert_one({
                    "_id": id_field,
                    "title": message_info.get("title"),
                    "sender": message_info.get("sender"),
                    "time": message_info.get("time"),
                    "body": message_info.get("body")
                })

            # Нахождение кнопки для перенаправления к следующему письму
            next_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-title-shortcut='Ctrl+↓']")))

            print(f"Конец парсинга {i} письма")
            i += 1
            next_button.click()
        except exceptions.TimeoutException:
            print("Парсинг входящих писем завершён")
            break
except AssertionError:
    print("Вы не находитесь на странице с формой для авторизации")

driver.quit()
