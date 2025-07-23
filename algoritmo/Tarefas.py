from Base_Escalonador1 import TarefaCAV

def criar_tarefas():
    tarefas = [
        TarefaCAV("Deteccao de Obstaculo", 6, prioridade=5, deadline=15, tempo_chegada=7),
        TarefaCAV("Planejamento de Rota", 7, prioridade=1, deadline=9, tempo_chegada=3),
        TarefaCAV("Manutencao de Velocidade", 1, prioridade=7, deadline=40, tempo_chegada=10),
        TarefaCAV("Comunicando com Infraestrutura", 3, prioridade=3, deadline=50, tempo_chegada=11)
    ]
    tarefas.sort(key=lambda tarefa: tarefa.tempo_chegada)  #ordena de acordo com o tempo de chegada
    return tarefas