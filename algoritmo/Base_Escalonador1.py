from abc import ABC, abstractmethod

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

class TarefaCAV:
    def __init__(self, nome, duracao, tempo_chegada=0,prioridade=1, deadline = 2**32 -1):
        self.nome = nome            # Nome da tarefa (ex. Detecção de Obstáculo)
        self.duracao = duracao      # Tempo necessário para completar a tarefa (em segundos)
        self.prioridade = prioridade # Prioridade da tarefa (quanto menor o número, maior a prioridade)
        self.deadline = deadline     #Valor da deadline, caso não seja passado nenhum valor assume o maior valor possível para um sistema de 32 bits (daedline quase infinita)
        self.pontuacao = 6*(1/deadline) + 4*(1/prioridade) 
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