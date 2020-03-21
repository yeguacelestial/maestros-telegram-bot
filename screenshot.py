import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True

def capture(link):
    with webdriver.Chrome(options=options) as driver:
        driver.get(link)
        time.sleep(3)
        image = driver.find_element_by_id('listado').screenshot('listado.png')
