from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
# pip3 install selenium

# lista global com todos os stands
STANDS_DB = []


def verify_repeated(part):
    try:
        tabbernav = navegador.find_element('xpath', '//*[@id="tabber-d7ebef15c1a2568511617c1c4b543b17"]/ul' )
        aba_atual = tabbernav.find_elements(By.TAG_NAME, 'li')

        for i in range(len(aba_atual)):
            part_aba_atual = aba_atual[i].text
            part_aba_atual = int(part_aba_atual[-1])

            print(part_aba_atual)
            if part_aba_atual == part:
                aba_atual[i].click()
                wait()
                return True
    except:
        return False

def treatment_char(stat):

    stat = grab_initial_letter(stat)
    
    if stat == '∞':
        return 'I'
    elif stat == 'N':
        return 'NULL'
    elif stat == '<' or stat == '?' or stat == 'U':
        return 'UNKNOWN'
    else:
        return stat.upper()
#alguns status bugam e pegam alguns códigos HTML além deles próprios, então é necessária uma função para corrigir isso.
def grab_initial_letter(stat):
    return stat[0]
def get_info(navegador, STANDS_DB, part):

    try:
        # adiciona o nome do stand na lista
        stand_name = navegador.find_element(
            'xpath', '//h2[@class="pi-item pi-item-spacing pi-title"]').text

        # verificar se tem stands repetidos como o Star Platinum na parte 3, 4 e 6
        isRepeated = verify_repeated(part)

       
        # adiciona o nome do usuario
        div_stand_master = navegador.find_elements(
            'xpath', '//div[@data-source="user"]')[0].text
        div_stand_master = div_stand_master.split("\n")
        stand_master = div_stand_master[1]

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

        if isRepeated:
            for stand in STANDS_DB:
                if (stand[3] == destpower and stand[4] == speed and stand[5] == range_stand and stand[6] == stamina and stand[7] == precision):
                    return 0
            navegador.back()

        STANDS_DB.append(stand_info)

    except:
        pass
def write_file(file_name):
    with open(file_name, 'w') as file:
        for stand in STANDS_DB:
            file.writelines("({}, {}, {}, {}, {}, {}, {}, {}, {})\n".format(stand[0], stand[1], stand[2],
                                                                       stand[3], stand[4], stand[5], stand[6], stand[7], stand[8]))
def wait():
    sleep(10)


navegador = webdriver.Chrome(executable_path=r'chromedriver')
navegador.maximize_window()

print("TABELA DE DEBUG\n[1.0] Entrar na Página")
navegador.get("https://jojowiki.com/List_of_Stands")

# ---- descobrir quantos elementos tem na pagina

# procurar o menu
menu = navegador.find_element(By.CLASS_NAME, "tabbernav")
# pegar somente os elementos dentro do menu
el = menu.find_elements(By.TAG_NAME, 'li')

wait()

bloco = navegador.find_elements(By.CLASS_NAME, 'diamond2')
t = 0
num_art = bloco[t].find_elements(By.CLASS_NAME, 'charwhitelink')

for i in range(1, len(el)):
    part = i + 2
    for art in range(len(num_art)):
        #repetir o bloco porque a estrutura do DOM atualiza quando volta a pagina
        wait()

        bloco = navegador.find_elements(By.CLASS_NAME, 'diamond2')
        num_art = bloco[t].find_elements(By.CLASS_NAME, 'charwhitelink')

        element = WebDriverWait(navegador, 5).until(EC.element_to_be_clickable(num_art[art]))
        element.click()
        get_info(navegador, STANDS_DB, part)
        navegador.back()

        print(STANDS_DB)

    # atualizar o menu e os itens por conta do DOM
    menu = navegador.find_element(By.CLASS_NAME, "tabbernav")
    
    aba_atual = navegador.find_element(By.XPATH, '(//li)[{}]'.format(i+1))
    aba_atual.click()

    t = t + 1

#    wait()
    WebDriverWait(navegador, 3)
