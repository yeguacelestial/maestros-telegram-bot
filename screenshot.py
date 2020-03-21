import time
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.headless = True

link = 'https://horarios.fime.me/dependencia/2316/periodo/3444993/materias/a/maestros/3'
link = 'https://horarios.fime.me/dependencia/2316/periodo/3444993/materias/a/maestros/162'

with webdriver.Firefox(options=options) as driver:
    driver.get(link)
    time.sleep(3)
    image = driver.find_element_by_id('listado').screenshot('listado.png')
    