import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By #'CLASS_NAME', 'CSS_SELECTOR', 'ID', 'LINK_TEXT', 'NAME', 'PARTIAL_LINK_TEXT', 'TAG_NAME', 'XPATH'
from selenium.webdriver.chrome.service import Service

driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
#profile_path = "C:\\Users\\79951\\AppData\\Local\\Google\\Chrome\\User Data" #
#profile_path = "C:\\Users\\cocolacre\\AppData\\Local\\Google\\Chrome\\User Data" #
service = Service(executable_path=driver_path)
options = Options()
#options.add_argument(f"user-data-dir={profile_path}")
browser = webdriver.Chrome(service=service, options=options)

browser.get('http://www.google.com/')

time.sleep(5) # Let the user actually see something!
find_methods = [x for x in dir(browser) if x.find("find") > -1]
print(find_methods)
try:
    search_box = browser.find_element(By.NAME, 'q')
    print(f"{search_box=}")
    search_box.send_keys('ChromeDriver')

    search_box.submit()

    time.sleep(5) # Let the user actually see something!

    browser.quit()
except Exception as _e:
    print(str(_e))

browser.quit()





"""

chromedriver_path = "D:\\chromedriver-win64\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver_path)  # Optional argument, if not specified will search path.

driver.get('http://www.google.com/')

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element_by_name('q')

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5) # Let the user actually see something!

driver.quit()
"""