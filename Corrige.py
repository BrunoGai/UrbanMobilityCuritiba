import json
from pathlib import Path

# Corrige os arquivos json da URBS
#------------------------------------------------------
def Corrige():
    # Path para arquivos .json
    path_Geral = 'D:/UTFPR/TCC 2 - Sérgio Moribe/Dados URBS/Geral/'
    path_Arquivos = 'D:/UTFPR/TCC 2 - Sérgio Moribe/Dados URBS/Veiculos/'
    # Carrega quais arquivos de posicionamento devem ser abertos 
    with open(path_Geral + 'Arquivos_Completo.json') as f:
        arquivos = json.load(f)
    # Converte os arquivos json em txt 
    for p in arquivos:
        arquivoJSON = (path_Arquivos + p['ARQUIVO']+'.json')
        arquivoTXT  = (path_Arquivos + p['ARQUIVO']+'.txt')     
        a = Path(arquivoJSON)
        a.rename(a.with_suffix('.txt'))
        # Altera os caracteres necessários     
        with open(arquivoTXT) as f:           
            texto = f.readlines()          
            for x in range (1,  len(texto)-1):
                texto[x] = texto[x].replace('}', '},')              
            texto[0] = texto[1].replace('{', '[{')
            texto[len(texto)-1] = texto[len(texto)-1].replace('}', '}]')       
        with open(arquivoTXT, 'w') as f:
            for linha in texto:
                f.write(linha)           
        # Converte os arquivos txt em .json
        a = Path(arquivoTXT)
        a.rename(a.with_suffix('.json'))   
        
# Execução do Programa
#------------------------------------------------------
Corrige()

