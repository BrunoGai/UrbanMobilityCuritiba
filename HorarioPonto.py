import json

# Extrai os horários de um ponto específico
# e armazena em um arquivo .json
#------------------------------------------------------
def HorarioPonto():
  # Variáveis para armazenamento de strings
  HorarioLinha = []
  # Path para arquivos .json
  path_Linhas = 'D:/Dados URBS/Linhas/'
  path_Geral = 'D:/Dados URBS/Geral/'
  # Variáveis do ponto a ser localizado
  Linha = '507'
  Ponto = '109027'
  NomePonto = 'Terminal Guadalupe'
  # Carrega arquivo com tabelas horárias das linhas
  with open(path_Linhas + 'TabelaLinha.json') as f:
    data = json.load(f)
  # Percorre o arquivos buscando os pontos de uma linha específica
  for p in data:
    if  (p['NUM'] == Ponto and p['COD'] == Linha):
  # Escreve o resultado em um array de strings
      HorarioLinha.append({'HORA': p['HORA']})         
  # Transfere resultados para arquivos .json
  NomeArquivo = 'HorarioLinha_' + Linha + '_' + Ponto + '_' + NomePonto + '.json'
  with open(path_Geral + NomeArquivo, 'w') as outfile:
    json.dump(HorarioLinha, outfile, indent=0)

# Execução do Programa
#------------------------------------------------------
HorarioPonto()
