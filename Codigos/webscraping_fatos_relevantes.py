from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    url = 'https://ri.celesc.com.br/comunicados-e-atas/aviso-aos-acionistas/'
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, 'tabela_1')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabela_1"]/tr[1]')))

    rows = driver.find_elements(By.XPATH, '//*[@id="tabela_1"]/tr')
    data_list = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if len(cols) >= 2:
            data = cols[0].text.strip()
            try:
                title_elem = cols[1].find_element(By.TAG_NAME, 'a')
                title = title_elem.text.strip()
                link = title_elem.get_attribute('href')
            except:
                title = 'Aviso aos Acionistas - Documento'
                link = ''

            data_list.append([data, title, link])

    with open('aviso_acionistas.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Data', 'Título', 'Link'])
        writer.writerows(data_list)

    print(f"✅ Extração concluída! {len(data_list)} registros salvos em aviso_acionistas.csv")

finally:
    driver.quit()
