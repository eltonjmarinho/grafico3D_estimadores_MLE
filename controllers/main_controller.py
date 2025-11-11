import numpy as np
import os
from models.estimation_model import LikelihoodModel
from views.plot_view import PlotView

class MainController:
    """
    Orquestra a interação entre o modelo e a visão para gerar e salvar os resultados.
    """
    def __init__(self):
        self.model = LikelihoodModel()
        self.view = PlotView()
        self.results_path = "results"
        self.plots_path = os.path.join(self.results_path, "plots")
        self.data_path = os.path.join(self.results_path, "data")

    def _setup_directories(self):
        """Cria os diretórios de saída se não existirem."""
        os.makedirs(self.plots_path, exist_ok=True)
        os.makedirs(self.data_path, exist_ok=True)

    def run(self):
        """
        Executa o fluxo principal da aplicação:
        1. Configura os diretórios de saída.
        2. Define a grade de parâmetros a serem analisados.
        3. Calcula a log-verossimilhança para cada ponto na grade.
        4. Salva os dados brutos da grade.
        5. Gera e salva os gráficos estáticos (PNG).
        6. Gera e salva um relatório HTML completo com gráficos interativos e estáticos.
        """
        self._setup_directories()

        # 1. Define a grade de valores para os parâmetros
        beta1_grid = np.linspace(0.3, 1.3, 80)
        sigma2_grid = np.linspace(0.5, 3.0, 80)

        # 2. Calcula a log-verossimilhança
        B1, S2, LL = self.model.calculate_likelihood_grid(beta1_grid, sigma2_grid)

        # 3. Salva os dados da grade
        data_filepath = os.path.join(self.data_path, "likelihood_grid.npz")
        self.model.save_grid_data(data_filepath, B1, S2, LL)

        # 4. Define os caminhos para os arquivos de saída
        static_3d_path = os.path.join(self.plots_path, "log_likelihood_3d.png")
        static_contour_path = os.path.join(self.plots_path, "log_likelihood_contour.png")
        html_report_path = os.path.join(self.plots_path, "relatorio_interativo.html")

        # 5. Gera e salva os gráficos estáticos (PNG)
        self.view.save_static_plots(B1, S2, LL, static_3d_path, static_contour_path)

        # 6. Gera o relatório HTML completo
        self.view.create_html_report(B1, S2, LL, html_report_path)
        
        print("\nProcesso concluído com sucesso!")