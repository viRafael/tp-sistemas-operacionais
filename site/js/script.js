let tasks = [];
        let selectedAlgorithms = ['pontuacao'];
        let taskColors = ['task-a', 'task-b', 'task-c', 'task-d'];

        class Task {
            constructor(name, duration, priority, arrivalTime, deadline) {
                this.name = name;
                this.duration = duration;
                this.priority = priority;
                this.arrivalTime = arrivalTime;
                this.deadline = deadline || 4294967295; // 2^32 - 1
                this.remainingTime = duration;
                this.score = priority === 1 ? 10000 : (2 * duration) / (7 * priority);
                this.waitTime = 0;
                this.completed = false;
                this.startTime = 0;
                this.finishTime = 0;
            }

            reset() {
                this.remainingTime = this.duration;
                this.waitTime = 0;
                this.completed = false;
                this.startTime = 0;
                this.finishTime = 0;
            }
        }

        function toggleAlgorithm(algorithm) {
            const checkbox = document.getElementById(`alg-${algorithm}`);
            const container = checkbox.parentElement;
            
            checkbox.checked = !checkbox.checked;
            
            if (checkbox.checked) {
                container.classList.add('selected');
                if (!selectedAlgorithms.includes(algorithm)) {
                    selectedAlgorithms.push(algorithm);
                }
            } else {
                container.classList.remove('selected');
                selectedAlgorithms = selectedAlgorithms.filter(alg => alg !== algorithm);
            }
            
            // Ensure at least one algorithm is selected
            if (selectedAlgorithms.length === 0) {
                checkbox.checked = true;
                container.classList.add('selected');
                selectedAlgorithms.push(algorithm);
            }
        }

        function addTask() {
            const name = document.getElementById('taskName').value;
            const duration = parseInt(document.getElementById('taskDuration').value);
            const priority = parseInt(document.getElementById('taskPriority').value);
            const arrivalTime = parseInt(document.getElementById('taskArrival').value);
            const deadline = parseInt(document.getElementById('taskDeadline').value);

            if (!name || !duration || !priority) {
                alert('Por favor, preencha todos os campos obrigatórios!');
                return;
            }

            const task = new Task(name, duration, priority, arrivalTime, deadline);
            tasks.push(task);
            
            // Clear form
            document.getElementById('taskName').value = '';
            document.getElementById('taskDuration').value = '5';
            document.getElementById('taskPriority').value = '5';
            document.getElementById('taskArrival').value = '0';
            document.getElementById('taskDeadline').value = '50';
            
            updateTaskList();
        }

        function loadDefaultTasks() {
            tasks = [
                new Task("Detecção de Obstáculo", 6, 5, 0, 20),
                new Task("Planejamento de Rota", 7, 1, 8, 30),
                new Task("Manutenção de Velocidade", 1, 7, 20, 40),
                new Task("Comunicação com Infraestrutura", 3, 3, 20, 50)
            ];
            updateTaskList();
        }

        function clearTasks() {
            tasks = [];
            updateTaskList();
            document.getElementById('results').innerHTML = '';
            document.getElementById('comparisonTable').style.display = 'none';
            document.getElementById('comparisonMode').style.display = 'none';
        }

        function updateTaskList() {
            const tasksDiv = document.getElementById('tasks');
            tasksDiv.innerHTML = '';
            
            tasks.forEach((task, index) => {
                const taskDiv = document.createElement('div');
                taskDiv.className = 'task-item';
                taskDiv.innerHTML = `
                    <div class="task-info">
                        <div class="task-name">${task.name}</div>
                        <div class="task-details">
                            D: ${task.duration}s | P: ${task.priority} | C: ${task.arrivalTime}s | DL: ${task.deadline}s
                        </div>
                    </div>
                    <div class="task-score">${task.score.toFixed(1)}</div>
                `;
                tasksDiv.appendChild(taskDiv);
            });
        }

        function runComparison() {
            if (tasks.length === 0) {
                alert('Adicione pelo menos uma tarefa!');
                return;
            }

            if (selectedAlgorithms.length === 0) {
                alert('Selecione pelo menos um algoritmo!');
                return;
            }

            const quantum = parseInt(document.getElementById('quantum').value);
            const results = {};

            // Run each selected algorithm
            selectedAlgorithms.forEach(algorithm => {
                // Reset all tasks
                tasks.forEach(task => task.reset());
                
                results[algorithm] = runAlgorithm(algorithm, tasks, quantum);
            });

            displayResults(results);
        }

        function runAlgorithm(algorithm, taskList, quantum) {
            const executionResults = [];
            let executionQueue = [];
            let arrivalQueue = [...taskList].sort((a, b) => a.arrivalTime - b.arrivalTime);
            let currentTime = 0;
            let overhead = 0;
            let log = [];
            let contextSwitches = 0;

            while (executionQueue.length > 0 || arrivalQueue.length > 0) {
                // Remove completed tasks
                if (executionQueue.length > 0 && executionQueue[0].remainingTime === 0) {
                    const completedTask = executionQueue.shift();
                    completedTask.completed = true;
                    completedTask.finishTime = currentTime;
                    completedTask.waitTime = currentTime - completedTask.arrivalTime - completedTask.duration;
                    log.push(`✅ ${completedTask.name} finalizada`);
                }

                // Add arriving tasks
                while (arrivalQueue.length > 0 && arrivalQueue[0].arrivalTime <= currentTime) {
                    const arrivingTask = arrivalQueue.shift();
                    executionQueue.push(arrivingTask);
                    log.push(`📋 ${arrivingTask.name} chegou`);
                    
                    // Sort queue based on algorithm
                    sortQueue(executionQueue, algorithm);
                }

                // Execute task
                if (executionQueue.length > 0) {
                    const currentTask = executionQueue[0];
                    let executionTime;

                    switch (algorithm) {
                        case 'fifo':
                        case 'prioridade':
                            executionTime = currentTask.remainingTime;
                            break;
                        default:
                            executionTime = Math.min(currentTask.remainingTime, quantum);
                    }

                    if (currentTask.startTime === 0 && currentTask.remainingTime === currentTask.duration) {
                        currentTask.startTime = currentTime;
                    }

                    executionResults.push({
                        taskName: currentTask.name,
                        startTime: currentTime,
                        duration: executionTime,
                        taskIndex: taskList.indexOf(currentTask)
                    });

                    currentTask.remainingTime -= executionTime;
                    currentTime += executionTime;
                    log.push(`⚡ ${currentTask.name}: ${executionTime}s`);

                    // Handle preemption and context switch
                    if (currentTask.remainingTime > 0 && algorithm !== 'fifo' && algorithm !== 'prioridade') {
                        overhead += 1;
                        currentTime += 1;
                        contextSwitches++;
                        
                        // Special handling for pontuacao algorithm
                        if (algorithm === 'pontuacao') {
                            // Reapply pontuacao logic after each execution
                            executionQueue = handlePontuacaoQueue(executionQueue, quantum);
                        }
                    }
                } else {
                    currentTime += 1;
                }
            }

            const completedTasks = taskList.filter(t => t.completed);
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

        function sortQueue(queue, algorithm) {
            switch (algorithm) {
                case 'fifo':
                    // No sorting needed, FIFO maintains arrival order
                    break;
                case 'prioridade':
                case 'prioridadePreemptivo':
                    queue.sort((a, b) => a.priority - b.priority);
                    break;
                case 'edf':
                    queue.sort((a, b) => a.deadline - b.deadline);
                    break;
                case 'pontuacao':
                    queue.forEach(task => {
                        if (task.priority === 1) task.score = 10000;
                    });
                    queue.sort((a, b) => b.score - a.score);
                    break;
                case 'roundrobin':
                    // Round robin doesn't sort, just rotates
                    break;
            }
        }

        function handlePontuacaoQueue(queue, quantum) {
            // First, handle critical tasks (priority 1)
            queue.forEach(task => {
                if (task.priority === 1) task.score = 10000;
            });
            
            // Sort by score
            queue.sort((a, b) => b.score - a.score);
            
            // If no critical tasks, prioritize short tasks
            if (queue.length > 0 && queue[0].score !== 10000) {
                for (let i = 0; i < queue.length; i++) {
                    if (queue[i].remainingTime < quantum) {
                        const shortTask = queue.splice(i, 1)[0];
                        queue.unshift(shortTask);
                        break;
                    }
                }
            }
            
            return queue;
        }

        function createWaitTimeline(executionResults, maxTime) {
            const periods = [];
            let currentTime = 0;
            
            // Criar lista de todos os períodos ocupados
            const occupiedPeriods = executionResults.map(exec => ({
                start: exec.startTime,
                end: exec.startTime + exec.duration
            })).sort((a, b) => a.start - b.start);
            
            occupiedPeriods.forEach(period => {
                // Adicionar espera antes deste período
                if (period.start > currentTime) {
                    periods.push({
                        type: 'wait',
                        start: currentTime,
                        duration: period.start - currentTime
                    });
                }
                
                // Adicionar período ocupado (não-espera)
                periods.push({
                    type: 'execution',
                    start: period.start,
                    duration: period.end - period.start
                });
                
                currentTime = Math.max(currentTime, period.end);
            });
            
            // Adicionar espera final se necessário
            if (currentTime < maxTime) {
                periods.push({
                    type: 'wait',
                    start: currentTime,
                    duration: maxTime - currentTime
                });
            }
            
            return periods;
        }

        function createOverheadTimeline(executionResults, maxTime) {
            const periods = [];
            let currentTime = 0;
            
            executionResults.forEach((execution, index) => {
                // Período antes da execução
                if (execution.startTime > currentTime) {
                    const gapDuration = execution.startTime - currentTime;
                    
                    // Se o gap é exatamente 1, é sobrecarga
                    if (gapDuration === 1 && index > 0) {
                        periods.push({
                            type: 'overhead',
                            start: currentTime,
                            duration: 1
                        });
                    } else if (gapDuration > 0) {
                        periods.push({
                            type: 'empty',
                            start: currentTime,
                            duration: gapDuration
                        });
                    }
                }
                
                // Período da execução (não é sobrecarga)
                periods.push({
                    type: 'empty',
                    start: execution.startTime,
                    duration: execution.duration
                });
                
                currentTime = execution.startTime + execution.duration;
            });
            
            // Completar até o final
            if (currentTime < maxTime) {
                periods.push({
                    type: 'empty',
                    start: currentTime,
                    duration: maxTime - currentTime
                });
            }
            
            return periods;
        }

        function displayResults(results) {
            const resultsDiv = document.getElementById('results');
            const comparisonMode = document.getElementById('comparisonMode');
            const comparisonTable = document.getElementById('comparisonTable');
            
            const isComparison = Object.keys(results).length > 1;
            
            if (isComparison) {
                comparisonMode.style.display = 'block';
                resultsDiv.innerHTML = '<div class="comparison-results"></div>';
                const comparisonDiv = resultsDiv.querySelector('.comparison-results');
                
                Object.entries(results).forEach(([algorithm, result]) => {
                    const algorithmDiv = document.createElement('div');
                    algorithmDiv.className = 'algorithm-result';
                    algorithmDiv.innerHTML = createAlgorithmResult(algorithm, result);
                    comparisonDiv.appendChild(algorithmDiv);
                });
                
                displayComparisonTable(results);
            } else {
                comparisonMode.style.display = 'none';
                const algorithm = Object.keys(results)[0];
                const result = results[algorithm];
                resultsDiv.innerHTML = `<div class="single-result">${createAlgorithmResult(algorithm, result)}</div>`;
                comparisonTable.style.display = 'none';
            }
        }

        function createAlgorithmResult(algorithm, result) {
            const algorithmNames = {
                pontuacao: 'Pontuação',
                fifo: 'FIFO',
                roundrobin: 'Round Robin',
                prioridade: 'Prioridade',
                prioridadePreemptivo: 'Prioridade Preemptivo',
                edf: 'EDF'
            };

            return `
                <div class="algorithm-title">${algorithmNames[algorithm]}</div>
                <div class="timeline">
                    ${createTimeline(result.executionResults)}
                </div>
                <div class="algorithm-stats">
                    <div class="stat-item">
                        <div class="stat-value">${result.totalTime}</div>
                        <div class="stat-label">Tempo Total (s)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.avgWaitTime.toFixed(1)}</div>
                        <div class="stat-label">Tempo Médio de Espera (s)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.overhead}</div>
                        <div class="stat-label">Sobrecarga (s)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.completedTasks}</div>
                        <div class="stat-label">Tarefas Concluídas</div>
                    </div>
                </div>
                <div class="execution-log">
                    ${result.log.slice(-10).map(entry => `<div>${entry}</div>`).join('')}
                </div>
            `;
        }

        function createTimeline(executionResults) {
            if (executionResults.length === 0) return '<div>Nenhuma execução</div>';
            
            const maxTime = Math.max(...executionResults.map(r => r.startTime + r.duration));
            
            let html = '<div class="timeline-container">';
            
            // Scale
            html += '<div class="timeline-scale">';
            for (let i = 0; i <= Math.min(maxTime, 20); i++) {
                html += `<div class="timeline-tick">${i}</div>`;
            }
            if (maxTime > 20) html += `<div class="timeline-tick">...${maxTime}</div>`;
            html += '</div>';
            
        // Estado bars - Execução, Espera, Sobrecarga
            const stateTypes = ['Execução', 'Espera', 'Sobrecarga'];
            const stateColors = ['task-a', 'task-b', 'task-c'];

            stateTypes.forEach((stateType, stateIndex) => {
                html += '<div class="timeline-bar">';
                html += `<div class="task-label">${stateType}</div>`;
                
                let currentPos = 0;
                
                if (stateType === 'Execução') {
                    // Mostrar períodos de execução
                    executionResults.forEach(execution => {
                        // Add gap if needed (períodos de não-execução)
                        if (execution.startTime > currentPos) {
                            const gapWidth = ((execution.startTime - currentPos) / Math.max(maxTime, 20)) * 100;
                            html += `<div style="width: ${gapWidth}%; height: 20px;"></div>`;
                        }
                        
                        const width = (execution.duration / Math.max(maxTime, 20)) * 100;
                        html += `<div class="task-execution ${stateColors[0]}" style="width: ${width}%;">${execution.taskName.substring(0, 3)}</div>`;
                        currentPos = execution.startTime + execution.duration;
                    });
                } else if (stateType === 'Espera') {
                    // Mostrar períodos de espera (inverso da execução)
                    const allPeriods = createWaitTimeline(executionResults, maxTime);
                    allPeriods.forEach(period => {
                        const width = (period.duration / Math.max(maxTime, 20)) * 100;
                        if (period.type === 'wait') {
                            html += `<div class="task-execution ${stateColors[1]}" style="width: ${width}%;">Espera</div>`;
                        } else {
                            html += `<div style="width: ${width}%; height: 20px;"></div>`;
                        }
                    });
                } else if (stateType === 'Sobrecarga') {
                    // Mostrar períodos de sobrecarga
                    const overheadPeriods = createOverheadTimeline(executionResults, maxTime);
                    overheadPeriods.forEach(period => {
                        const width = (period.duration / Math.max(maxTime, 20)) * 100;
                        if (period.type === 'overhead') {
                            html += `<div class="task-execution ${stateColors[2]}" style="width: ${width}%;">CS</div>`;
                        } else {
                            html += `<div style="width: ${width}%; height: 20px;"></div>`;
                        }
                    });
                }
                
                html += '</div>';
            });
            return html;
        }

        function displayComparisonTable(results) {
            const comparisonTable = document.getElementById('comparisonTable');
            const tableContent = document.getElementById('tableContent');
            
            // Find best results
            const metrics = ['totalTime', 'avgWaitTime', 'overhead', 'contextSwitches'];
            const bestResults = {};
            
            metrics.forEach(metric => {
                const values = Object.entries(results).map(([alg, res]) => ({
                    algorithm: alg,
                    value: res[metric]
                }));
                bestResults[metric] = values.reduce((best, current) => 
                    current.value < best.value ? current : best
                ).algorithm;
            });
            
            // Create table
            let tableHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>Algoritmo</th>
                            <th>Tempo Total (s)</th>
                            <th>Tempo Médio de Espera (s)</th>
                            <th>Sobrecarga (s)</th>
                            <th>Mudanças de Contexto</th>
                            <th>Tarefas Concluídas</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            const algorithmNames = {
                pontuacao: 'Pontuação',
                fifo: 'FIFO',
                roundrobin: 'Round Robin',
                prioridade: 'Prioridade',
                prioridadePreemptivo: 'Prioridade Preemptivo',
                edf: 'EDF'
            };
            
            Object.entries(results).forEach(([algorithm, result]) => {
                tableHTML += '<tr>';
                tableHTML += `<td><strong>${algorithmNames[algorithm]}</strong></td>`;
                tableHTML += `<td class="${bestResults.totalTime === algorithm ? 'best-result' : ''}">${result.totalTime}</td>`;
                tableHTML += `<td class="${bestResults.avgWaitTime === algorithm ? 'best-result' : ''}">${result.avgWaitTime.toFixed(1)}</td>`;
                tableHTML += `<td class="${bestResults.overhead === algorithm ? 'best-result' : ''}">${result.overhead}</td>`;
                tableHTML += `<td class="${bestResults.contextSwitches === algorithm ? 'best-result' : ''}">${result.contextSwitches}</td>`;
                tableHTML += `<td>${result.completedTasks}</td>`;
                tableHTML += '</tr>';
            });
            
            tableHTML += '</tbody></table>';
            tableContent.innerHTML = tableHTML;
            comparisonTable.style.display = 'block';
        }

        let isFullscreen = false;
        function toggleFullscreen() {
            const visualizationPanel = document.querySelector('.visualization-panel');
            const mainContent = document.querySelector('.main-content');
            const fullscreenBtn = document.getElementById('fullscreenBtn');
            
            isFullscreen = !isFullscreen;
            
            if (isFullscreen) {
                visualizationPanel.classList.add('fullscreen');
                mainContent.classList.add('fullscreen-mode');
                fullscreenBtn.innerHTML = '🗙 Fechar';
                fullscreenBtn.title = 'Sair do modo expandido';
                
                // Prevenir scroll do body quando expandido
                document.body.style.overflow = 'hidden';
            } else {
                visualizationPanel.classList.remove('fullscreen');
                mainContent.classList.remove('fullscreen-mode');
                fullscreenBtn.innerHTML = '🔍 Expandir';
                fullscreenBtn.title = 'Expandir visualização';
                
                // Restaurar scroll do body
                document.body.style.overflow = 'auto';
            }
        }

        // Fechar com ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isFullscreen) {
                toggleFullscreen();
            }
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Set initial selected algorithm
            document.getElementById('alg-pontuacao').checked = true;
            document.querySelector('[onclick="toggleAlgorithm(\'pontuacao\')"]').classList.add('selected');
            
            // Load default tasks
            loadDefaultTasks();
        });