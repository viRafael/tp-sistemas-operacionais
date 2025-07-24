function criar_tarefas() {
    let tarefas = [
        new TarefaCAV("Deteccao de Obstaculo", 6, 7, 5, 15),
        new TarefaCAV("Planejamento de Rota", 7, 3, 1, 9),
        new TarefaCAV("Manutencao de Velocidade", 1, 10, 7, 40),
        new TarefaCAV("Comunicando com Infraestrutura", 3, 11, 3, 50)
    ];
    tarefas.sort((a, b) => a.tempo_chegada - b.tempo_chegada);
    return tarefas;
}
