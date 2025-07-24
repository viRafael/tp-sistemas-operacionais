# Trabalho de Sistemas Operacionais - Semestre 2025.1

## Descrição

Este repositório contém o trabalho prático da disciplina de **Sistemas Operacionais** do semestre 2025.1. O objetivo deste trabalho é implementar e testar diferentes algoritmos de escalonamento de processos em um sistema operacional simulado. O código foi desenvolvido como base para que os alunos possam propor modificações, otimizações e novos algoritmos de escalonamento, proporcionando uma aprendizagem prática sobre os conceitos fundamentais de escalonamento de processos.

## Estrutura do Projeto

```
algoritmo/    # Implementação dos algoritmos de escalonamento em Python
executavel/   # Scripts para gerar e rodar o executável da interface gráfica
site/         # Código do site para simulação e comparação dos algoritmos (HTML, JS, CSS)
```

- **algoritmo/**: Contém a base dos escalonadores e as implementações dos algoritmos (FIFO, Round Robin, Prioridade, EDF, Pontuação, SJF, etc).
- **executavel/**: Scripts para empacotar a interface gráfica em um executável para Windows ou Linux.
- **site/**: Interface web para simulação visual dos algoritmos, podendo ser aberta em qualquer navegador moderno.

## Como Executar o Simulador

### 1. Executando o Executável

#### **Windows**

1. Baixe o arquivo `SimuladorCAV_Win.exe'.
2. Dê um duplo clique no arquivo para abrir a interface gráfica.
3. Não é necessário instalar dependências.

#### **Linux**

1. Baixe o arquivo `SimuladorCAV`.
2. Torne o arquivo executável com o comando:
   ```sh
   chmod +x SimuladorCAV
   ```
3. Execute o simulador:
   ```sh
   ./SimuladorCAV
   ```

> **Obs:** Em ambos os sistemas, o executável pode ser gerado rodando o script correspondente em [`executavel/build_executable_win.py`](executavel/build_executable_win.py) ou [`executavel/build_executable_linux.py`](executavel/build_executable_linux.py).

## Observações

Além da implementação da base do escalonador, temos neste repositório:

- O algoritmo idealizado e implementado pela equipe.
- O código de um site que implementa a comparação entre algoritmos, incluindo o nosso.
- O código de uma aplicação que gera um executável do nosso site, incluindo o próprio executável.

## Créditos

Desenvolvido para a disciplina Sistemas Operacionais 2025.1

## Equipe Responsavel: 

#### Rafael Viera
#### Samuel Costa
#### Thales
#### Pedro
