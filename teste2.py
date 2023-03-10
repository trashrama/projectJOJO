from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
# pip3 install selenium

# lista global com todos os stands
STANDS_DB = []


def verify_repeated(stand_name, part):
    if len(STANDS_DB) > 0:
        for stand in STANDS_DB:
            if stand[0] == stand_name and stand[1] != part and part < 7:
                return True
            else:
                return False


def treatment_char(stat):

    lista_atrib = ['A', 'B', 'C', 'D', 'E', 'NULL']
    stat = grab_initial_letter(stat)

    if (stat.upper() in lista_atrib):
        return stat.upper()
    elif stat == '∞':
        return 'INFINITE'
    elif stat == 'N' or stat == 'Ø':
        return 'NULL'
    elif stat == '<' or stat == '?':
        return 'UNKNOWN'
    else:
        return stat.upper()
#alguns status bugam e pegam alguns códigos HTML além deles próprios, então é necessária uma função para corrigir isso.
def grab_initial_letter(stat):
    return stat[0]
def get_info(navegador, STANDS_DB, stand_name, stand_master, part):

    try:
        WebDriverWait(navegador, 100).until(EC.presence_of_element_located(
            (By.XPATH, "//td[@data-source='destpower']")))
        # adiciona o nome do stand na lista

        try:
            destpower = navegador.find_element(
                'xpath', "//td[@data-source='destpower']").get_attribute("innerHTML")
        except:
            destpower = "UNKNOWN"
        try:
            speed = navegador.find_element(
                'xpath', "//td[@data-source='speed']").get_attribute("innerHTML")
        except:
            speed = "UNKNOWN"
        try:
            range_stand = navegador.find_element(
                'xpath', "//td[@data-source='range']").get_attribute("innerHTML")
        except:
            range_stand = "UNKNOWN"
        try:
            stamina = navegador.find_element(
                'xpath', "//td[@data-source='stamina']").get_attribute("innerHTML")
        except:
            stamina = "UNKNOWN"
        try:
            precision = navegador.find_element(
                'xpath', "//td[@data-source='precision']").get_attribute("innerHTML")
        except:
            precision = "UNKNOWN"
        try:
            potential = navegador.find_element(
                'xpath', "//td[@data-source='potential']").get_attribute("innerHTML")
        except:
            potential = "UNKNOWN"
        
        destpower = treatment_char(destpower)
        speed = treatment_char(speed)
        range_stand = treatment_char(range_stand)
        potential = treatment_char(potential)
        precision = treatment_char(precision)
        destpower = treatment_char(destpower)
        
        stand_info = [stand_name, part, stand_master, destpower, speed, range_stand,
                        stamina, precision, potential]
        if stand_info not in STANDS_DB:
            STANDS_DB.append(stand_info)
        else:
            print("sem pagina")
    except:
        return True
def write_file(file_name):
    with open(file_name, 'w') as file:
        for stand in STANDS_DB:
            file.writelines("({}, {}, {}, {}, {}, {}, {}, {}, {})\n".format(stand[0], stand[1], stand[2],
                                                                       stand[3], stand[4], stand[5], stand[6], stand[7], stand[8]))
def wait():
    sleep(5)


navegador = webdriver.Chrome(executable_path=r'chromedriver')
navegador.maximize_window()

print("TABELA DE DEBUG\n[1.0] Entrar na Página")
navegador.get("https://jojowiki.com/List_of_Stands")

# ---- descobrir quantos elementos tem na pagina

# procurar o menu
WebDriverWait(navegador, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'tabbernav')))
menu = navegador.find_element(By.CLASS_NAME, "tabbernav")
# pegar somente os elementos dentro do menu
el = menu.find_elements(By.TAG_NAME, 'li')

wait()

bloco = navegador.find_elements(By.CLASS_NAME, 'diamond2')
t = 1
art = bloco[t].find_elements(By.CLASS_NAME, 'charwhitelink')

nav_voltou = False

for i in range(2, len(el)):
    WebDriverWait(navegador, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'tabbernav')))
    menu = navegador.find_element(By.CLASS_NAME, "tabbernav")
    
    aba_atual = navegador.find_element(By.XPATH, '(//li)[{}]'.format(i))
    aba_atual.click()
    part = i + 2
    for num_art in range(len(art)):
        #repetir o bloco porque a estrutura do DOM atualiza quando volta a pagina

        if nav_voltou == True:
            WebDriverWait(navegador, 190).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'diamond2')))
            bloco = navegador.find_elements(By.CLASS_NAME, 'diamond2')
            art = bloco[t].find_elements(By.CLASS_NAME, 'charwhitelink')

        #verifica assim que achar o nome do artigo se é repetido
        isRepeated = verify_repeated(art[num_art].text, part)
        if not isRepeated:
            nome_usuario = bloco[t].find_elements(By.CLASS_NAME, 'charstand')
            nome_usuario = nome_usuario[num_art].text
            nome_stand = art[num_art].text
            element = WebDriverWait(navegador, 100).until(EC.element_to_be_clickable(art[num_art]))
            element.click()
            sem_pagina = get_info(navegador, STANDS_DB, nome_stand, nome_usuario, part)
            navegador.back()
            nav_voltou = True
        print(STANDS_DB)

    # atualizar o menu e os itens por conta do DOM
    WebDriverWait(navegador, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'tabbernav')))
    menu = navegador.find_element(By.CLASS_NAME, "tabbernav")
    
    aba_atual = navegador.find_element(By.XPATH, '(//li)[{}]'.format(i+1))
    aba_atual.click()

    t = t + 1

#    wait()
    WebDriverWait(navegador, 3)
