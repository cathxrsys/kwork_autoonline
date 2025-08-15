import time
import random
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

telegram_api = 'YOUR TELEGRAM TOKEN' # telegram bot token for notifications
admin = 00000000 # telegram account id

print('*** Selenium (Firefox) init... ***')
firefox_options = Options()

firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('--no-sandbox')

firefox_options.binary_location = '/snap/firefox/6421/usr/lib/firefox/firefox'  # Путь к Firefox

firefox_options.headless = True  # Запуск в фоне

# Создание драйвера Firefox
driver = webdriver.Firefox(options=firefox_options)
print('*** Firefox init successful ***')

main_page = 'https://kwork.ru/user/your_username'  # Замените на ваш URL
driver.get(main_page)

# Загрузка cookies
try:
    with open('cookies.json', 'r') as f:
        for cookie in json.load(f):
            try:
                driver.add_cookie({'name': cookie['name'], 'value': cookie['value']})
            except Exception as e:
                print(f"Cookie error: {e}")
except FileNotFoundError:
    print("cookies.json не найден")

driver.get(main_page)
message_count = 0

def send_message(chat_id: int, text: str):
    url = f'https://api.telegram.org/bot{telegram_api}/sendMessage'
    requests.get(url, params={'chat_id': chat_id, 'text': text})


while True:
    try:
        t = random.randint(10, 30)
        print(f'Sleeping for {t} seconds...')
        time.sleep(t)
        print(f'Loading {main_page}...')
        driver.get(main_page)

        last_message_count = message_count
        element = driver.find_element(By.CLASS_NAME, 'message-counter')
        message_text = element.text.strip()

        message_count = int(message_text) if message_text else 0

        print(f'last_message_count={last_message_count}')
        print(f'message_count={message_count}')

        if message_count != last_message_count and message_count != 0:
            send_message(admin, 'Получено новое сообщение')

    except Exception as e:
        print(f"Ошибка в цикле: {e}")
        continue
