import os
import json
import datetime
import requests
from bs4 import BeautifulSoup
from typing import List, NamedTuple, Tuple
import pandas as pd

# Define todas as informacoes contidas em uma reclamacao publicada no site Reclame Aqui
class Complain(NamedTuple):
  status: str
  date: str
  city: str
  state: str
  isResolved: str
  complain: str
  response: str
  evaluation: int
  evaluationText: str

# Define os parametros usados para realizar requisicoes sequencialmente
class IterationParams(NamedTuple):
  resultsPerRequest: int
  complains: List[Complain]
  currentIndex: int
  saveDelay: int

# Define os dados relativos a empresa
class Company(NamedTuple):
  headerName: str # Nome do arquivo json com as informacoes do header, obtido no site
  datasetName: str # Nome do arquivo csv para salvar as reclamacoes obtidas
  numberOfComplains: int # Numero total de reclamacoes da empresa cadastrada no site
  hash: str # Hash associado a empresa, obtido no site

# Factory da url de uma empresa
def makeUrl(company: Company, iteration: IterationParams) -> str:
  return f"https://consumidor.gov.br/pages/indicador/relatos/consultar?indicePrimeiroResultado={iteration.currentIndex}&palavrasChave=&segmentoMercado=&fornecedor={company.hash}&regiao=&area=&assunto=&problema=&dataInicio=&dataTermino=&avaliacao=&nota="

# Funcao para extrair as informacoes de uma lista de 10 divs obtidas com web scraping do site, retorna uma lista de Complain
def extractData(complainDivs):
  complains = []
  status = list(map(lambda x: str(x.find("h4", class_="relatos-status").text).strip(), complainDivs))
  meta = list(map(lambda x: str(x.find("span", class_="relatos-data").text).strip(), complainDivs))
  date = list(map(lambda x: x.split(", ")[0], meta))
  city = list(map(lambda x: x.split(", ")[1].split(" - ")[0], meta))
  state = list(map(lambda x: x.split(", ")[1].split(" - ")[1], meta))
  complain = list(map(lambda x: str(x.find_all("p")[0].text).strip(), complainDivs))
  response = list(map(lambda x: str(x.find_all("p")[1].text).strip(), complainDivs))
  evaluation = list(map(lambda x: str(x.find_all("p")[-2].text).strip(), complainDivs))
  evaluationText = list(map(lambda x: str(x.find_all("p")[-1].text).strip(), complainDivs))
  isResolved = list(map(lambda x: str(x.find("h4", class_="relatos-status").text), complainDivs))

  for i in range(len(evaluation)):
    complains.append(
      Complain(
        status=status[i], 
        date=date[i], 
        city=city[i], 
        state=state[i], 
        complain=" ".join(complain[i].splitlines()), 
        response=" ".join(response[i].splitlines()), 
        evaluation=evaluation[i], 
        evaluationText=" ".join(evaluationText[i].splitlines()),
        isResolved=" ".join(isResolved[i].split()),
      )
    )
  return complains

# Factory que retorna uma tupla com os valores para iniciar as requiscoes
def getInitialParams() -> Tuple[Company, IterationParams]:

  # Le o arquivo header, recebe do stdin o hash da empresa, o numero de reclamacoes total da empresa e o csv de output
  def getInitialInfo() -> Company:
    headerName = str(input("Arquivo header: "))
    hash = str(input("Hash da empresa: "))
    numberOfComplains = int(input("Numero de reclamacoes da empresa: "))
    datasetName = str(input("Arquivo csv: "))

    return Company(headerName, datasetName, numberOfComplains, hash)

  # 10 divs por requisicao(default do reclame aqui), lista de complains vazia, indice inicial 0 e atualiza o csv a cada 1000 reclamacoes obtidas
  def getInitialIteration() -> IterationParams:
    return IterationParams(10, [], 0, 1000)

  return getInitialInfo(), getInitialIteration()

# Espera a atualizacao do arquivo header.json e le do stdin o novo hash da empresa. Esses parametros mudam de tempo em tempo
def updateChangableInfo(data: Company) -> Company:
  while input("Renove o header e digite ok para continuar: ") != "ok":
    pass

  hash = str(input("Hash da empresa: "))

  return Company(data.headerName, data.datasetName, data.numberOfComplains, hash)

def getHeader(data: Company):
  return json.loads(open(data.headerName, "r").read())

# Incrementa current index pelo valor de results per request
def updateCurrentIndex(iteration: IterationParams):
  return IterationParams(iteration.resultsPerRequest, iteration.complains, iteration.currentIndex + iteration.resultsPerRequest, iteration.saveDelay)



# Inicio do script
os.system('cls||clear')
print("Iniciando script")
company, iteration = getInitialParams()

while iteration.currentIndex < company.numberOfComplains:
  try:
    response = requests.post(makeUrl(company, iteration), headers=getHeader(company))

    # Se a requisicao nao foi bem sucedida, renova os parametros que mudam
    # Pode ser necessario tratar outros erros que gerem status diferente de 200, ou tratar os erros a partir dos status
    if response.status_code != 200:
      print("Renovando parametros")
      company = updateChangableInfo(company)
      continue
    
    # Transforma o html em um objeto python, extrai as divs e extrai as informacoes das divs
    html = BeautifulSoup(response.text, "html.parser")
    complainDivs = html.find_all("div", class_="cartao-relato")
    totalResults = len(complainDivs)

    currentComplains = extractData(complainDivs)
    iteration.complains.extend(currentComplains)
    iteration = updateCurrentIndex(iteration)
    now = datetime.datetime.now()

    # Print para indicar andamento do script - % de reclamacoes extraidas - hora e minuto atual
    print(f"{100*(iteration.currentIndex/company.numberOfComplains):.2f}% - {now.hour:02d}:{now.minute:02d}")
    
    # Salva os dados a cada <saveDelay> reclamacoes tratadas
    if len(iteration.complains) % iteration.saveDelay == 0:
      pd.DataFrame(iteration.complains, columns=Complain._fields).to_csv(company.datasetName, index=False)

  # Em caso de erro nao tratado, printa o erro e salva todos os dados obtidos ate o momento
  except Exception as e:
    print(e)
    pd.DataFrame(iteration.complains, columns=Complain._fields).to_csv(company.datasetName, index=False)
