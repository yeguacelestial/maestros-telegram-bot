import time, os
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()
GOOGLE_CHROME_BIN = os.getenv('GOOGLE_CHROME_BIN')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

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
