import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

def capture(link):
    with webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options) as driver:
        driver.get(link)
        time.sleep(3)
        image = driver.find_element_by_id('listado').screenshot('listado.png')
