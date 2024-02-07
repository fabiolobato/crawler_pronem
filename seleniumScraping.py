import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

edge_driver_path = "driver/msedgedriver.exe"
options = Options()
options.add_argument('--headless')
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

# Finding total number of complains
driver.get("https://consumidor.gov.br/pages/indicador/empresa/abrir")
inputCompanyName = driver.find_element(By.XPATH, '//*[@id="autocomplete_priEmpresa"]')
inputCompanyName.send_keys("Vivo - Telefônica")

time.sleep(1)
inputCompanyName.send_keys(Keys.ARROW_DOWN)
inputCompanyName.send_keys(Keys.ENTER)

buttonAllComplains = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo-decorator"]/div/div[2]/div/div/div/div/div/ul/li[4]/a')))
buttonAllComplains.click()

time.sleep(5)

spanNumberOfComplains = driver.find_element(By.XPATH, '//*[@id="indicadorTotalReclamacao"]/span')
totalNumberOfComplains = int(spanNumberOfComplains.get_attribute("innerText"))
print(totalNumberOfComplains)
print(driver.current_url)

# Get all complains
driver.get("https://consumidor.gov.br/pages/indicador/relatos/abrir")
btnPesquisar = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="relatos-acoes"]/div/button')))
btnPesquisar.click()

formFornecedor = driver.find_element(By.XPATH, '//*[@id="fornecedor"]')
formFornecedor.send_keys("Vivo - Telefônica")

btnPesquisar = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-pesquisar"]')))
btnPesquisar.click()

resultsPerPage = 10
currentNumberOfResults = 0
os.system('cls||clear')

while currentNumberOfResults < totalNumberOfComplains:
  currentNumberOfResults = driver.find_element(By.XPATH, '//*[@id="contador"]')
  currentNumberOfResults = int(currentNumberOfResults.get_attribute("innerText").split(" ")[0])
  print(currentNumberOfResults, totalNumberOfComplains, f"{currentNumberOfResults/totalNumberOfComplains*100:.2f}%")
  btnNextPage = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-mais-resultados"]')))
  btnNextPage.click()

divComplains = driver.find_elements(By.XPATH, '//*[@id="resultados"]/div')
print(len(divComplains))
while input("q for quit: ") != 'q':
  pass