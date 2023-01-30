import time
from selenium import webdriver
from selenium.webdriver.common.by import By

navegador = webdriver.Chrome(executable_path='chromedriver')

navegador.get('https://jojowiki.com/Star_Platinum#Part_3')
navegador.implicitly_wait(0.5)

tabbernav = navegador.find_element('xpath', '//*[@id="tabber-d7ebef15c1a2568511617c1c4b543b17"]/ul' )
aba_atual = tabbernav.find_elements(By.TAG_NAME, 'li')

part = 6

for i in range(len(aba_atual)):
    navegador.implicitly_wait(0.5)
    part_aba_atual = aba_atual[i].text
    part_aba_atual = int(part_aba_atual[-1])

    print(part_aba_atual)
    if part_aba_atual == part:
        aba_atual[i].click()
        print("clico..")
        time.sleep(10)


