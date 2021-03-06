import time, os
from selenium import webdriver
from dotenv import load_dotenv


def capture(link):

    load_dotenv()
    GOOGLE_CHROME_BIN = os.getenv('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

    options = webdriver.ChromeOptions()
    options.headless = True
    options.binary_location = GOOGLE_CHROME_BIN
    #options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    #options.add_argument("--window-size=1280,1696")
    options.add_argument("--window-size=1920,1080")

    with webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options) as driver:
        driver.get(link)
        time.sleep(1)
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width+74, required_height)

        element = driver.find_element_by_id('listado')
        element_png = element.screenshot_as_png
        with open("listado.png", "wb") as file:
            file.write(element_png)
        #image = driver.find_element_by_id('listado').screenshot('listado.png')
