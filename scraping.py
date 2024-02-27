import requests

cookies = {
  '_ga_VQRK96VHEX': 'GS1.3.1708991838.14.1.1708993414.0.0.0',
  '_ga': 'GA1.3.160338958.1707330398',
  '_gid': 'GA1.3.975575609.1708989704',
  'INGRESSCOOKIE': 'ee547cc59d9f68342a0bb8c65be4770b',
  'acoesSessaoCookie': 'A706CE6D909D75CA5BBB792278B7CCE6',
}

headers = {
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Accept': 'text/plain, */*; q=0.01',
  'Sec-Fetch-Site': 'same-origin',
  'Accept-Language': 'pt-BR,pt;q=0.9',
  'Sec-Fetch-Mode': 'cors',
  'Host': 'www.consumidor.gov.br',
  'Origin': 'https://www.consumidor.gov.br',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
  'Referer': 'https://www.consumidor.gov.br/pages/indicador/relatos/abrir',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'X-Requested-With': 'XMLHttpRequest',
}

data = {
  'indicePrimeiroResultado': '0',
  'palavrasChave': '',
  'segmentoMercado': '',
  'fornecedor': 'XJ0XIF4_dgSs3EdYMiBTuEk84etliElPUZxPYNIV9Ew',
  'regiao': '',
  'area': '',
  'assunto': '',
  'problema': '',
  'dataInicio': '01/01/2023',
  'dataTermino': '01/01/2024',
  'avaliacao': '',
  'nota': '',
}

response = requests.post(
  'https://www.consumidor.gov.br/pages/indicador/relatos/consultar',
  cookies=cookies,
  headers=headers,
  data=data,
)

print(response.text)

"""

acessar consumidor.gov > indicadores > relatos dos consumidores
abrir ferramentas de desenvolvedor > rede e limpar requisicoes
fazer pesquisa com fornecedor para obter o hash, pode usar data de inicio e termino como parametros para iteracao tambem
copiar requisicao como curl, instalar curl se nao tiver
transformar a requisicao copiada pro python - https://curlconverter.com/python/
copiar codigo em um arquivo python e executar, redirecionar output para um arquivo html - python3 arquivo.py > out.html
implementar iteracao com indicePrimeiroResultado e possivelmente dataInicio e dataTermino, tratar caso de mudanca nos headers e especialmente nos cookies

para ver o numero total de reclamacoes de uma empresa: consumidor.gov > indicadores > por empresa > pesquisar e clicar em todas

"""
