import json
import datetime
from datetime import *

# Verifica quais datas contém informações nos arquivos
# e atuzaliza o .json com o status
#------------------------------------------------------
def Verificacao():
    # Path para arquivos .json
    path_Geral = 'D:/Dados URBS/Geral/'
    path_Arquivos = 'D:/Dados URBS/Veiculos/'
    data1 = date(2017,1,1)
    # Carrega quais arquivos de posicionamento devem ser abertos 
    with open(path_Geral + 'Arquivos_Completo.json') as f:
        arquivos = json.load(f)
    # Carrega os arquivos com as datas a serem analisadas
    with open(path_Geral + 'Datas_Completo.json') as h:
        datas = json.load(h)
    # Carrega os arquivos de posicionamento e os percorre
    for p in arquivos:
        arquivo = (path_Arquivos + p['ARQUIVO']+'.json')  
        with open(arquivo) as g:
            dados = json.load(g)
            for q in dados:
                data,hora = q['DTHR'].split(' ')
                dia,mes,ano = data.split('/')
                data2 = date(int(ano),int(mes),int(dia))
                # Verifica se existem as datas nos arquivos de veículos              
                if (data2 > data1): 
                    data1 = data2                                   
                    # Escreve o resultado em um array de strings 
                    for h in datas:
                        if (h['DIA'] == data):
                            h['DADOS'] = '1'
    # Transfere resultados para arquivos .json
    with open(path_Geral + 'Datas_Completo.json', 'w+') as outfile:
        json.dump(datas, outfile, indent=0)

# Execução do Programa
#------------------------------------------------------                       
Verificacao()



