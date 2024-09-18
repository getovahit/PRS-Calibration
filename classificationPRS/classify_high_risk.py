import click
import pandas as pd
import numpy as np
from scipy.stats import norm

@click.command()
@click.option('--z-score-file', help='Path to the z-scores CSV file', default='z_scores_output.csv')
@click.option('--out-file', help='Output file with risk classification', default='risk_classification_output.csv')
@click.option('--low-risk-percentile', help='Percentile cutoff for low-risk classification (e.g., 20 for bottom 20%)', default=20.0, type=float)
@click.option('--high-risk-percentile', help='Percentile cutoff for high-risk classification (e.g., 90 for top 10%)', default=90.0, type=float)
def classify_risk(z_score_file, out_file, low_risk_percentile, high_risk_percentile):
    # Load z-scores
    z_scores_df = pd.read_csv(z_score_file)
    if 'z_score' not in z_scores_df.columns:
        raise ValueError("The input file must contain a 'z_score' column.")
    z_scores = z_scores_df['z_score'].values

    # Calculate the z-score cutoffs
    low_cutoff = norm.ppf(low_risk_percentile / 100.0)
    high_cutoff = norm.ppf(high_risk_percentile / 100.0)

    print(f"The z-score cutoff for low risk (bottom {low_risk_percentile}%) is: {low_cutoff:.4f}")
    print(f"The z-score cutoff for high risk (top {100-high_risk_percentile}%) is: {high_cutoff:.4f}")

    # Classify individuals
    risk_classification = pd.cut(z_scores, 
                                 bins=[-np.inf, low_cutoff, high_cutoff, np.inf], 
                                 labels=['Low', 'Typical', 'High'])

    # Add the risk classification to the DataFrame
    z_scores_df['risk_category'] = risk_classification

    # Save the updated DataFrame
    z_scores_df.to_csv(out_file, index=False)
    print(f"Risk classification has been saved to '{out_file}'.")

if __name__ == '__main__':
    classify_risk()
