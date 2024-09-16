
import numpy as np
from scipy.optimize import minimize
import pandas as pd
from sklearn.preprocessing import StandardScaler

class PRSAncestryCalibration:
    def __init__(self, n_pcs):
        self.n_pcs = n_pcs
        self.params = None
        self.scaler = StandardScaler()

    def negative_log_likelihood(self, params, prs, pcs):
        n = len(prs)
        alpha = params[:self.n_pcs + 1]
        beta = params[self.n_pcs + 1:]
        
        mu = alpha[0] + np.dot(pcs, alpha[1:])
        sigma = np.exp(beta[0] + np.dot(pcs, beta[1:]))
        
        # Adding a small constant to sigma to avoid division by zero
        epsilon = 1e-8
        sigma = np.maximum(sigma, epsilon)
        
        # Computing the negative log likelihood
        nll = np.sum(np.log(sigma) + 0.5 * ((prs - mu) / sigma) ** 2)
        
        return nll

    def fit(self, prs, pcs):
        if prs is None or pcs is None:
            raise ValueError("PRS and PCs data must be provided.")
        
        pcs_scaled = self.scaler.fit_transform(pcs)
        initial_params = np.zeros(2 * (self.n_pcs + 1))
        
        result = minimize(self.negative_log_likelihood, initial_params, args=(prs, pcs_scaled), method='BFGS')
        self.params = result.x

    def calculate_z_score(self, prs, pcs):
        if self.params is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        pcs_scaled = self.scaler.transform(pcs)
        alpha = self.params[:self.n_pcs + 1]
        beta = self.params[self.n_pcs + 1:]
        
        mu = alpha[0] + np.dot(pcs_scaled, alpha[1:])
        sigma = np.exp(beta[0] + np.dot(pcs_scaled, beta[1:]))
        
        # Adding a small constant to sigma to avoid division by zero
        epsilon = 1e-8
        sigma = np.maximum(sigma, epsilon)
        
        # Calculate z-scores
        z_scores = (prs - mu) / sigma
        
        return z_scores

def load_data(prs_file, pc_file):
    prs_data = pd.read_csv(prs_file)
    pc_data = pd.read_csv(pc_file)
    
    # Ensure the order of samples is the same in both files
    common_samples = prs_data.index.intersection(pc_data.index)
    prs_data = prs_data.loc[common_samples]
    pc_data = pc_data.loc[common_samples]
    
    return prs_data['PRS'].values, pc_data.values

def main():
    # Load your data
    prs_file = 'path/to/your/prs_data.csv'  # CSV with columns: sample_id, PRS
    pc_file = 'path/to/your/pc_data.csv'    # CSV with columns: sample_id, PC1, PC2, ..., PCn
    
    prs, pcs = load_data(prs_file, pc_file)
    
    # Initialize and fit the model
    n_pcs = pcs.shape[1]  # Number of principal components
    prs_calibrator = PRSAncestryCalibration(n_pcs)
    prs_calibrator.fit(prs, pcs)
    
    # Calculate z-scores for individuals
    z_scores = prs_calibrator.calculate_z_score(prs, pcs)
    
    # Output z-scores
    print("Z-scores:", z_scores)

if __name__ == '__main__':
    main()
