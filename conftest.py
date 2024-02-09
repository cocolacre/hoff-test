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
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        #options.add_argument(f'--user-agent="{user_agent}"')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        print("Starting Chrome...")
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        print("Starting Firefox...")
        browser = webdriver.Firefox()
    else:
        raise pytest.UsageError("--browser_name should be 'chrome' or 'firefox'")
    
    yield browser
    print("Closing browser...")
    browser.quit()