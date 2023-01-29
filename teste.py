from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

# pip3 install selenium

# lista global com todos os stands
STANDS_DB = []
JOJO_PARTS = [i for i in range(3, 9)]


def get_info(navegador, STANDS_DB, PARTE):
    stand_info = []

    # adiciona o nome do stand na lista
    name_stand = navegador.find_element(
        'xpath', "//h2[@class='pi-item pi-item-spacing pi-title']").text
    # adiciona o nome do usuario
    stand_master = navegador.find_elements(
        'xpath', '// div[@data-source="user"]')

    for stand in stand_master:
        if stand.text.casefold() != 'user':
            stand_master = stand


navegador = webdriver.Chrome(executable_path=r'chromedriver')

navegador.get("https://jojowiki.com/Magician%27s_Red")


get_info(navegador, STANDS_DB, JOJO_PARTS[0])
print(STANDS_DB)


# //*[@id="tabber-7b41f183054568e35f06bd9e4c65aa1d"]/div[1]/div[1]/div/div[2]/div[1]/div[2]/a/
