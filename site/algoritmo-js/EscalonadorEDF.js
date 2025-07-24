class EscalonadorEDF extends EscalonadorCAV { // Adicionado para forçar recarregamento // Adicionado para forçar recarregamento
    constructor(quantum, valor_sobrecarga = 1) {
        super(valor_sobrecarga);
        this.quantum = quantum;
    }

    async escalonar() {
        const executionResults = [];
        let executionQueue = [];
        let arrivalQueue = [...this.tarefas].sort((a, b) => a.tempo_chegada - b.tempo_chegada);
        let currentTime = 0;
        let overhead = 0;
        let log = [];
        let contextSwitches = 0;

        console.log("EDF: Iniciando escalonamento.");
        console.log("EDF: Tarefas iniciais (arrivalQueue):", arrivalQueue.map(t => t.nome));

        while (executionQueue.length > 0 || arrivalQueue.length > 0) {
            console.log(`EDF: Tempo atual: ${currentTime}, Fila de execução: ${executionQueue.map(t => t.nome)}, Fila de chegada: ${arrivalQueue.map(t => t.nome)}`);

            // Adiciona tarefas que chegaram
            while (arrivalQueue.length > 0 && arrivalQueue[0].tempo_chegada <= currentTime) {
                const arrivingTask = arrivalQueue.shift();
                executionQueue.push(arrivingTask);
                log.push(`📋 ${arrivingTask.nome} chegou`);
                executionQueue.sort((a, b) => a.deadline - b.deadline);
                console.log(`EDF: Tarefa ${arrivingTask.nome} chegou. Fila de execução após chegada e ordenação: ${executionQueue.map(t => t.nome)}`);
            }

            // Remove tarefas concluídas
            if (executionQueue.length > 0 && executionQueue[0].tempo_restante === 0) {
                const completedTask = executionQueue.shift();
                completedTask.completed = true;
                completedTask.tempo_final = currentTime;
                completedTask.waitTime = currentTime - completedTask.tempo_chegada - completedTask.duracao;
                log.push(`✅ ${completedTask.nome} finalizada`);
                console.log(`EDF: Tarefa ${completedTask.nome} finalizada.`);
            }

            if (executionQueue.length > 0) {
                const currentTask = executionQueue[0];
                const tempo_exec = Math.min(currentTask.tempo_restante, this.quantum);

                if (currentTask.tempo_inicio === 0 && currentTask.tempo_restante === currentTask.duracao) {
                    currentTask.tempo_inicio = currentTime;
                    console.log(`EDF: Tarefa ${currentTask.nome} iniciada em ${currentTime}.`);
                }

                executionResults.push({
                    taskName: currentTask.nome,
                    startTime: currentTime,
                    duration: tempo_exec,
                    taskIndex: this.tarefas.indexOf(currentTask)
                });

                currentTask.tempo_restante -= tempo_exec;
                currentTime += tempo_exec;
                log.push(`⚡ ${currentTask.nome}: ${tempo_exec}s`);
                console.log(`EDF: Executando ${currentTask.nome} por ${tempo_exec}s. Tempo restante: ${currentTask.tempo_restante}`);

                if (currentTask.tempo_restante > 0) {
                    overhead += this.valor_sobrecarga;
                    currentTime += this.valor_sobrecarga;
                    contextSwitches++;
                    executionQueue.sort((a, b) => a.deadline - b.deadline); // Re-sort after preemption
                    console.log(`EDF: Sobrecarga e troca de contexto. Tempo atual: ${currentTime}. Fila de execução após preempção e ordenação: ${executionQueue.map(t => t.nome)}`);
                }
            } else {
                currentTime++;
                console.log(`EDF: Nenhuma tarefa para executar. Incrementando tempo para ${currentTime}.`);
            }
        }

        const completedTasks = this.tarefas.filter(t => t.completed);
        const avgWaitTime = completedTasks.length > 0 ?
            completedTasks.reduce((sum, t) => sum + t.waitTime, 0) / completedTasks.length : 0;

        console.log("EDF: Escalonamento concluído.");
        return {
            executionResults,
            totalTime: currentTime,
            avgWaitTime,
            overhead,
            contextSwitches,
            completedTasks: completedTasks.length,
            log
        };
}
}