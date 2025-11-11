import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

class PlotView:
    """
    Responsável por criar e exibir as visualizações gráficas.
    """
    def plot_3d_surface(self, B1, S2, LL, save_path=None):
        """Plota a superfície 3D da log-verossimilhança (estático)."""
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(B1, S2, LL, cmap="viridis", alpha=0.9)
        ax.set_xlabel(r"$\beta_1$")
        ax.set_ylabel(r"$\sigma^2$")
        ax.set_zlabel(r"$\log L(\beta_1, \sigma^2)$")
        ax.set_title(r"Superfície 3D da Log-Verossimilhança (fixando $\beta_0$ no MLE)")
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            print(f"Gráfico 3D (estático) salvo em: {save_path}")

    def plot_2d_contour(self, B1, S2, LL, save_path=None):
        """Plota as curvas de nível 2D da log-verossimilhança."""
        plt.figure(figsize=(8, 5))
        contour = plt.contourf(B1, S2, LL, levels=30, cmap="viridis")
        plt.colorbar(contour, label=r"$\log L(\beta_1, \sigma^2)$")
        plt.xlabel(r"$\beta_1$")
        plt.ylabel(r"$\sigma^2$")
        plt.title("Curvas de nível da log-verossimilhança")

        if save_path:
            plt.savefig(save_path)
            print(f"Gráfico de contorno salvo em: {save_path}")

    def plot_3d_surface_interactive(self, B1, S2, LL, save_path=None):
        """Plota a superfície 3D da log-verossimilhança (interativo)."""
        fig = go.Figure(data=[go.Surface(z=LL, x=B1, y=S2, colorscale='Viridis')])
        fig.update_layout(
            title='Superfície 3D da Log-Verossimilhança (Interativo)',
            scene=dict(
                xaxis_title='β1',
                yaxis_title='σ²',
                zaxis_title='Log L(β1, σ²)'
            )
        )
        
        if save_path:
            config = {'responsive': True}
            fig.write_html(save_path, include_plotlyjs='cdn', config=config)
            print(f"Gráfico 3D (interativo) salvo em: {save_path}")

    def show_plots(self):
        """Exibe as figuras do matplotlib."""
        plt.show()
