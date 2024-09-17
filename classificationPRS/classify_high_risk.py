import click
import pandas as pd
import numpy as np
from scipy.stats import norm

@click.command()
@click.option('--z-score-file', help='Path to the z-scores CSV file', default='z_scores_output.csv')
@click.option('--out-file', help='Output file with high-risk classification', default='high_risk_output.csv')
@click.option('--percentile-cutoff', help='Percentile cutoff for high-risk classification (e.g., 9 for top 9%)', default=9.0, type=float)
def classify_high_risk(z_score_file, out_file, percentile_cutoff):
    # Load z-scores
    z_scores_df = pd.read_csv(z_score_file)
    if 'z_score' not in z_scores_df.columns:
        raise ValueError("The input file must contain a 'z_score' column.")

    z_scores = z_scores_df['z_score'].values

    # Define your percentile cutoff
    # Convert top X% to cumulative probability
    percentile = 1 - (percentile_cutoff / 100.0)
    # Calculate the z-score cutoff
    z_cutoff = norm.ppf(percentile)
    print(f"The z-score cutoff for the top {percentile_cutoff}% is: {z_cutoff:.4f}")

    # Classify individuals
    high_risk = z_scores > z_cutoff

    # Add the high-risk classification to the DataFrame
    z_scores_df['high_risk'] = high_risk

    # Save the updated DataFrame
    z_scores_df.to_csv(out_file, index=False)
    print(f"High-risk classification has been saved to '{out_file}'.")

if __name__ == '__main__':
    classify_high_risk()
