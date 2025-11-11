import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import base64
from io import BytesIO
import json

class PlotView:
    """
    Responsável por criar e salvar as visualizações gráficas.
    """

    def _get_static_3d_surface_as_base64(self, B1, S2, LL):
        """Gera o gráfico 3D estático e retorna como uma string base64."""
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(B1, S2, LL, cmap="viridis", alpha=0.9)
        ax.set_xlabel(r"$\beta_1$")
        ax.set_ylabel(r"$\sigma^2$")
        ax.set_zlabel(r"$\log L(\beta_1, \sigma^2)$")
        ax.set_title(r"Superfície 3D da Log-Verossimilhança (fixando $\eta_0$ no MLE)")
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def _get_static_2d_contour_as_base64(self, B1, S2, LL):
        """Gera o gráfico de contorno estático e retorna como uma string base64."""
        fig = plt.figure(figsize=(8, 5))
        contour = plt.contourf(B1, S2, LL, levels=30, cmap="viridis")
        plt.colorbar(contour, label=r"$\log L(\beta_1, \sigma^2)$")
        plt.xlabel(r"$\beta_1$")
        plt.ylabel(r"$\sigma^2$")
        plt.title("Curvas de nível da log-verossimilhança")
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def save_static_plots(self, B1, S2, LL, path_3d, path_contour):
        """Salva as versões estáticas (PNG) dos gráficos."""
        # Gráfico 3D
        fig_3d = plt.figure(figsize=(10, 6))
        ax = fig_3d.add_subplot(111, projection="3d")
        ax.plot_surface(B1, S2, LL, cmap="viridis", alpha=0.9)
        ax.set_xlabel(r"$\beta_1$")
        ax.set_ylabel(r"$\sigma^2$")
        ax.set_zlabel(r"$\log L(\beta_1, \sigma^2)$")
        ax.set_title(r"Superfície 3D da Log-Verossimilhança (fixando $\eta_0$ no MLE)")
        plt.tight_layout()
        plt.savefig(path_3d)
        plt.close(fig_3d)
        print(f"Gráfico 3D (estático) salvo em: {path_3d}")

        # Gráfico de Contorno
        fig_contour = plt.figure(figsize=(8, 5))
        contour = plt.contourf(B1, S2, LL, levels=30, cmap="viridis")
        plt.colorbar(contour, label=r"$\log L(\beta_1, \sigma^2)$")
        plt.xlabel(r"$\beta_1$")
        plt.ylabel(r"$\sigma^2$")
        plt.title("Curvas de nível da log-verossimilhança")
        plt.tight_layout()
        plt.savefig(path_contour)
        plt.close(fig_contour)
        print(f"Gráfico de contorno salvo em: {path_contour}")

    def create_html_report(self, B1, S2, LL, save_path):
        """
        Cria um relatório HTML autônomo e responsivo usando a técnica de "data island"
        para garantir a máxima compatibilidade e robustez.
        """
        
        # 1. Cria as figuras interativas
        fig_3d = go.Figure(data=[go.Surface(
            z=LL,
            x=B1,
            y=S2,
            colorscale='Viridis',
            cmin=LL.min(),
            cmax=LL.max(),
            colorbar=dict(
                title='Log-Likelihood',
                orientation='h',
                x=0.5,
                y=-0.1,
                xanchor='center',
                yanchor='bottom'
            )
        )])
        fig_3d.update_layout(
            title='Superfície 3D da Log-Verossimilhança',
            scene=dict(
                xaxis_title='β1',
                yaxis_title='σ²',
                zaxis_title='Log L',
                camera=dict(
                    eye=dict(x=2.0, y=2.0, z=1.5)  # Afasta a câmera para "zoom out"
                )
            ),
            margin=dict(l=40, r=40, b=40, t=80)
        )

        fig_contour = go.Figure(data=go.Contour(z=LL, x=B1[0], y=S2[:, 0], colorscale='Viridis', contours=dict(coloring='heatmap')))
        fig_contour.update_layout(
            title='Curvas de Nível da Log-Verossimilhança',
            xaxis_title='β1',
            yaxis_title='σ²',
            margin=dict(l=40, r=40, b=40, t=80)
        )

        # 2. Serializa as figuras para JSON
        fig_3d_json = fig_3d.to_json()
        fig_contour_json = fig_contour.to_json()

        # 3. Cria o template HTML usando a técnica "data island"
        html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Relatório Interativo de Análise</title>
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 1rem;
            background-color: #f8f9fa;
            color: #212529;
        }}
        h1 {{
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }}
        .plot-container {{
            width: 100%;
            height: 75vh;
            min-height: 450px;
            margin-bottom: 2rem;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <h1>Relatório Interativo da Log-Verossimilhança</h1>

    <!-- Divs onde os gráficos serão renderizados -->
    <div id="plot-3d" class="plot-container"></div>
    <div id="plot-contour" class="plot-container"></div>

    <!-- "Data Islands" para armazenar os dados JSON de forma segura -->
    <script id="fig3d-data" type="application/json">{fig_3d_json}</script>
    <script id="figContour-data" type="application/json">{fig_contour_json}</script>

    <!-- Script principal para renderizar os gráficos -->
    <script>
        window.addEventListener('DOMContentLoaded', (event) => {{
            console.log("DOM fully loaded. Attempting to render plots.");
            try {{
                const config = {{'responsive': true}};

                // Gráfico 3D
                const fig3dDataElement = document.getElementById('fig3d-data');
                const fig3dJson = fig3dDataElement.textContent;
                const fig3d = JSON.parse(fig3dJson);
                console.log("Successfully parsed 3D plot data.");
                Plotly.newPlot('plot-3d', fig3d.data, fig3d.layout, config);
                console.log("3D plot rendering call finished.");

                // Gráfico de Contorno
                const figContourDataElement = document.getElementById('figContour-data');
                const figContourJson = figContourDataElement.textContent;
                const figContour = JSON.parse(figContourJson);
                console.log("Successfully parsed contour plot data.");
                Plotly.newPlot('plot-contour', figContour.data, figContour.layout, config);
                console.log("Contour plot rendering call finished.");

            }} catch (e) {{
                console.error("An error occurred during plotting:", e);
                const errorDiv = document.createElement('div');
                errorDiv.style.cssText = "padding: 1em; background-color: #ffdddd; border: 1px solid #ff0000; color: #d8000c;";
                errorDiv.innerHTML = `<h3>Ocorreu um erro ao renderizar os gráficos.</h3><p>Por favor, abra o console do desenvolvedor (F12) para ver os detalhes técnicos.</p><pre>${{e.stack}}</pre>`;
                document.body.appendChild(errorDiv);
            }}
        }});
    </script>
</body>
</html>
"""
        # 4. Salva o arquivo
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"Relatório HTML interativo e responsivo salvo em: {save_path}")