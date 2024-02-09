import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def pytest_addoption(parser):
    parser.addoption('--browser_name', 
                    action='store',
                    default='chrome',
                    help="Choose browser: chrome or firefox")

@pytest.fixture(scope='function')
def browser(request):


    browser_name = request.config.getoption("browser_name")
    browser = None
    if browser_name == "chrome":
        driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
        service = Service(executable_path=driver_path)
        options = Options()
        print("Starting Chrome...")
        browser = webdriver.Chrome()
    elif browser_name == "firefox":
        print("Starting Firefox...")
        browser = webdriver.Firefox()
    else:
        raise pytest.UsageError("--browser_name should be 'chrome' or 'firefox'")
    browser = webdriver.Chrome(service=service, options=options)
    yield browser
    print("Closing browser...")
    browser.quit()