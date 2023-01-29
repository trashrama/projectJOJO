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
        'xpath', "//h2[@class='pi-item pi-item-spacing pi-title']").text
    # adiciona o nome do usuario
    div_stand_master = navegador.find_elements(
        'xpath', '//div[@data-source="user"]')[0].text
    div_stand_master = div_stand_master.split("\n")
    stand_master = div_stand_master[1]

    print(navegador.find_element(
        'xpath', "//td[@data-source='destpower']").get_attribute("innerHTML"))

    lista_hab = [navegador.find_element(
        'xpath', "//td[@data-source='destpower']").get_attribute("innerHTML"), navegador.find_element(
        'xpath', "//td[@data-source='speed']").get_attribute("innerHTML"), navegador.find_element(
        'xpath', "//td[@data-source='range']").get_attribute("innerHTML"),
        navegador.find_element(
        'xpath', "//td[@data-source='stamina']").get_attribute("innerHTML"), navegador.find_element(
        'xpath', "//td[@data-source='precision']").get_attribute("innerHTML"), navegador.find_element(
        'xpath', "//td[@data-source='potential']").get_attribute("innerHTML")]

    stand_info.append(name_stand)
    stand_info.append(PARTE)
    stand_info.append(stand_master)
    stand_info.extend(lista_hab)
    STANDS_DB.append(stand_info)


navegador = webdriver.Chrome(executable_path=r'chromedriver')

navegador.get("https://jojowiki.com/List_of_Stands")


indice_artigos = 1
while True:

    pagina = WebDriverWait(navegador, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="tabber-7b41f183054568e35f06bd9e4c65aa1d"]/div[1]/div[1]/div/div[2]/div[{}]/div[2]/a'.format(indice_artigos))))

    pagina.click()
    get_info(navegador, STANDS_DB, JOJO_PARTS[0])
    print(STANDS_DB)
    navegador.back()

    indice_artigos = indice_artigos + 1
