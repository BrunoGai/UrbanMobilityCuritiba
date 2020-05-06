from datetime import datetime
import math, json

# Ordena ocorrencias e elimina duplicatas
#------------------------------------------------------
def Ordenar_Limpar(dados):   
    # Variáveis 
    dados1 = []
    # Ordena os dados em ordem crescente 
    dados = sorted(dados, key=lambda x: datetime.strptime(x['DTHR'], '%d/%m/%Y %H:%M:%S')) 
    # Percorre dados gardando informações sobre a 
    # data do registro atual e o próximo
    for i,q in enumerate(dados): 
        data1 = datetime.strptime(q['DTHR'], '%d/%m/%Y %H:%M:%S')
        veic1 = q['VEIC']
        if (i < len(dados)-1):
            data2 = datetime.strptime(dados[i + 1]['DTHR'], '%d/%m/%Y %H:%M:%S')
            veic2 = dados[i + 1]['VEIC']
        dif = (data1 - data2).total_seconds()   
        # Se a distancia do ponto anterior ou o veiculo for diferente 
        # é adicionada a ocorrencia no list e atualiza variável de controle              
        if (dif > 900 or veic1 != veic2):
            dados1.append({'DTHR': data1.strftime('%d/%m/%Y %H:%M:%S'),'VEIC': veic1})
    return(dados1)

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
    veic = ''
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