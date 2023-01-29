from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# pip3 install selenium

# lista global com todos os stands
STANDS_DB = []
JOJO_PARTS = [i for i in range(3, 9)]


def verify_repeated(stand_name, part):
    if len(STANDS_DB) > 0:
        for stand in STANDS_DB:
            if stand[0] == stand_name and stand[1] == part:
                return True
            else:
                return False


def get_info(navegador, STANDS_DB, part):

    try:
        # adiciona o nome do stand na lista
        stand_name = navegador.find_element(
            'xpath', '//h2[@class="pi-item pi-item-spacing pi-title"]').text

        # verificar se tem stands repetidos como o Star Platinum na parte 3, 4 e 6
        isRepeated = verify_repeated(stand_name, part)

        if not (isRepeated):
            # adiciona o nome do usuario
            div_stand_master = navegador.find_elements(
                'xpath', '//div[@data-source="user"]')[0].text
            div_stand_master = div_stand_master.split("\n")
            stand_master = div_stand_master[1]

            try:
                destpower = navegador.find_element(
                    'xpath', "//td[@data-source='destpower']").get_attribute("innerHTML")
            except:
                destpower = "NULL"
            try:
                speed = navegador.find_element(
                    'xpath', "//td[@data-source='speed']").get_attribute("innerHTML")
            except:
                speed = "NULL"
            try:
                range_stand = navegador.find_element(
                    'xpath', "//td[@data-source='range']").get_attribute("innerHTML")
            except:
                range_stand = "NULL"
            try:
                stamina = navegador.find_element(
                    'xpath', "//td[@data-source='stamina']").get_attribute("innerHTML")
            except:
                stamina = "NULL"
            try:
                precision = navegador.find_element(
                    'xpath', "//td[@data-source='precision']").get_attribute("innerHTML")
            except:
                precision = "NULL"
            try:
                potential = navegador.find_element(
                    'xpath', "//td[@data-source='potential']").get_attribute("innerHTML")
            except:
                potential = "NULL"

            stand_info = [stand_name, part, stand_master, destpower, speed, range_stand,
                          stamina, precision, potential]
            print(stand_info)
            STANDS_DB.append(stand_info)
    except:
        pass


def write_file(file_name):
    with open(file_name, 'w') as file:
        for stand in STANDS_DB:
            file.write("({}, {}, {}, {}, {}, {}, {}, {}, {})\n".format(stand[0], stand[1], stand[2],
                                                                       stand[3], stand[4], stand[5], stand[6], stand[7], stand[8]))


navegador = webdriver.Chrome(executable_path=r'chromedriver')

print("TABELA DE DEBUG\n[1.0] Entrar na Página")
navegador.get("https://jojowiki.com/List_of_Stands")
print("REALIZADO")

for i in range(1, 100):
    lista_paginas = WebDriverWait(navegador, 5).until(EC.element_to_be_clickable(
        (By.XPATH, "(//div[@class='charname'])[{}]".format(i))))

    nome_pagina = navegador.find_element(
        By.CLASS_NAME, "tabberactive")

    print(nome_pagina.text)

    lista_paginas.click()

    if (i > 0 and i <= 36):
        jojo_part = JOJO_PARTS[0]
    # elif (i > 36 and i)

    get_info(navegador, STANDS_DB, jojo_part)
    navegador.back()

write_file("stands.txt")
