class EscalonadorPontuacao extends EscalonadorCAV {
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

        while (executionQueue.length > 0 || arrivalQueue.length > 0) {
            // Adiciona tarefas que chegaram
            while (arrivalQueue.length > 0 && arrivalQueue[0].tempo_chegada <= currentTime) {
                const arrivingTask = arrivalQueue.shift();
                executionQueue.push(arrivingTask);
                log.push(`📋 ${arrivingTask.nome} chegou`);
                // Re-sort based on pontuacao after new task arrives
                executionQueue.forEach(task => {
                    if (task.prioridade === 1) task.pontuacao = 10000;
                });
                executionQueue.sort((a, b) => b.pontuacao - a.pontuacao);
            }

            // Remove tarefas concluídas
            if (executionQueue.length > 0 && executionQueue[0].tempo_restante === 0) {
                const completedTask = executionQueue.shift();
                completedTask.completed = true;
                completedTask.tempo_final = currentTime;
                completedTask.waitTime = currentTime - completedTask.tempo_chegada - completedTask.duracao;
                log.push(`✅ ${completedTask.nome} finalizada`);
            }

            // Handle deadline misses
            if (executionQueue.length > 0 && currentTime > executionQueue[0].deadline) {
                const missedDeadlineTask = executionQueue.shift();
                missedDeadlineTask.completed = true; // Mark as completed to be counted
                missedDeadlineTask.tempo_final = currentTime;
                missedDeadlineTask.waitTime = currentTime - missedDeadlineTask.tempo_chegada - missedDeadlineTask.duracao;
                log.push(`❌ ${missedDeadlineTask.nome} não cumpriu o deadline e será encerrada.`);
            }

            // Prioritize short tasks if no critical tasks
            if (executionQueue.length > 0 && executionQueue[0].pontuacao !== 10000) {
                for (let i = 0; i < executionQueue.length; i++) {
                    if (executionQueue[i].tempo_restante < this.quantum) {
                        const shortTask = executionQueue.splice(i, 1)[0];
                        executionQueue.unshift(shortTask);
                        break;
                    }
                }
            }

            if (executionQueue.length > 0) {
                const currentTask = executionQueue[0];
                const tempo_exec = Math.min(currentTask.tempo_restante, this.quantum);

                if (currentTask.tempo_inicio === 0 && currentTask.tempo_restante === currentTask.duracao) {
                    currentTask.tempo_inicio = currentTime;
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

                if (currentTask.tempo_restante > 0) {
                    overhead += this.valor_sobrecarga;
                    currentTime += this.valor_sobrecarga;
                    contextSwitches++;
                    // Re-sort after preemption
                    executionQueue.forEach(task => {
                        if (task.prioridade === 1) task.pontuacao = 10000;
                    });
                    executionQueue.sort((a, b) => b.pontuacao - a.pontuacao);
                }
            } else {
                currentTime++;
            }
        }

        const completedTasks = this.tarefas.filter(t => t.completed);
        const avgWaitTime = completedTasks.length > 0 ?
            completedTasks.reduce((sum, t) => sum + t.waitTime, 0) / completedTasks.length : 0;

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
