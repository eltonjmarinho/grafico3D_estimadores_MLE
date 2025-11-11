# Projeto de Visualização 3D da Log-Verossimilhança

Este projeto visualiza a superfície da função de log-verossimilhança para um modelo de regressão linear simples. A aplicação foi estruturada utilizando o padrão Model-View-Controller (MVC).

Ao ser executado, o script gera os resultados e os salva na pasta `results/`.

## Saídas Geradas

- **Gráfico 3D Estático (`.png`):** Uma imagem da superfície de verossimilhança.
- **Gráfico 3D Interativo (`.html`):** Um arquivo HTML com um gráfico 3D que permite rotação e zoom, gerado com Plotly.
- **Gráfico de Contorno 2D (`.png`):** Um mapa de contorno da superfície.
- **Dados da Grade (`.npz`):** Um arquivo binário contendo os arrays (B1, S2, LL) usados para gerar os gráficos.

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação.
- `requirements.txt`: Lista de dependências do projeto.
- `results/`: Pasta contendo os resultados gerados.
  - `data/`: Armazena os dados da grade de verossimilhança.
  - `plots/`: Armazena os gráficos.
- `controllers/`: Contém a lógica de controle que liga o modelo e a visão.
- `models/`: Contém a lógica de negócio e manipulação de dados.
- `views/`: Contém a lógica de apresentação (criação dos gráficos).

## Como Executar

1.  **Crie um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    python main.py
    ```
Os arquivos de saída serão salvos na pasta `results`.
