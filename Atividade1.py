#Avaliador de algoritmos de escalonamento de tarefas:
#   FCFS
#   RR
#   SJF
#   SRTF

#   PRIOc
#   PRIOp
#   PRIOd

#ENTRADA:
#   Numero inteiro N indicando numero de tarefas
#   N valores inteiros indicando os instantes de ingresso de cada tarefa do sistema
#   N valores inteiros indicando o tempo de execução de cada tarefa
#   N valores inteiros indicando a prioridade das tarefas


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

    while ordem_fila!=[]:
        #adicionando os tempos
        momento+=1
        tempo_rodando[ordem_fila[0]]+=1
        for i in ordem_fila:
            if i!=ordem_fila[0]:
                tempo_parado[i]+=1
        tempo_execucao[ordem_fila[0]]-=1
        tempo_atual_quantum-=1

        #adicionando novas tarefas para a fila
        while momento in instantes_ingresso:
            ordem_fila.append(instantes_ingresso.index(momento))
            instantes_ingresso[instantes_ingresso.index(momento)]=-1

        #arrumando a fila
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
            troca_contexto+=1
            tempo_atual_quantum=tempo_quantum
        elif tempo_atual_quantum==0:
            auxiliar=ordem_fila[0]
            ordem_fila.remove(ordem_fila[0])
            ordem_fila.append(auxiliar)
            troca_contexto+=1
            tempo_atual_quantum=tempo_quantum

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

    while ordem_fila!=[]:
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

    while ordem_fila!=[]:
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
        aux_ordem_fila=ordem_fila[0]
        print('1')
        if tempo_execucao[ordem_fila[0]]==0:
            ordem_fila.remove(ordem_fila[0])
        print('2')
        ordem_fila=organiza_ordem_fila(ordem_fila,tempo_execucao)
        print('3')
        if ordem_fila!=[] and aux_ordem_fila!=ordem_fila[0]:
            troca_contexto+=1
        print('4')

    #arrumando a troca de contexto, pois no loop ela é adicionada 1 vez a mais quando acabam as tarefas
    #retornando as medias
    return [(sum(tempo_parado)+sum(tempo_rodando))/len(tempo_parado), sum(tempo_parado)/len(tempo_parado), troca_contexto]


#TESTES

N=5
instantes_ingresso=[0,0,1,3,5]
tempo_execucao=[5,2,4,1,2]
prioridade=[2,3,1,4,5]
SRTF(N,instantes_ingresso,tempo_execucao)
