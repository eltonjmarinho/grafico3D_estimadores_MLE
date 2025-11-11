# Projeto de Visualização 3D da Log-Verossimilhança

Este projeto visualiza a superfície da função de log-verossimilhança para um modelo de regressão linear simples. A aplicação foi estruturada utilizando o padrão Model-View-Controller (MVC).

Ao ser executado, o script gera dois gráficos (uma superfície 3D e um mapa de contorno 2D) e salva os dados calculados e os gráficos resultantes na pasta `results/`.

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação.
- `requirements.txt`: Lista de dependências do projeto.
- `results/`: Pasta contendo os resultados gerados.
  - `data/`: Armazena os dados da grade de verossimilhança em formato `.npz`.
  - `plots/`: Armazena os gráficos gerados em formato `.png`.
- `controllers/`: Contém a lógica de controle que liga o modelo e a visão.
  - `main_controller.py`: Orquestra a execução, gerando os dados e solicitando a plotagem.
- `models/`: Contém a lógica de negócio e manipulação de dados.
  - `estimation_model.py`: Define o modelo de regressão, gera os dados simulados e calcula a log-verossimilhança.
- `views/`: Contém a lógica de apresentação e interface com o usuário.
  - `plot_view.py`: Responsável por gerar e exibir os gráficos 3D e de contorno.

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
