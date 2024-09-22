import click
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import StandardScaler


class PRSAncestryCalibration:
    def __init__(self, n_pcs):
        self.n_pcs = n_pcs
        self.params = None
        self.scaler = StandardScaler()

    def negative_log_likelihood(self, params, prs, pcs):
        alpha = params[: self.n_pcs + 1]
        beta = params[self.n_pcs + 1 :]

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

        result = minimize(
            self.negative_log_likelihood,
            initial_params,
            args=(prs, pcs_scaled),
            method="BFGS",
        )
        self.params = result.x

    def calculate_z_score(self, prs, pcs):
        if self.params is None:
            raise ValueError("Model not fitted. Call fit() first.")

        pcs_scaled = self.scaler.transform(pcs)
        alpha = self.params[: self.n_pcs + 1]
        beta = self.params[self.n_pcs + 1 :]

        mu = alpha[0] + np.dot(pcs_scaled, alpha[1:])
        sigma = np.exp(beta[0] + np.dot(pcs_scaled, beta[1:]))

        # Adding a small constant to sigma to avoid division by zero
        epsilon = 1e-8
        sigma = np.maximum(sigma, epsilon)

        # Calculate z-scores
        z_scores = (prs - mu) / sigma

        return z_scores


def load_data(prs_file, pc_file, sample_col, prs_col, pc_col_prefix, sep):
    prs_data = pd.read_csv(prs_file, sep=sep)
    pc_data = pd.read_csv(pc_file, sep=sep)

    # Merge the data on 'sample_id' to ensure correct alignment
    merged_data = pd.merge(prs_data, pc_data, on=sample_col)

    # Extract PRS values
    prs = merged_data[prs_col].values

    # Extract PC columns
    pc_columns = [col for col in merged_data.columns if col.startswith(pc_col_prefix)]
    if not pc_columns:
        raise ValueError("No PC columns found in the data.")
    pcs = merged_data[pc_columns].values

    # Extract all columns except PC columns
    non_pc_columns = merged_data.drop(columns=pc_columns)

    return prs, pcs, non_pc_columns


@click.command()
@click.option("--prs-file", help="Path to your PRS data file", default="prs_data.csv")
@click.option("--pc-file", help="Path to your PCs data file", default="pc_data.csv")
@click.option("--out-file", help="Output file", default="z_scores_output.csv")
@click.option("--sample-col", help="Sample column name", default="sample_id")
@click.option("--prs-col", help="PRS column name", default="PRS")
@click.option("--pc-col-prefix", help="PC column prefix", default="PC")
@click.option("--delimiter", help="PC column prefix", default=",")
def main(prs_file, pc_file, out_file, sample_col, prs_col, pc_col_prefix, delimiter):
    # Load data
    prs, pcs, output_df = load_data(
        prs_file,
        pc_file,
        sample_col,
        prs_col=prs_col,
        pc_col_prefix=pc_col_prefix,
        sep=delimiter,
    )

    # Initialize and fit the model
    n_pcs = pcs.shape[1]  # Number of principal components
    prs_calibrator = PRSAncestryCalibration(n_pcs)
    prs_calibrator.fit(prs, pcs)

    # Calculate z-scores for individuals
    z_scores = prs_calibrator.calculate_z_score(prs, pcs)

    # Add the z_score column to non_pc_data
    output_df["z_score"] = z_scores

    # Output the DataFrame to a CSV file
    output_df.to_csv(out_file, index=False)
    print(f"Z-scores have been saved to '{out_file}'.")


if __name__ == "__main__":
    main()
