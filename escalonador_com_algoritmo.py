import random
import time
from collections import deque
from abc import ABC, abstractmethod

#Atual

# Para implementar um novo método de escalonamento, vocês devem criar uma nova classe que herda de Escalonador e implementar o método escalonar de acordo com sua estratégia.
# Este código fornece a base para que vocês experimentem e implementem suas próprias ideias de escalonamento, mantendo a estrutura flexível e fácil de estender.

class TarefaCAV:
    def __init__(self, nome, duracao, tempo_chegada=0,prioridade=1, deadline = 2**32 -1):
        self.nome = nome            # Nome da tarefa (ex. Detecção de Obstáculo)
        self.duracao = duracao      # Tempo necessário para completar a tarefa (em segundos)
        self.prioridade = prioridade # Prioridade da tarefa (quanto menor o número, maior a prioridade)
        self.deadline = deadline     #Valor da deadline, caso não seja passado nenhum valor assume o maior valor possível para um sistema de 32 bits (daedline quase infinita)
        self.pontuacao = (2*duracao)/(7*prioridade) 
        self.tempo_chegada = tempo_chegada
        self.tempo_restante = duracao # Tempo restante para completar a tarefa
        self.tempo_inicio = 0       # Hora em que a tarefa começa
        self.tempo_final = 0        # Hora em que a tarefa termina

    def __str__(self):
        return f"Tarefa {self.nome} (Prioridade {self.prioridade}): {self.duracao} segundos"

    def executar(self, quantum):
        """Executa a tarefa por um tempo de 'quantum' ou até terminar"""
        tempo_exec = min(self.tempo_restante, quantum)
        self.tempo_restante -= tempo_exec
        return tempo_exec

# Cada processo tem um nome, um tempo total de execução (tempo_execucao),
# e um tempo restante (tempo_restante), que é decrementado conforme o processo vai sendo executado.
# O método executar(quantum) executa o processo por uma quantidade limitada de tempo (quantum) ou até ele terminar.


# Classe abstrata de Escalonador
class EscalonadorCAV(ABC):
    def __init__(self, valor_sobrecarga=1):  #Podemos atribuir agora o valor da sobrecarga
        self.tarefas = []
        self.sobrecarga_total = 0
        self.valor_sobrecarga = valor_sobrecarga

    def adicionar_tarefa(self, tarefa):
        """Adiciona uma tarefa (ação do CAV) à lista de tarefas"""
        self.tarefas.append(tarefa)

    @abstractmethod
    def escalonar(self):
        """Método que será implementado pelos alunos para o algoritmo de escalonamento"""
        pass

    def registrar_sobrecarga(self, tempo):
        """Adiciona tempo de sobrecarga ao total"""
        self.sobrecarga_total += tempo

    def exibir_sobrecarga(self):
        """Exibe a sobrecarga total acumulada"""
        print(f"valor da sobrecarga: {self.valor_sobrecarga}")  #Mostra o valor atribuído a cada ocorrência de sobrecarga
        print(f"Sobrecarga total acumulada: {self.sobrecarga_total:.2f} segundos.\n") #Mostra a sobrecarga total

# A classe base Escalonador define a estrutura para os escalonadores, incluindo um método escalonar
# que vocês deverão implementar em suas versões específicas de escalonamento (como FIFO e Round Robin).


class EscalonadorFIFO(EscalonadorCAV):
    def __init__(self, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0

        while lista_execucao or fila_chegada:
            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()
                lista_execucao.append(tarefa)

            if lista_execucao:
                tarefa = lista_execucao[0]
                tempo_exec = tarefa.duracao
                tarefa.tempo_restante -= tempo_exec
                contador += tempo_exec
                print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                time.sleep(tempo_exec)
                print(f"Tarefa {tarefa.nome} finalizada, tempo de espera: {contador - tarefa.tempo_chegada}")
                lista_execucao.pop(0)

            else:
                contador += 1

        self.exibir_sobrecarga()

# O escalonador FIFO executa os processos na ordem em que foram adicionados, sem interrupção, até que todos os processos terminem.


class EscalonadorRoundRobin(EscalonadorCAV):
    def __init__(self, quantum, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)
        self.quantum = quantum

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0

        while lista_execucao or fila_chegada:

            if lista_execucao and lista_execucao[0].tempo_restante == 0:
                tarefa_finalizada = lista_execucao.pop(0)
                print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a prioridade, tempo de espera: {contador - tarefa_finalizada.tempo_chegada}")

            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()
                lista_execucao.append(tarefa)

            if lista_execucao:
                tarefa = lista_execucao[0]
                if tarefa.tempo_restante > 0:
                    tempo_exec = min(tarefa.tempo_restante, self.quantum)
                    tarefa.tempo_restante -= tempo_exec
                    contador += tempo_exec
                    print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                    time.sleep(tempo_exec)

                    if tarefa.tempo_restante > 0:
                        temp = lista_execucao.pop(0)
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga
                        lista_execucao.append(temp)

            else:
                contador += 1

        self.exibir_sobrecarga()

# O escalonador Round Robin permite que cada processo seja executado por um tempo limitado (quantum).
# Quando o processo termina ou o quantum é atingido, o próximo processo da fila é executado.
# Se o processo não terminar no quantum, ele é colocado de volta na fila.


class EscalonadorPrioridade(EscalonadorCAV):
    
    def __init__(self, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0

        while lista_execucao or fila_chegada:

            if lista_execucao and lista_execucao[0].tempo_restante == 0:
                tarefa_finalizada = lista_execucao.pop(0)
                print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a prioridade, tempo de espera: {contador - tarefa_finalizada.tempo_chegada}")

            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()
                lista_execucao.append(tarefa)
                lista_execucao.sort(key=lambda tarefa: tarefa.prioridade)

            if lista_execucao:
                tarefa = lista_execucao[0]
                tempo_exec = tarefa.duracao
                tarefa.tempo_restante -= tempo_exec
                contador += tempo_exec
                print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                time.sleep(tempo_exec)
                print(f"Tarefa {tarefa.nome} finalizada cumprindo a prioridade, tempo de espera: {contador - tarefa.tempo_chegada}")
                lista_execucao.pop(0)

            else:
                contador += 1

        self.exibir_sobrecarga()

class EscalonadorPrioridadePreemptivo(EscalonadorCAV):
    def __init__(self, quantum, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)
        self.quantum = quantum

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0

        while lista_execucao or fila_chegada:

            if lista_execucao and lista_execucao[0].tempo_restante == 0:
                tarefa_finalizada = lista_execucao.pop(0)
                print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a prioridade, tempo de espera: {contador - tarefa_finalizada.tempo_chegada}")

            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()
                lista_execucao.append(tarefa)
                lista_execucao.sort(key=lambda tarefa: tarefa.prioridade)

            if lista_execucao:
                tarefa = lista_execucao[0]

                if tarefa.tempo_restante > 0:
                    tempo_exec = min(tarefa.tempo_restante, self.quantum)
                    tarefa.tempo_restante -= tempo_exec
                    contador += tempo_exec
                    print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                    time.sleep(tempo_exec)

                    if tarefa.tempo_restante > 0:
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga

            else:
                contador += 1

        self.exibir_sobrecarga()

class EscalonadorEDF(EscalonadorCAV):
    
    def __init__(self, quantum, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)
        self.quantum = quantum

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0

        while lista_execucao or fila_chegada:

            if lista_execucao and lista_execucao[0].tempo_restante == 0:
                tarefa_finalizada = lista_execucao.pop(0)
                if contador <= tarefa_finalizada.deadline:
                    print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a deadline, tempo de espera: {contador - tarefa_finalizada.tempo_chegada}")

                else:
                    print(f"Tarefa {tarefa_finalizada.nome} finalizada não cumprindo a deadline, tempo de espera: {contador - tarefa_finalizada.tempo_chegada}")

            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()
                lista_execucao.append(tarefa)
                lista_execucao.sort(key=lambda tarefa: tarefa.deadline)

            if lista_execucao:
                tarefa = lista_execucao[0]

                if tarefa.tempo_restante > 0:
                    tempo_exec = min(tarefa.tempo_restante, self.quantum)
                    tarefa.tempo_restante -= tempo_exec
                    contador += tempo_exec
                    print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                    time.sleep(tempo_exec)

                    if tarefa.tempo_restante > 0:
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga
                

            else:
                contador += 1
            
            print(f"Tempo atual {contador}")

        self.exibir_sobrecarga()

class EscalonadorPontuacao(EscalonadorCAV):    
    def __init__(self, quantum, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)
        self.quantum = quantum

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0

        while lista_execucao or fila_chegada:

            if lista_execucao and lista_execucao[0].tempo_restante == 0:
                tarefa_finalizada = lista_execucao.pop(0)
                print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a prioridade, tempo de espera: {contador - tarefa_finalizada.tempo_chegada}")

            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()

                if tarefa.prioridade == 1:
                    tarefa.pontuacao = 10000

                lista_execucao.append(tarefa)
                lista_execucao.sort(key=lambda tarefa: tarefa.pontuacao, reverse=True)

            if lista_execucao and lista_execucao[0].pontuacao != 10000:
                for t in lista_execucao:
                    if t.tempo_restante < self.quantum:
                        lista_execucao.remove(t)
                        lista_execucao.insert(0,t)
                        break

            if lista_execucao:
                tarefa = lista_execucao[0]

                if tarefa.tempo_restante > 0:
                    tempo_exec = min(tarefa.tempo_restante, self.quantum)
                    tarefa.tempo_restante -= tempo_exec
                    contador += tempo_exec
                    print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                    time.sleep(tempo_exec)

                    if tarefa.tempo_restante > 0:
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga

            else:
                contador += 1

        self.exibir_sobrecarga()

class CAV:
    def __init__(self, id):
        self.id = id  # Identificador único para cada CAV
        self.tarefas = []  # Lista de tarefas atribuídas a esse CAV

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def executar_tarefas(self, escalonador):
        print(f"CAV {self.id} começando a execucao de tarefas...\n")
        escalonador.escalonar()
        print(f"CAV {self.id} terminou todas as suas tarefas.\n")


# Função para criar algumas tarefas fictícias
def criar_tarefas():
    tarefas = [
        TarefaCAV("Deteccao de Obstaculo", 6, prioridade=5, deadline=20, tempo_chegada=0),
        TarefaCAV("Planejamento de Rota", 7, prioridade=1, deadline=30, tempo_chegada=8),
        TarefaCAV("Manutencao de Velocidade", 1, prioridade=7, deadline=40, tempo_chegada=20),
        TarefaCAV("Comunicando com Infraestrutura", 3, prioridade=3, deadline=50, tempo_chegada=20)
    ]
    tarefas.sort(key=lambda tarefa: tarefa.tempo_chegada)  #ordena de acordo com o tempo de chegada
    return tarefas

# Exemplo de uso
if __name__ == "__main__":
    # Criar algumas tarefas fictícias
    tarefas = criar_tarefas()

    # Criar uns CAV
    cav1 = CAV(id=1)
    for t in tarefas:
        cav1.adicionar_tarefa(t)

    #Criar um escalonador Pontuação
    print("Simulando CAV com Pontuação: \n")
    escalonador_pont = EscalonadorPontuacao(2)
    for t in tarefas:
        escalonador_pont.adicionar_tarefa(t)
    
    simulador_pont = CAV(id=1)
    simulador_pont.executar_tarefas(escalonador_pont)

    #Criar um escalonador EDF 
    print("Simulando CAV com EDF:\n")
    escalonador_EDF= EscalonadorEDF(2)
    for t in tarefas:
        escalonador_EDF.adicionar_tarefa(t)

    simulador_EDF= CAV(id=1)
    simulador_EDF.executar_tarefas(escalonador_EDF)

    # Criar um escalonador com prioridade preemptivo 
    print("Simulando CAV com Prioridade preemptivo:\n")
    escalonador_prioridadePreemptivo= EscalonadorPrioridadePreemptivo(2)
    for t in tarefas:
        escalonador_prioridadePreemptivo.adicionar_tarefa(t)

    simulador_prioridadePreemptivo= CAV(id=1)
    simulador_prioridadePreemptivo.executar_tarefas(escalonador_prioridadePreemptivo)

    # Criar um escalonador FIFO
    print("Simulando CAV com FIFO:\n")
    escalonador_fifo = EscalonadorFIFO()
    for t in tarefas:
        escalonador_fifo.adicionar_tarefa(t)

    simulador_fifo = CAV(id=1)
    simulador_fifo.executar_tarefas(escalonador_fifo)

    # Criar um escalonador Round Robin com quantum de 3 segundos
    print("\nSimulando CAV com Round Robin:\n")
    escalonador_rr = EscalonadorRoundRobin(quantum=3)
    for t in tarefas:
        escalonador_rr.adicionar_tarefa(t)

    simulador_rr = CAV(id=1)
    simulador_rr.executar_tarefas(escalonador_rr)

    # Criar um escalonador por Prioridade
    print("\nSimulando CAV com Escalonamento por Prioridade:\n")
    escalonador_prio = EscalonadorPrioridade()
    for t in tarefas:
        escalonador_prio.adicionar_tarefa(t)

    simulador_prio = CAV(id=1)
    simulador_prio.executar_tarefas(escalonador_prio)