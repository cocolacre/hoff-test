# hoff-test
test task for Hoff

Перейти на страницу каталога https://hoff.ru/catalog/ofis/domashniy_ofis/komputernye_stoly/, выбрать и перейти к любому доступному товару. На открывшейся странице товара проверить, что присутствует кнопка добавления в корзину, кнопка активна и тест соответсвует «Добавить в корзину». Добавить товар в корзину и перейти на страницу корзины. На открывшейся странице проверить, что присутствует пустое поле для ввода телефона с кнопкой «Войти» и в списке товаров 1 единственный добавленный товар. В поле Итого стоимость самого товара.

Что бы установить allure на Windows 10, можно использовать scoop.

Команды для установки scoop через Powershell (права администратора не нужны): 
    
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


Команда для установки allure:

    scoop install allure

Проверено на Windows 10, Python 3.10.9

Тест можно запустить просто командой pytest.