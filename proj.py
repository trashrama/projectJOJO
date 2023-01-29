from selenium import webdriver

# pip3 install selenium

# lista global com todos os stands
STANDS_DB = []


def get_info(navegador, STANDS_DB):
    stand_info = []

    # adiciona o nome do stand na lista
    stand_info.append(navegador.find_element(
        'xpath', '//*[@id="mw-content-text"]/div/aside/h2').get_attribute("innerHTML"))

    # adiciona o nome do usuario
    stand_info.append(navegador.find_element('xpath',
                                             '//*[@id="mw-content-text"]/div/aside/div[4]/div').get_attribute("innerHTML"))
    # adiciona as habilidades

    for i in range(1, 7):
        cont = navegador.find_element(
            'xpath', '//*[@id="mw-content-text"]/div/aside/section/div[{}]/div'.format(i)).get_attribute("innerHTML")

        if ("→" in cont):
            cont = cont[(cont.find("→"))+2]
        stand_info.append(cont)

    STANDS_DB.append(stand_info)


JOJO_PARTS = [i for i in range(3, 9)]
print(JOJO_PARTS)

navegador = webdriver.Chrome(executable_path=r'chromedriver')

navegador.get("https://jjba.fandom.com/pt-br/wiki/Star_Platinum")

get_info(navegador, STANDS_DB)

print(STANDS_DB)
