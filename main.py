from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Если работаем в Firefox
browser = webdriver.Firefox()

try:
    # Заходим на страницу
    browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")

    # Находим окно поиска
    search_box = browser.find_element(By.ID, "searchInput")

    # Ввод текста
    user_input = input("Введите текст для поиска: ")
    search_box.send_keys(user_input)
    search_box.send_keys(Keys.RETURN)

    # Задержка для загрузки страницы
    time.sleep(3)

    # Кликаем на первый результат поиска
    try:
        a = browser.find_element(By.PARTIAL_LINK_TEXT, user_input)
        a.click()
    except Exception as e:
        print(f"Ошибка: {e}")
        browser.quit()
        exit()

    while True:
        # Выбор действия
        choice = input("Выберите действие: Enter - листать параграфы, 1 - перейти по случайной ссылке, 2 - выход: ")

        if choice == "":
            # Листаем параграфы
            paragraphs = browser.find_elements(By.TAG_NAME, "p")
            for paragraph in paragraphs:
                print(paragraph.text)
                input("Нажмите Enter для продолжения...")

        elif choice == "1":
            # Переход по случайной внутренней ссылке
            try:
                links = WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
                )
                # Фильтруем только внутренние ссылки Википедии.
                internal_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and "/wiki/" in link.get_attribute("href")]
                if internal_links:
                    random_link = random.choice(internal_links)
                    print(f"Переход по внутренней ссылке: {random_link}")
                    browser.get(random_link)
                else:
                    print("Внутренние ссылки не найдены.")
            except Exception as e:
                print(f"Ошибка при переходе по ссылке: {e}")

        elif choice == "2":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

finally:
    browser.quit()
