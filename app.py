from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

# pip3 install selenium

# lista global com todos os stands
STANDS_DB = []
JOJO_PARTS = [i for i in range(3, 9)]


def close_cookie_ad(navegador):

    cookie_ad = WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[7]/div/div/div[2]/div[2]")))

    if (cookie_ad.is_displayed()):
        cookie_ad.click()


def get_info(navegador, STANDS_DB, PARTE):
    stand_info = []

    # adiciona o nome do stand na lista
    name_stand = navegador.find_element(
        'xpath', '//*[@id="mw-content-text"]/div[2]/aside/h2').text
    # adiciona o nome do usuario
    stand_master = navegador.find_element(
        'xpath', '//*[@id="mw-content-text"]/div[2]/aside/div[3]/div/a').text

    lista_hab = []
    # adiciona as habilidades
    for i in range(1, 3):
        for j in range(1, 4):
            hab = navegador.find_element(
                'xpath', '//*[@id="tabber-6ecfd84b5e9d4da5669c4a38e694027b"]/div[1]/aside/section[{}]/table/tbody/tr/td[{}]'.format(i, j)).get_attribute("innerHTML")
            lista_hab.append(hab)

    stand_info.append(name_stand)
    stand_info.append(PARTE)
    stand_info.append(stand_master)
    stand_info.extend(lista_hab)


navegador = webdriver.Chrome(executable_path=r'chromedriver')

navegador.get("https://jojowiki.com/Star_Platinum")

get_info(navegador, STANDS_DB, JOJO_PARTS[0])
# print(STANDS_DB)

# indice_artigos = 1
# while True:
#     WebDriverWait(navegador, 10)
#     pagina = navegador.find_element(
#         'xpath', '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[3]/th[{}]/i/a'.format(indice_artigos))
#     pagina.click()
#     navegador.back()
#     indice_artigos = indice_artigos + 1
