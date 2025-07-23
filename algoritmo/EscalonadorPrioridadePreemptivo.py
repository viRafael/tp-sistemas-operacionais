import time
from collections import deque
from Base_Escalonador1 import *
from Tarefas import *

class EscalonadorPrioridadePreemptivo(EscalonadorCAV):

    def __init__(self, quantum, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)
        self.quantum = quantum

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0
        tempo_resposta_total = 0
        quantidade_tarefas = len(fila_chegada)

        while lista_execucao or fila_chegada:

            if lista_execucao and lista_execucao[0].tempo_restante == 0:
                tarefa_finalizada = lista_execucao.pop(0)
                tempo_resposta = contador - tarefa_finalizada.tempo_chegada
                print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a prioridade, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta

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
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

if __name__ == "__main__":
    # Criar algumas tarefas fictícias
    tarefas = criar_tarefas()

    # Criar uns CAV
    cav1 = CAV(id=1)
    for t in tarefas:
        cav1.adicionar_tarefa(t)

    #Criar um escalonador PrioridadePreemptivo 
    print("Simulando CAV com PrioridadePreemptivo: \n")
    escalonador_priopremp= EscalonadorPrioridadePreemptivo(2)
    for t in tarefas:
        escalonador_priopremp.adicionar_tarefa(t)
    
    simulador_pont = CAV(id=1)
    simulador_pont.executar_tarefas(escalonador_priopremp)