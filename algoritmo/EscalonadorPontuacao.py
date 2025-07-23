import time
from collections import deque
from Base_Escalonador1 import * 
from Tarefas import *

class EscalonadorPontuacao(EscalonadorCAV):    

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
                print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a prioridade e o deadline, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta

            if lista_execucao and contador > lista_execucao[0].deadline:
                tarefa_finalizada = lista_execucao.pop(0)
                tempo_resposta = contador - tarefa_finalizada.tempo_chegada
                print(f"Tarefa {tarefa_finalizada.nome} nao cumpriu o deadline e sera encerrada, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta
                                    

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
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")
        
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