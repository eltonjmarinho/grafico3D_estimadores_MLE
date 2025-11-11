import numpy as np

class LikelihoodModel:
    """
    Encapsula a geração de dados e o cálculo da log-verossimilhança.
    """
    def __init__(self, n=50, beta_true=np.array([2.0, 0.8]), sigma2_true=1.5**2):
        np.random.seed(42)
        self.n = n
        self.beta_true = beta_true
        self.sigma2_true = sigma2_true
        self.X = None
        self.y = None

    def generate_data(self):
        """Gera dados simulados para o modelo de regressão."""
        x = np.linspace(0, 10, self.n)
        self.X = np.column_stack((np.ones(self.n), x))
        self.y = self.X @ self.beta_true + np.random.normal(0, np.sqrt(self.sigma2_true), self.n)
        return self.X, self.y

    def get_beta0_mle(self):
        """Calcula a estimativa de máxima verossimilhança para beta0."""
        if self.X is None or self.y is None:
            self.generate_data()
        
        # Para um modelo de regressão simples, o MLE de beta0 é o intercepto
        # da regressão de mínimos quadrados.
        beta_hat = np.linalg.lstsq(self.X, self.y, rcond=None)[0]
        return beta_hat[0]

    def log_likelihood(self, beta0, beta1, sigma2):
        """Calcula a log-verossimilhança para dados parâmetros."""
        resid = self.y - self.X @ np.array([beta0, beta1])
        ll = -0.5 * self.n * np.log(2 * np.pi * sigma2) - (resid @ resid) / (2 * sigma2)
        return ll

    def calculate_likelihood_grid(self, beta1_grid, sigma2_grid):
        """Calcula a log-verossimilhança para uma grade de parâmetros."""
        if self.X is None or self.y is None:
            self.generate_data()

        beta0_hat = self.get_beta0_mle()
        
        B1, S2 = np.meshgrid(beta1_grid, sigma2_grid)
        LL = np.zeros_like(B1)

        for i in range(B1.shape[0]):
            for j in range(B1.shape[1]):
                LL[i, j] = self.log_likelihood(beta0_hat, B1[i, j], S2[i, j])
        
        return B1, S2, LL

    def save_grid_data(self, path, B1, S2, LL):
        """Salva os dados da grade em um arquivo .npz."""
        np.savez_compressed(path, B1=B1, S2=S2, LL=LL)
