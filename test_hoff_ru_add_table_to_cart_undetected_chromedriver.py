from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time, sys
import undetected_chromedriver as uc # для обхода блокировки селениума сервером (ошибки 403)
#from allure import step

from locators import *


def test_hoff_ru():
    #driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
    browser = uc.Chrome()
    #url = "https://hoff.ru/catalog/ofis/domashniy_ofis/komputernye_stoly/"
    browser.get(HOFF_COMPUTER_TABLES_URL)
    
    # перейти к любому доступному товару
    product_preview_element = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, PRODUCT_PREVIEW_ELEMENT_CLASS_NAME)))
    #print("product_link LOADED.")
    product_link = product_preview_element.get_attribute('href')
    #product_link = browser.find_element(By.CLASS_NAME, PRODUCT_PREVIEW_ELEMENT_CLASSNAME).get_attribute('href')

    #print(f"{product_link=}")
    browser.get(product_link)
    product_basket_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, PRODUCT_BASKET_CLASS_NAME)))
    
    # цена товара для сравнения с суммой в корзине.
    price_actual_span = browser.find_element(By.CLASS_NAME, PRICE_ACTUAL_CLASS_NAME)
    # извлечём цифры и сформируем цену товара в виде числа.
    price_actual = int("".join([char for char in price_actual_span.text if char.isnumeric()]))
    #print(f"{price_actual=}")

    # кнопка добавления товара в корзину активна ?
    assert not product_basket_button.get_attribute("disabled"), "Кнопка добавления товара в корзину не активна"

    # соглашаемся с выбором нашего предполагаемого города, если нужно.
    try:
        button_decline = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, BUTTON_CITY_SELECTION_DECLINE_CLASS_NAME)))
        button_decline.click()
        time.sleep(2)
    except Exception as _e:
        print(str(_e))
    
    # соглашаемся с использованием cookie, если нужно.
    try: 
        button_coockie_agree = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, COOCKIE_AGREE_BUTTON_CLASS_NAME)))
        button_coockie_agree.click()
        time.sleep(2) # можно заменить на проверку кликабельности кнопки добавления товара в корзину.
    except Exception as _e:
        print(str(_e))

    # добавим товар в корзину.
    # replace with EC ?
    span_basket_button_text_general = browser.find_element(By.CLASS_NAME, 'btn-text__general') 
    basket_button_text_general = span_basket_button_text_general.text
    #print(f"{basket_button_text_general.lower().strip()=}")
    product_basket_button.click()
    time.sleep(5) # дадим браузеру время обновить надпись на кнопке

    # проверим, что товар добавлен в корзину.
    product_basket_button = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-basket-button')))
    #print(f"BUTTON TEXT:[{product_basket_button.text=}]")
    assert product_basket_button.text == "Товар в корзине", "Текст на кнопке добавления в корзину не соответствует 'Товар в корзине', вероятно товар не добавлен в корзину."

    # откроем страницу корзины напрямую.
    browser.get('https://hoff.ru/basket/')
    

    phone_number_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-input__field')))
    input_value = phone_number_input.get_attribute("value")
    #print(f"{input_value=}")
    # присутствует пустое поле для ввода телефона?
    assert input_value == '', "Поле для ввода телефона не пустое!"

    # TODO: Вынести локаторы в отдельный файл с константами и отрефакторить!
    # присутствует кнопка «Войти»?
    basket_auth_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'basket-auth__button')))
    basket_auth_button_text = basket_auth_button.text
    assert basket_auth_button_text.strip() == "Войти", "Отсутствует кнопка 'Войти'!" 

    # Теперь извлечём из DOM суммарную стоимость товаров в корзине и сравним с ценой выбранного стола.
    basket_title = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'basket__title')))
    basket_title_text = basket_title.text
    #print(f'{basket_title_text=}')
    num_added_goods = int(basket_title_text.split(" ")[0])
    #print(f"{num_added_goods=}")
    assert num_added_goods == 1, "В списке товаров в корзине не один товар!" # в списке товаров 1 единственный добавленный товар

    # В поле Итого стоимость самого товара ?
    basket_summary_total_price = browser.find_element(By.CLASS_NAME, "basket-summary__total-price")
    total_price_span = basket_summary_total_price.find_element(By.TAG_NAME, "span")
    total_price = int(total_price_span.text.replace(" ",""))
    #print(f"{total_price=}")
    assert total_price == price_actual, "Число в поле Итого не соответствует стоимости товара! "
    
    print("Тест успешен, задание выполнени!")

if __name__ == "__main__":
    test_hoff_ru()
