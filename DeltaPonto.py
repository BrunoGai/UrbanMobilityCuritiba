import json, csv, Haversine, Thread_
from datetime import datetime

# Variáveis do ponto a ser localizado
#------------------------------------------------------
raio    = 50
#margem  = 450
#margem  = 300
margem  = 350
acerto  = 60
#------------------------------------
#Linha   = '924'
#NomePonto = 'Terminal Santa Felicidade'
#Ponto   = '106018'

#NomePonto = 'Terminal Santa Candida'
#Ponto   = '105905'
#------------------------------------
#Linha   = '303'
#NomePonto = 'Terminal Centenario'
#Ponto   = '105101'

#NomePonto = 'Terminal Campo Comprido'
#Ponto   = '104601'
#------------------------------------
Linha   = '507'
#NomePonto = 'Terminal Boqueirao'
#Ponto   = '109102'

#NomePonto = 'Terminal Sitio Cercado'
#Ponto   = '109113'

#NomePonto = 'Terminal Pinheirinho'
#Ponto   = '105707'

NomePonto = 'Terminal Guadalupe'
Ponto   = '109027'
#------------------------------------

# Variáveis para armazenamento de strings
dados1 = []
# Path para arquivos .json
path_Geral = 'D:/UTFPR/TCC 2 - Sérgio Moribe/Dados URBS/Geral/'
path_Arquivos = 'D:/UTFPR/TCC 2 - Sérgio Moribe/Dados URBS/Veiculos/'
path_Linhas = 'D:/UTFPR/TCC 2 - Sérgio Moribe/Dados URBS/Linhas/'

# Calcula a variação por horaria de ocorrencias por ponto
#------------------------------------------------------
def Calculo(dados, margem, acerto, path):
    # Variáveis
    dados1  = [['hora', 'valPos', 'qntPos', 'valorNeg', 'qntNeg', 'qntOk', 'total']]
    valorPos = 0
    valorNeg = 0
    qntPos = 0
    qntNeg = 0
    qntOk = 0
    difFinal = 0
    grupoDif = []
    dataProx = '01/11/2018'
    # Abre arquivo de horarios
    with open(path) as i:
        horarios = json.load(i) 
    # Percorre list de horários 
    for q in horarios: 
        # Percorre ocorrencias   
        for i,m in enumerate(dados): 
            # Armazena data e hora da tabela de horarios
            horaHorar = datetime.strptime(q['HORA'], '%H:%M')  
            data,hora = m['DTHR'].split(' ')
            # Armazena data e hora da ocorrencia    
            horaOcorr = datetime.strptime(hora, '%H:%M:%S') 
            # Calcula a diferenca entre o previsto e o analisado        
            dif = (horaOcorr-horaHorar).total_seconds() 
            # Armazena data e hora da próxima ocorrencia
            if (i < len(dados)-1):
                dataProx,horaProx = dados[i + 1]['DTHR'].split(' ')
            # Se a diferença estiver dentro da margem, armazena valor 
            if (dif <= margem and dif >= (margem*(-1))):
                grupoDif.append(dif)        
            # Se a data da proxima ocorrencia for diferente, 
            # calcula menor valor 
            if (data != dataProx):  
                if len(grupoDif) != 0:
                    difFinal = min(grupoDif, key=lambda x:abs(int(x)-0))
                # Se a diferença estiver dentro da margem de acerto, 
                # armazena valor 
                if (difFinal <= acerto and difFinal >= (acerto*(-1)) and difFinal != 0):
                    qntOk = qntOk + 1
                # Se a diferença não estiver dentro da margem de acerto, 
                # armazena valor positivo ou negativo              
                else:
                    if (difFinal > 0):
                        valorPos = valorPos + difFinal
                        qntPos = qntPos + 1
                    if (difFinal < 0):
                        valorNeg = valorNeg + difFinal
                        qntNeg = qntNeg + 1
                grupoDif = []   
        # Armazena resultado em um list         
        dados1.append([q['HORA'], int(round(valorPos)), 
                          qntPos, int(round(valorNeg)), 
                          qntNeg, qntOk])
        # Reseta variaveis
        valorPos = 0
        valorNeg = 0
        qntPos = 0
        qntNeg = 0
        qntOk  = 0   
        grupoDif = []
    return (dados1)

# Rotina assíncrona para varredura de arquivos
#------------------------------------------------------
def thread_DeltaPonto(arquivo, datas, Coord_1):
    # Abre arquivo e percorre dados
    with open(arquivo) as g:
        dados = json.load(g)
    for q in dados:              
        # Se for identificado o código da linha declarado
        if q['COD_LINHA'] == Linha:                   
            # Verifica se as datas são válidas (dia útil)
            for r in datas:
                Data,Hora = q['DTHR'].split(' ')
                if (r['DIA'] == Data and 
                    r['SEMANA'] != 'SABADO' and 
                    r['SEMANA'] != 'DOMINGO' and 
                    r['OBS'] != 'FERIADO'):                          
                    # Calcula a distancia das coordenadas
                    Coord_2 = (float(q['LAT']),float(q['LON']))
                    dist = Haversine.Distancia(Coord_1, Coord_2)
                    # Se a coordenada estiver dentro do raio indicado
                    if (dist < raio):
                        # Faz um print para acompanhamento de progresso
                        print(Data, Hora)
                        # Escreve o resultado em um array de strings   
                        dados1.append({'DTHR': q['DTHR'],
                                       'VEIC': q['VEIC']})

# Verifica a variação das ocorrencias de um veículo
# em relação ao horário previsto
#------------------------------------------------------
def DeltaPonto(): 
    # Definição de coordenadas do ponto a ser analisado
    with open(path_Linhas + 'PontosLinha.json') as k:
        pontos = json.load(k)
    for m in pontos:
        if (m['NUM'] == Ponto and m['COD'] == Linha):
            Coord_1 = (float(m['LAT']),float(m['LON']))
    # Carrega os arquivos com as datas a serem analisadas
    with open(path_Geral + 'Datas_Bimestre.json') as h:
        datas = json.load(h)
    # Carrega quais arquivos de posicionamento devem ser abertos 
    with open(path_Geral + 'Arquivos_Bimestre.json') as f:
        arquivos = json.load(f)
    # Armazena o número de threads utilizadas
    pool = Thread_.ThreadPool(10)
    # Carrega os arquivos de posicionamento e os percorre
    for p in arquivos:
        NomeArquivo = (path_Arquivos + p['ARQUIVO'] +'.json')
        # Chama um o número configurado de threads 
        pool.add_task(thread_DeltaPonto(NomeArquivo, datas, Coord_1))
    pool.wait_completion() 
    # Ordena ocorrencias
    dados2 = sorted(dados1, key=lambda x: datetime.strptime(x['DTHR'], '%d/%m/%Y %H:%M:%S'))
    # Calcula variação em relação ao previsto
    NomeArquivo = path_Linhas + 'Tabela_' + Linha + '_' + Ponto + '.json'
    dados3 = Calculo(dados2,margem,acerto,NomeArquivo)
    # Transfere resultados para arquivos .csv
    NomeArquivo = path_Geral + Linha + '_' + Ponto + '_' + NomePonto + '.csv'
    with open (NomeArquivo, 'w') as arquivoCSV:
        writer = csv.writer(arquivoCSV, lineterminator='\n', dialect='excel')
        writer.writerows(dados3)
    arquivoCSV.close()

# Execução do Programa
#------------------------------------------------------
DeltaPonto()
