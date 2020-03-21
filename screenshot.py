import time, os
from selenium import webdriver
from dotenv import load_dotenv


def capture(link):
    load_dotenv()
    FIREFOX_BIN = os.getenv('FIREFOX_BIN')
    GECKODRIVER_PATH = os.getenv('GECKODRIVER_PATH')
    LD_LIBRARY_PATH = os.getenv('LD_LIBRARY_PATH')
    PATH = os.getenv('PATH')

    options = webdriver.FirefoxOptions()
    options.headless = True
    options.binary_location = FIREFOX_BIN
    #options.add_argument('--disable-gpu')
    #options.add_argument('--no-sandbox')

    with webdriver.Firefox(executable_path=PATH, options=options) as driver:
        driver.get(link)
        time.sleep(3)
        image = driver.find_element_by_id('listado').screenshot('listado.png')