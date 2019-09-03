#Avaliador de algoritmos de escalonamento de tarefas:
#   FCFS
#   RR
#   SJF
#   SRTF
#   PRIOc
#   PRIOp
#   PRIOd


def organiza_ordem_fila(indices, fila):
    for i in range(0,len(indices)):
        for j in range(0,len(indices)-1):
            if fila[indices[j]]>fila[indices[j+1]]:
                aux=indices[j]
                indices[j]=indices[j+1]
                indices[j+1]=aux
    return indices


#Função para calcular o FCFS
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def FCFS(N, instantes_ingresso, tempo_execucao):

    #iniciando as variaveis
    instantes_ingresso_auxiliar=sum(instantes_ingresso)
    N_auxiliar=N
    trocas_contexto=N-1
    inicio_execucao=[None]*N
    fim_execucao=[None]*N
    tempo_corrido=0
    
    #loop para contas
    while N!=0:
        index_proxima_tarefa=instantes_ingresso.index(min(instantes_ingresso))
        inicio_execucao[index_proxima_tarefa]=tempo_corrido
        fim_execucao[index_proxima_tarefa]=inicio_execucao[index_proxima_tarefa]+tempo_execucao[index_proxima_tarefa]
        tempo_corrido=fim_execucao[index_proxima_tarefa]
        N=N-1
        instantes_ingresso[index_proxima_tarefa]=max(instantes_ingresso)+1
    
    #contas para retirar as medias
    tempo_medio_execucao=(sum(fim_execucao)-instantes_ingresso_auxiliar)/N_auxiliar
    tempo_medio_espera=(sum(inicio_execucao)-instantes_ingresso_auxiliar)/N_auxiliar

    return [tempo_medio_execucao, tempo_medio_espera, trocas_contexto]


#Função para calcular o RR
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def RR(N, instantes_ingresso, tempo_execucao, tempo_quantum):

    #iniciando a fila
    ordem_fila=[]
    momento=0
    while momento in instantes_ingresso:
        ordem_fila.append(instantes_ingresso.index(momento))
        instantes_ingresso[instantes_ingresso.index(momento)]=-1

    #iniciando as variaveis
    troca_contexto=0
    tempo_rodando=[0]*N
    tempo_parado=[0]*N
    tempo_atual_quantum=tempo_quantum

    count_tarefas_feitas=0

    while ordem_fila!=[] and count_tarefas_feitas!=N:
        #adicionando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1
        tempo_atual_quantum-=1

        #arrumando a fila
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            count_tarefas_feitas+=1
            troca_contexto+=1
            tempo_atual_quantum=tempo_quantum
        elif tempo_atual_quantum==0:
            auxiliar=ordem_fila[0]
            ordem_fila.remove(ordem_fila[0])
            ordem_fila.append(auxiliar)
            troca_contexto+=1
            tempo_atual_quantum=tempo_quantum

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto-1]
      

#Função para calcular o SJF
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def SJF(N, instantes_ingresso, tempo_execucao):

    #arrumando a fila
    ordem_fila=[]
    momento=0
    while momento in instantes_ingresso:
        ordem_fila.append(instantes_ingresso.index(momento))
        instantes_ingresso[instantes_ingresso.index(momento)]=-1
    ordem_fila=organiza_ordem_fila(ordem_fila,tempo_execucao)

    #iniciando as variaveis
    troca_contexto=0
    tempo_rodando=[0]*N
    tempo_parado=[0]*N

    count_tarefas_feitas=0

    while ordem_fila!=[] and count_tarefas_feitas!=N:
        #arrumando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1

        #arrumando a fila
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            count_tarefas_feitas+=1
            troca_contexto+=1
            ordem_fila=organiza_ordem_fila(ordem_fila,tempo_execucao)

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto-1]


#Função para calcular o SRTF
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def SRTF(N, instantes_ingresso, tempo_execucao):

    #arrumando a fila
    ordem_fila=[]
    momento=0
    while momento in instantes_ingresso:
        ordem_fila.append(instantes_ingresso.index(momento))
        instantes_ingresso[instantes_ingresso.index(momento)]=-1
    ordem_fila=organiza_ordem_fila(ordem_fila,tempo_execucao)

    #iniciando as variaveis
    troca_contexto=0
    tempo_rodando=[0]*N
    tempo_parado=[0]*N

    count_tarefas_feitas=0

    while ordem_fila!=[] and count_tarefas_feitas!=N:
        #arrumando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1

        #arrumando a fila
        aux_ordem_fila=ordem_fila[0]
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            count_tarefas_feitas+=1

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1


        ordem_fila=organiza_ordem_fila(ordem_fila,tempo_execucao)

        if ordem_fila!=[] and aux_ordem_fila!=ordem_fila[0]:
            troca_contexto+=1

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto]


#Função para calcular o PRIOc
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#   ordem_prioridade: a prioridade das tarefas
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def PRIOC(N, instantes_ingresso, tempo_execucao, ordem_prioridade):

    #arrumando a fila
    ordem_fila=[]
    momento=0
    while momento in instantes_ingresso:
        ordem_fila.append(instantes_ingresso.index(momento))
        instantes_ingresso[instantes_ingresso.index(momento)]=-1
    ordem_fila=organiza_ordem_fila(ordem_fila,ordem_prioridade)
    ordem_fila.reverse()

    #iniciando as variaveis
    troca_contexto=0
    tempo_rodando=[0]*N
    tempo_parado=[0]*N

    count_tarefas_feitas=0

    while ordem_fila!=[] and count_tarefas_feitas!=N:
        #arrumando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1

        #arrumando a fila
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            count_tarefas_feitas+=1
            troca_contexto+=1
            ordem_fila=organiza_ordem_fila(ordem_fila,ordem_prioridade)
            ordem_fila.reverse()

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto-1]


#Função para calcular o PRIOp
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#   ordem_prioridade: a prioridade das tarefas
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def PRIOP(N, instantes_ingresso, tempo_execucao, ordem_prioridade):

    #arrumando a fila
    ordem_fila=[]
    momento=0
    while momento in instantes_ingresso:
        ordem_fila.append(instantes_ingresso.index(momento))
        instantes_ingresso[instantes_ingresso.index(momento)]=-1
    ordem_fila=organiza_ordem_fila(ordem_fila,ordem_prioridade)
    ordem_fila.reverse()

    #iniciando as variaveis
    troca_contexto=0
    tempo_rodando=[0]*N
    tempo_parado=[0]*N

    count_tarefas_feitas=0

    while ordem_fila!=[] and count_tarefas_feitas!=N:
        #arrumando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1

        #arrumando a fila
        aux_ordem_fila=ordem_fila[0]
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            count_tarefas_feitas+=1

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1

        #organizando fila
        ordem_fila=organiza_ordem_fila(ordem_fila,ordem_prioridade)
        ordem_fila.reverse()

        if ordem_fila!=[] and aux_ordem_fila!=ordem_fila[0]:
            troca_contexto+=1

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto]


#Função para calcular o PRIOd
#ENTRADA:
#   N: o número de tarefas
#   instantes_ingresso: os instantes de ingresso das tarefas
#   tempo_execucao: o tempo de execucao de cada tarefa
#   ordem_prioridade: a prioridade das tarefas
#SAIDA:
#   lista com respecitvamente, o tempo medio de execucao de cada tarefa, tempo medio de espera de cada tarefa e numero de trocas de contexto que ocorreram
def PRIOD(N, instantes_ingresso, tempo_execucao, ordem_prioridade):

    prioridade_dinamica=[0]*N

    #arrumando a fila
    ordem_fila=[]
    momento=0
    while momento in instantes_ingresso:
        ordem_fila.append(instantes_ingresso.index(momento))
        instantes_ingresso[instantes_ingresso.index(momento)]=-1

    for i in ordem_fila:
        prioridade_dinamica[i]=-ordem_prioridade[i]
    ordem_fila=organiza_ordem_fila(ordem_fila,prioridade_dinamica)

    #organizando ordem dinamica
    for i in ordem_fila:
        if i!=ordem_fila[0]:
            prioridade_dinamica[i]-=1

    #iniciando as variaveis
    troca_contexto=0
    tempo_rodando=[0]*N
    tempo_parado=[0]*N

    count_tarefas_feitas=0

    while ordem_fila!=[] and count_tarefas_feitas!=N:
        #arrumando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1

        #arrumando a fila
        aux_ordem_fila=ordem_fila[0]
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            count_tarefas_feitas+=1

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1

        for i in ordem_fila:
            if prioridade_dinamica[i]==0:
                prioridade_dinamica[i]=-ordem_prioridade[i]

        #organizando fila
        ordem_fila=organiza_ordem_fila(ordem_fila,prioridade_dinamica)

        if ordem_fila!=[] and aux_ordem_fila!=ordem_fila[0]:
            troca_contexto+=1
            for i in ordem_fila:
                if i!=ordem_fila[0]:
                    prioridade_dinamica[i]-=1
                if i==ordem_fila[0]:
                    prioridade_dinamica[i]=-ordem_prioridade[i]

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto-1]


entrada_funcoes=[None]*4
f=open('in.txt', 'r')
in_lines=f.readlines()
j=0
for i in in_lines:
    entrada_funcoes[j]=i
    j+=1

f.close()

for i in range(0,4):
    entrada_funcoes[i]=entrada_funcoes[i].replace('\n','')

#pegando N
N_fixo=int(entrada_funcoes[0])

instantes_ingresso_fixo=entrada_funcoes[1].split(',')
tempo_execucao_fixo=entrada_funcoes[2].split(',')
prioridade_fixo=entrada_funcoes[3].split(',')

for i in range(0,N_fixo):
    instantes_ingresso_fixo[i]=int(instantes_ingresso_fixo[i])
    tempo_execucao_fixo[i]=int(tempo_execucao_fixo[i])
    prioridade_fixo[i]=int(prioridade_fixo[i])
    
N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_FCFS=FCFS(N,instantes_ingresso,tempo_execucao)

N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_RR=RR(N,instantes_ingresso,tempo_execucao,2)

N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_SJF=SJF(N,instantes_ingresso,tempo_execucao)

N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_SRTF=SRTF(N,instantes_ingresso,tempo_execucao)

N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_PRIOC=PRIOC(N,instantes_ingresso,tempo_execucao,prioridade)

N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_PRIOP=PRIOP(N,instantes_ingresso,tempo_execucao,prioridade)

N=N_fixo
instantes_ingresso=instantes_ingresso_fixo[:]
tempo_execucao=tempo_execucao_fixo[:]
prioridade=prioridade_fixo[:]
results_PRIOD=PRIOD(N,instantes_ingresso,tempo_execucao,prioridade)

file_results=open('results.txt','w')
file_results.write('RESULTADOS DOS SIMULADORES DOS ALGORITMOS:\n\n')

file_results.write('\n-Algoritmo FCFS:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_FCFS[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_FCFS[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_FCFS[2]))

file_results.write('\n\n-Algoritmo RR:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_RR[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_RR[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_RR[2]))

file_results.write('\n\n-Algoritmo SJF:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_SJF[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_SJF[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_SJF[2]))

file_results.write('\n\n-Algoritmo SRTF:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_SRTF[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_SRTF[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_SRTF[2]))

file_results.write('\n\n-Algoritmo PRIOc:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_PRIOC[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_PRIOC[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_PRIOC[2]))

file_results.write('\n\n-Algoritmo PRIOp:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_PRIOP[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_PRIOP[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_PRIOP[2]))

file_results.write('\n\n-Algoritmo PRIOd:')
file_results.write('\nTempo medio de execucao:\n    ' + str(results_PRIOD[0]))
file_results.write('\nTempo medio de espera:\n    ' + str(results_PRIOD[1]))
file_results.write('\nTrocas de contexto:\n    ' + str(results_PRIOD[2]))
