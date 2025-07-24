import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from collections import deque
from abc import ABC, abstractmethod
import sys
from io import StringIO

# Importar suas classes originais (copiadas aqui para funcionar)
class TarefaCAV:
    def __init__(self, nome, duracao, tempo_chegada=0, prioridade=1, deadline=2**32-1):
        self.nome = nome
        self.duracao = duracao
        self.prioridade = prioridade
        self.deadline = deadline
        self.pontuacao = (2*duracao)/(7*prioridade)
        self.tempo_chegada = tempo_chegada
        self.tempo_restante = duracao
        self.tempo_inicio = 0
        self.tempo_final = 0

    def __str__(self):
        return f"Tarefa {self.nome} (Prioridade {self.prioridade}): {self.duracao} segundos"

    def executar(self, quantum):
        tempo_exec = min(self.tempo_restante, quantum)
        self.tempo_restante -= tempo_exec
        return tempo_exec

class EscalonadorCAV(ABC):
    def __init__(self, valor_sobrecarga=1):
        self.tarefas = []
        self.sobrecarga_total = 0
        self.valor_sobrecarga = valor_sobrecarga

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    @abstractmethod
    def escalonar(self):
        pass

    def registrar_sobrecarga(self, tempo):
        self.sobrecarga_total += tempo

    def exibir_sobrecarga(self):
        print(f"Valor da sobrecarga: {self.valor_sobrecarga}")
        print(f"Sobrecarga total acumulada: {self.sobrecarga_total:.2f} segundos.\n")

class EscalonadorFIFO(EscalonadorCAV):

    def __init__(self, ):
        super().__init__()

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0
        tempo_resposta_total = 0
        quantidade_tarefas = len(fila_chegada)

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
                time.sleep(0.1)
                tempo_resposta = contador - tarefa.tempo_chegada
                print(f"Tarefa {tarefa.nome} finalizada, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta
                lista_execucao.pop(0)

            else:
                contador += 1

        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

class EscalonadorRoundRobin(EscalonadorCAV):

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
                print(f"Tarefa {tarefa_finalizada.nome} finalizada, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta

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
                    time.sleep(0.1)

                    if tarefa.tempo_restante > 0:
                        temp = lista_execucao.pop(0)
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga
                        lista_execucao.append(temp)

            else:
                contador += 1

        self.exibir_sobrecarga()
        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

class EscalonadorPrioridade(EscalonadorCAV):
    
    def __init__(self, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0
        tempo_resposta_total = 0
        quantidade_tarefas = len(fila_chegada)

        while lista_execucao or fila_chegada:

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
                time.sleep(0.1)
                tempo_resposta = contador - tarefa.tempo_chegada
                print(f"Tarefa {tarefa.nome} finalizada cumprindo a prioridade, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta
                lista_execucao.pop(0)

            else:
                contador += 1

        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

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
                    time.sleep(0.1)

                    if tarefa.tempo_restante > 0:
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga

            else:
                contador += 1

        self.exibir_sobrecarga()
        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

class EscalonadorEDF(EscalonadorCAV):
    
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
                if contador <= tarefa_finalizada.deadline:
                    print(f"Tarefa {tarefa_finalizada.nome} finalizada cumprindo a deadline, tempo de resposta: {tempo_resposta}")

                else:
                    print(f"Tarefa {tarefa_finalizada.nome} finalizada não cumprindo a deadline, tempo de resposta: {tempo_resposta}")

                tempo_resposta_total += tempo_resposta

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
                    time.sleep(0.1)

                    if tarefa.tempo_restante > 0:
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga

            else:
                contador += 1

        self.exibir_sobrecarga()
        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

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
                    time.sleep(0.1)

                    if tarefa.tempo_restante > 0:
                        self.registrar_sobrecarga(self.valor_sobrecarga)
                        contador += self.valor_sobrecarga

            else:
                contador += 1

        self.exibir_sobrecarga()
        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")
     
class EscalonadorSJF(EscalonadorCAV):

    def __init__(self, valor_sobrecarga=1):
        super().__init__(valor_sobrecarga)

    def escalonar(self):
        lista_execucao = []
        fila_chegada = deque(self.tarefas)
        contador = 0
        tempo_resposta_total = 0
        quantidade_tarefas = len(fila_chegada)

        while lista_execucao or fila_chegada:
            while fila_chegada and fila_chegada[0].tempo_chegada <= contador:
                tarefa = fila_chegada.popleft()
                lista_execucao.append(tarefa)
                lista_execucao.sort(key=lambda tarefa: tarefa.duracao)

            if lista_execucao:
                tarefa = lista_execucao[0]
                tempo_exec = tarefa.duracao
                tarefa.tempo_restante -= tempo_exec
                contador += tempo_exec
                print(f"Executando tarefa {tarefa.nome} por {tempo_exec} segundos.")
                time.sleep(0.1)
                tempo_resposta = contador - tarefa.tempo_chegada
                print(f"Tarefa {tarefa.nome} finalizada, tempo de resposta: {tempo_resposta}")
                tempo_resposta_total += tempo_resposta
                lista_execucao.pop(0)

            else:
                contador += 1

        print("\n")
        print(f"Tempo de resposta médio = {tempo_resposta_total/quantidade_tarefas:.2f}")

class CAV:
    def __init__(self, id):
        self.id = id
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def executar_tarefas(self, escalonador):
        print(f"CAV {self.id} começando execução de tarefas...\n")
        escalonador.escalonar()
        print(f"CAV {self.id} terminou todas as suas tarefas.\n")

# Interface Gráfica
class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Escalonamento CAV - Sistema Operacionais")
        self.root.geometry("1500x900")
        self.root.configure(bg='#2c3e50')
        
        # Variáveis
        self.tarefas_criadas = []
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="🚗 SIMULADOR DE ESCALONAMENTO CAV", 
                              font=('Arial', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Sistema de Escalonamento de Processos para Carros Autônomos", 
                                 font=('Arial', 12), fg='#95a5a6', bg='#2c3e50')
        subtitle_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Painel esquerdo - Configurações
        left_frame = tk.LabelFrame(main_frame, text="⚙️ Configurações", font=('Arial', 14, 'bold'),
                                  fg='#ecf0f1', bg='#34495e', bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        
        self.setup_task_creation(left_frame)
        self.setup_scheduler_selection(left_frame)
        
        # Painel direito - Resultados
        right_frame = tk.LabelFrame(main_frame, text="📊 Resultados da Simulação", font=('Arial', 14, 'bold'),
                                   fg='#ecf0f1', bg='#34495e', bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=0)
        
        self.setup_results_panel(right_frame)
        
    def setup_task_creation(self, parent):
        # Frame para criação de tarefas
        task_frame = tk.LabelFrame(parent, text="➕ Criar Tarefas", font=('Arial', 12, 'bold'),
                                  fg='#ecf0f1', bg='#34495e')
        task_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Campos de entrada
        fields = [
            ("Nome:", "entry_nome"),
            ("Duração (s):", "entry_duracao"),
            ("Tempo Chegada (s):", "entry_chegada"),
            ("Prioridade (1-10):", "entry_prioridade"),
            ("Deadline (s):", "entry_deadline")
        ]
        
        self.entries = {}
        for i, (label, var_name) in enumerate(fields):
            tk.Label(task_frame, text=label, fg='#ecf0f1', bg='#34495e', font=('Arial', 10)).grid(
                row=i, column=0, sticky='w', padx=5, pady=2)
            
            entry = tk.Entry(task_frame, font=('Arial', 10), width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[var_name] = entry
        
        # Botões
        btn_frame = tk.Frame(task_frame, bg='#34495e')
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="➕ Adicionar Tarefa", command=self.adicionar_tarefa,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📋 Usar Exemplo", command=self.carregar_exemplo,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_tarefas,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Lista de tarefas
        list_frame = tk.Frame(task_frame, bg='#34495e')
        list_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10, sticky='ew')
        
        tk.Label(list_frame, text="📝 Tarefas Criadas:", fg='#ecf0f1', bg='#34495e', 
                font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.task_listbox = tk.Listbox(list_frame, height=6, font=('Arial', 9))
        self.task_listbox.pack(fill=tk.X, pady=5)
        
    def setup_scheduler_selection(self, parent):
        # Frame para seleção de escalonador
        sched_frame = tk.LabelFrame(parent, text="🔄 Algoritmos de Escalonamento", 
                                   font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        sched_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.scheduler_var = tk.StringVar(value="FIFO")
        
        schedulers = [
            ("FIFO (First In, First Out)", "FIFO"),
            ("Round Robin", "RoundRobin"),
            ("Prioridade (Não-Preemptivo)", "Prioridade"),
            ("Prioridade Preemptiva", "PrioridadePreemptiva"),
            ("EDF (Earliest Deadline First)", "EDF"),
            ("Pontuação", "Pontuacao"),
            ("SJF (Short Job First)", "SJF")
        ]
        
        for text, value in schedulers:
            tk.Radiobutton(sched_frame, text=text, variable=self.scheduler_var, value=value,
                          fg='#ecf0f1', bg='#34495e', selectcolor='#2c3e50',
                          font=('Arial', 10)).pack(anchor='w', padx=10, pady=2)
        
        # Parâmetros adicionais
        param_frame = tk.Frame(sched_frame, bg='#34495e')
        param_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(param_frame, text="Quantum (RR/EDF):", fg='#ecf0f1', bg='#34495e', 
                font=('Arial', 10)).grid(row=0, column=0, sticky='w')
        self.quantum_entry = tk.Entry(param_frame, width=10, font=('Arial', 10))
        self.quantum_entry.insert(0, "3")
        self.quantum_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(param_frame, text="Sobrecarga:", fg='#ecf0f1', bg='#34495e',
                font=('Arial', 10)).grid(row=1, column=0, sticky='w')
        self.sobrecarga_entry = tk.Entry(param_frame, width=10, font=('Arial', 10))
        self.sobrecarga_entry.insert(0, "1")
        self.sobrecarga_entry.grid(row=1, column=1, padx=5)
        
        # Botão de execução
        tk.Button(sched_frame, text="🚀 EXECUTAR SIMULAÇÃO", command=self.executar_simulacao,
                 bg='#e67e22', fg='white', font=('Arial', 12, 'bold'), height=2).pack(pady=15)
        
    def setup_results_panel(self, parent):
        # Área de resultados
        self.output_text = scrolledtext.ScrolledText(parent, height=35, font=('Consolas', 10),
                                                    bg='#1e1e1e', fg='#00ff00', insertbackground='white')
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de progresso
        progress_frame = tk.Frame(parent, bg='#34495e')
        progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(progress_frame, text="Status:", fg='#ecf0f1', bg='#34495e',
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.status_label = tk.Label(progress_frame, text="Pronto", fg='#2ecc71', bg='#34495e',
                                    font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.RIGHT)
        
    def adicionar_tarefa(self):
        try:
            nome = self.entries['entry_nome'].get().strip()
            duracao = int(self.entries['entry_duracao'].get())
            chegada = int(self.entries['entry_chegada'].get())
            prioridade = int(self.entries['entry_prioridade'].get())
            deadline = int(self.entries['entry_deadline'].get()) if self.entries['entry_deadline'].get() else 2**32-1
            
            if not nome:
                messagebox.showerror("Erro", "Nome da tarefa é obrigatório!")
                return
                
            if duracao <= 0 or chegada < 0 or prioridade < 1 or prioridade > 10:
                messagebox.showerror("Erro", "Valores inválidos! Verifique os campos.")
                return
            
            tarefa = TarefaCAV(nome, duracao, chegada, prioridade, deadline)
            self.tarefas_criadas.append(tarefa)
            
            # Atualizar lista
            self.atualizar_lista_tarefas()
            
            # Limpar campos
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
            messagebox.showinfo("Sucesso", f"Tarefa '{nome}' adicionada com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")
            
    def carregar_exemplo(self):
        self.tarefas_criadas = [
            TarefaCAV("Detecção de Obstáculo", 6, prioridade=5, deadline=20, tempo_chegada=0),
            TarefaCAV("Planejamento de Rota", 7, prioridade=1, deadline=30, tempo_chegada=8),
            TarefaCAV("Manutenção de Velocidade", 1, prioridade=7, deadline=40, tempo_chegada=20),
            TarefaCAV("Comunicação com Infraestrutura", 3, prioridade=3, deadline=50, tempo_chegada=20)
        ]
        self.atualizar_lista_tarefas()
        messagebox.showinfo("Exemplo Carregado", "Tarefas de exemplo carregadas com sucesso!")
        
    def limpar_tarefas(self):
        self.tarefas_criadas = []
        self.atualizar_lista_tarefas()
        self.output_text.delete(1.0, tk.END)
        
    def atualizar_lista_tarefas(self):
        self.task_listbox.delete(0, tk.END)
        for tarefa in self.tarefas_criadas:
            info = f"{tarefa.nome} | Dur:{tarefa.duracao}s | Prio:{tarefa.prioridade} | Chegada:{tarefa.tempo_chegada}s"
            self.task_listbox.insert(tk.END, info)
    
    def executar_simulacao(self):
        if not self.tarefas_criadas:
            messagebox.showerror("Erro", "Adicione pelo menos uma tarefa antes de executar!")
            return
            
        if self.is_running:
            messagebox.showwarning("Aviso", "Uma simulação já está em execução!")
            return
            
        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=self._executar_simulacao_thread)
        thread.daemon = True
        thread.start()
    
    def _executar_simulacao_thread(self):
        self.is_running = True
        self.progress.start()
        self.status_label.config(text="Executando...", fg='#f39c12')
        
        # Capturar output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            scheduler_type = self.scheduler_var.get()
            quantum = int(self.quantum_entry.get()) if self.quantum_entry.get() else 3
            sobrecarga = int(self.sobrecarga_entry.get()) if self.sobrecarga_entry.get() else 1
            
            # Copiar tarefas (para não modificar as originais)
            tarefas_copia = []
            for t in self.tarefas_criadas:
                nova_tarefa = TarefaCAV(t.nome, t.duracao, t.tempo_chegada, t.prioridade, t.deadline)
                tarefas_copia.append(nova_tarefa)
            
            tarefas_copia.sort(key=lambda x: x.tempo_chegada)
            
            # Criar escalonador
            if scheduler_type == "FIFO":
                escalonador = EscalonadorFIFO()
            elif scheduler_type == "RoundRobin":
                escalonador = EscalonadorRoundRobin(quantum, sobrecarga)
            elif scheduler_type == "Prioridade":
                escalonador = EscalonadorPrioridade(sobrecarga)
            elif scheduler_type == "EDF":
                escalonador = EscalonadorEDF(quantum, sobrecarga)
            elif scheduler_type == "Pontuacao":
                escalonador = EscalonadorPontuacao(quantum, sobrecarga)
            elif scheduler_type == "PrioridadePreemptiva":
                escalonador = EscalonadorPrioridadePreemptivo(quantum, sobrecarga)
            elif scheduler_type == "SJF":
                escalonador = EscalonadorSJF(sobrecarga)
        
            for tarefa in tarefas_copia:
                escalonador.adicionar_tarefa(tarefa)
            
            # Executar
            cav = CAV(1)
            cav.executar_tarefas(escalonador)
            
        except Exception as e:
            print(f"ERRO na simulação: {str(e)}")
        finally:
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            # Atualizar interface na thread principal
            self.root.after(0, self._update_output, output)
            
    def _update_output(self, output):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"=== SIMULAÇÃO COM {self.scheduler_var.get()} ===\n\n")
        self.output_text.insert(tk.END, output)
        self.output_text.see(tk.END)
        
        self.progress.stop()
        self.status_label.config(text="Concluído", fg='#2ecc71')
        self.is_running = False

def main():
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
