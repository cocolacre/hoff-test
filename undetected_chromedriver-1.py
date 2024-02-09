from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time, sys
import undetected_chromedriver as uc
#from allure import step

def open_hoff_ru():
    """
    Перейти на страницу каталога https://hoff.ru/catalog/ofis/domashniy_ofis/komputernye_stoly/, 
    -перейти к любому доступному товару. 
    -На открывшейся странице товара проверить, что присутствует кнопка добавления в корзину, кнопка активна и текст соответсвует «Добавить в корзину». 
    -Добавить товар в корзину и 
    -перейти на страницу корзины. 
    -На открывшейся странице проверить, что присутствует пустое поле для ввода телефона с кнопкой «Войти» и в списке товаров 1 единственный добавленный товар. 
    -Проверить, что В поле Итого стоимость самого товара.


    
    """
    driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
    #service = Service(executable_path=driver_path)
    options = Options()
    browser = uc.Chrome()
    url = "https://hoff.ru/catalog/ofis/domashniy_ofis/komputernye_stoly/"
    #browser.get("https://google.com")
    #time.sleep(20)
    browser.get(url)
    time.sleep(10) #replace with EC or WAIT selenium methods.    
    product_link = browser.find_element(By.CLASS_NAME, 'product-preview').get_attribute('href')
    #product_link.get_attribute('href')
    print(f"{product_link=}")
    #product_link.click()
    time.sleep(20)
    browser.get(product_link)
    time.sleep(20)
    sys.exit()
    #browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # переходим на страницу товара
    product_link = browser.find_element(By.XPATH, '//a[@href="/catalog/ofis/domashniy_ofis/komputernye_stoly/komputernyy_stol_dlya_komp_yutera/"]')
    product_link.click()

    # провряем наличие кнопки добавления в корзину
    add_to_cart_button = browser.find_element(By.XPATH, '//button[text()="Добавить в корзину"]')
    assert add_to_cart_button.is_enabled(), "Кнопка добавления в корзину не активна"

    # добавм товар в корзину
    add_to_cart_button.click()

    cart_link = browser.find_element(By.XPATH, '//a[@href="/cart/"]')
    cart_link.click()

    # наличие пустого поля для ввода телефона и кнопки "Войти"
    phone_input = browser.find_element(By.XPATH, '//input[@name="phone"]')
    assert phone_input.get_attribute("value") == "", "Поле для ввода телефона не пустое"

    login_button = browser.find_element(By.XPATH, '//button[text()="Войти"]')
    assert login_button.is_enabled(), "Кнопка Войти не активна"

    # проверяем наличие 1 добавленного товара в корзине
    product_in_cart = browser.find_element(By.XPATH, '//div[@class="cart-item"]')
    assert product_in_cart.is_displayed(), "Товар не добавлен в корзину"

    # проверяем ненулевую стоимость товара
    total_price = browser.find_element(By.XPATH, '//span[@class="total-price"]')
    assert total_price.text != "", "Поле Итого пустое"
if __name__ == "__main__":
    dir(uc)
    open_hoff_ru()
