import json

# Extrai pontos de uma linha específica
# e armazena em um arquivo .json
#------------------------------------------------------
def PontosLinha():
  # Variáveis para armazenamento de strings
  PontosLinha = []
  # Path para arquivos .json
  path_Linhas = 'D:/UTFPR/TCC 2 - Sérgio Moribe/Dados URBS/Linhas/'
  # Variáveis da linha a ser localizada  
  #Linha = '924'
  #Linha = '303'
  Linha = '507'
  # Carrega arquivo com coordenadas dos pontos das linhas
  with open(path_Linhas + 'PontosLinha.json') as f:
    data = json.load(f)
  # Percorre os dados buscando as coordenadas dos 
  # pontos de uma linha específica
  for p in data:
    if p['COD'] == Linha:
        # Escreve o resultado em um array de strings
        PontosLinha.append({'NUM': p['NUM'],'NOME': p['NOME'],
                            'LAT': p['LAT'],'LON': p['LON'],
                            'SENTIDO': p['SENTIDO']})         
  # Transfere resultados para arquivos .json
  NomeArquivo = 'PontosLinha' + Linha + '.json'
  with open(path_Linhas + NomeArquivo, 'w') as outfile:
    json.dump(PontosLinha, outfile, indent=0)

# Execução do Programa
#------------------------------------------------------
PontosLinha()

