from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time, sys
import undetected_chromedriver as uc # для обхода блокировки селениума сервером (ошибки 403)
#from allure import step

def test_hoff_ru():
    """
    Перейти на страницу каталога https://hoff.ru/catalog/ofis/domashniy_ofis/komputernye_stoly/, 
    -перейти к любому доступному товару. 
    -На открывшейся странице товара проверить, что 
        1) присутствует кнопка добавления в корзину, 
            c-button c-button-red product-basket-button
        2) кнопка активна 
            ???
            <button><span> .btn-text__desktop

            if not button.get_attribute("disabled"):
                print("The button is active")
            else:
                print("The button is disabled")
        3) и текст соответсвует «Добавить в корзину». 
            <span> в корзину
        

    -Добавить товар в корзину и 
        "Товар добавлен" - c-modal-basket__title
            <svg>Товар в&nbsp;корзине
            child_elements = button.find_elements_by_tag_name("span")
            for child in child_elements:
                # Extract the text from the child element
                text = child.text
                # Concatenate the text to the concatenated text
                concatenated_text += text
             <button>Товар в корзине</button> 
    -перейти на страницу корзины. 
        class="basket-button button"
        href /basket/
            https://hoff.ru/basket/

    -На открывшейся странице проверить, что 
        1) присутствует пустое поле для ввода телефона
            .c-input__field
            <input>
            .c-input__field
            placeholder="+7 999 999 99 99"
            input_value = input_element.get_attribute("value")
            input_value = driver.execute_script("return arguments[0].value", input_element)
            document.querySelector('input[type=tel]').value !!!!!!!!!

        2)с кнопкой «Войти»  
            c-button c-button-red basket-auth__button
            <button> "Войти"
        3) и в списке товаров 1 единственный добавленный товар.
            <h2>
            .basket__title
            1 товар в корзине

    -Проверить, что В поле Итого стоимость самого товара.
        <span> .basket-summary__total-price
            <span>7 999
    
    """
    #driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
    #options = Options()
    browser = uc.Chrome()
    url = "https://hoff.ru/catalog/ofis/domashniy_ofis/komputernye_stoly/"
    browser.get(url)
    
    # перейти к любому доступному товару
    product_link = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-preview')))
    print("product_link LOADED.")
    product_link = browser.find_element(By.CLASS_NAME, 'product-preview').get_attribute('href')

    print(f"{product_link=}")
    browser.get(product_link)
    product_basket_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-basket-button')))
    
    # цена товара для сравнения с суммой в корзине.
    price_actual_span = browser.find_element(By.CLASS_NAME, "price-actual")
    # извлечём цифры и сформируем цену товара в виде числа.
    price_actual = int("".join([char for char in price_actual_span.text if char.isnumeric()]))
    print(f"{price_actual=}")

    # кнопка добавления товара в корзину активна ?
    assert not product_basket_button.get_attribute("disabled"), "Кнопка добавления товара в корзину не активна"

    # соглашаемся с выбором нашего предполагаемого города, если нужно.
    try:
        button_decline = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'decline')))
        button_decline.click()
        time.sleep(2)
    except Exception as _e:
        print(str(_e))
    
    # соглашаемся с использованием cookie, если нужно.
    try: 
        button_coockie_agree = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'exponea-banner__btn')))
        button_coockie_agree.click()
        time.sleep(2) # можно заменить на проверку кликабельности кнопки добавления товара в корзину.
    except Exception as _e:
        print(str(_e))

    # добавим товар в корзину.
    # replace with EC ?
    span_basket_button_text_general = browser.find_element(By.CLASS_NAME, 'btn-text__general') 
    basket_button_text_general = span_basket_button_text_general.text
    print(f"{basket_button_text_general.lower().strip()=}")
    product_basket_button.click()
    time.sleep(5) # дадим браузеру время обновить надпись на кнопке
    #print("clicked button.")

    # проверим, что товар добавлен в корзину.
    product_basket_button = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-basket-button')))
    print(f"BUTTON TEXT:[{product_basket_button.text=}]")
    assert product_basket_button.text == "Товар в корзине", "Текст на кнопке добавления в корзину не соответствует 'Товар в корзине', вероятно товар не добавлен в корзину."

    # откроем страницу корзины напрямую.
    browser.get('https://hoff.ru/basket/')
    

    phone_number_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-input__field')))
    input_value = phone_number_input.get_attribute("value")
    print(f"{input_value=}")
    # присутствует пустое поле для ввода телефона?
    assert input_value == '', "Поле для ввода телефона не пустое!"

    #basket-auth__button
    # TODO: Вынести локаторы в отдельный файл с константами и отрефакторить!
    # присутствует кнопка «Войти»?
    basket_auth_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'basket-auth__button')))
    basket_auth_button_text = basket_auth_button.text
    assert basket_auth_button_text.strip() == "Войти", "Отсутствует кнопка 'Войти'!" 

    # Теперь извлечём из DOM суммарную стоимость товаров в корзине и сравним с ценой выбранного стола.
    basket_title = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'basket__title')))
    basket_title_text = basket_title.text
    print(f'{basket_title_text=}')
    num_added_goods = int(basket_title_text.split(" ")[0])
    print(f"{num_added_goods=}")
    assert num_added_goods == 1, "В списке товаров в корзине не один товар!" # в списке товаров 1 единственный добавленный товар

    # В поле Итого стоимость самого товара ?
    basket_summary_total_price = browser.find_element(By.CLASS_NAME, "basket-summary__total-price")
    total_price_span = basket_summary_total_price.find_element(By.TAG_NAME, "span")
    total_price = int(total_price_span.text.replace(" ",""))
    print(f"{total_price=}")
    assert total_price == price_actual, "Число в поле Итого не соответствует стоимости товара! "
    
    print("Тест успешен, задание выполнени!")

if __name__ == "__main__":
    test_hoff_ru()
