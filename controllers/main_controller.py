import numpy as np
import os
from models.estimation_model import LikelihoodModel
from views.plot_view import PlotView

class MainController:
    """
    Orquestra a interação entre o modelo e a visão.
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
        2. Define a grade de parâmetros.
        3. Calcula a log-verossimilhança.
        4. Salva os dados da grade.
        5. Solicita à visão que plote e salve os resultados.
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
        print(f"Dados da grade salvos em: {data_filepath}")

        # 4. Plota e salva os resultados
        plot3d_path = os.path.join(self.plots_path, "log_likelihood_3d.png")
        plot3d_interactive_path = os.path.join(self.plots_path, "log_likelihood_3d.html")
        contour_path = os.path.join(self.plots_path, "log_likelihood_contour.png")
        
        self.view.plot_3d_surface(B1, S2, LL, save_path=plot3d_path)
        self.view.plot_3d_surface_interactive(B1, S2, LL, save_path=plot3d_interactive_path)
        self.view.plot_2d_contour(B1, S2, LL, save_path=contour_path)

        # 5. Exibe os gráficos do Matplotlib
        self.view.show_plots()
