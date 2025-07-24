

class EscalonadorCAV {
    constructor(valor_sobrecarga = 1) {
        this.tarefas = [];
        this.sobrecarga_total = 0;
        this.valor_sobrecarga = valor_sobrecarga;
    }

    adicionar_tarefa(tarefa) {
        /** Adiciona uma tarefa (ação do CAV) à lista de tarefas */
        this.tarefas.push(tarefa);
    }

    escalonar() {
        /** Método que será implementado pelos alunos para o algoritmo de escalonamento */
        throw new Error("O método 'escalonar' deve ser implementado pela subclasse.");
    }

    registrar_sobrecarga(tempo) {
        /** Adiciona tempo de sobrecarga ao total */
        this.sobrecarga_total += tempo;
    }

    exibir_sobrecarga() {
        /** Exibe a sobrecarga total acumulada */
        console.log(`valor da sobrecarga: ${this.valor_sobrecarga}`);
        console.log(`Sobrecarga total acumulada: ${this.sobrecarga_total.toFixed(2)} segundos.\n`);
    }
}

class TarefaCAV {
    constructor(nome, duracao, tempo_chegada = 0, prioridade = 1, deadline = Math.pow(2, 32) - 1) {
        this.nome = nome;
        this.duracao = duracao;
        this.prioridade = prioridade;
        this.deadline = deadline;
        this.pontuacao = 6 * (1 / deadline) + 4 * (1 / prioridade);
        this.tempo_chegada = tempo_chegada;
        this.tempo_restante = duracao;
        this.tempo_inicio = 0;
        this.tempo_final = 0;
        this.waitTime = 0;
        this.completed = false;
    }

    reset() {
        this.tempo_restante = this.duracao;
        this.tempo_inicio = 0;
        this.tempo_final = 0;
        this.waitTime = 0;
        this.completed = false;
    }

    toString() {
        return `Tarefa ${this.nome} (Prioridade ${this.prioridade}): ${this.duracao} segundos`;
    }

    executar(quantum) {
        /** Executa a tarefa por um tempo de 'quantum' ou até terminar */
        const tempo_exec = Math.min(this.tempo_restante, quantum);
        this.tempo_restante -= tempo_exec;
        return tempo_exec;
    }
}

class CAV {
    constructor(id) {
        this.id = id;
        this.tarefas = [];
    }

    adicionar_tarefa(tarefa) {
        this.tarefas.push(tarefa);
    }

    executar_tarefas(escalonador) {
        console.log(`CAV ${this.id} começando a execucao de tarefas...\n`);
        escalonador.escalonar();
        console.log(`CAV ${this.id} terminou todas as suas tarefas.\n`);
    }
}

