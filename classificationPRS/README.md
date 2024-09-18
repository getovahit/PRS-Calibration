# Risk Classification Script

This script classifies individuals into low, typical, and high-risk categories based on their Polygenic Risk Score (PRS) z-scores and user-specified percentile cutoffs.

## How the Script Works

### Input:
- `--z-score-file`: Path to your CSV file containing the sample IDs and z-scores (output from your first script).
- `--low-risk-percentile`: The percentile cutoff for low-risk classification (e.g., 20 for bottom 20%).
- `--high-risk-percentile`: The percentile cutoff for high-risk classification (e.g., 90 for top 10%).
- `--out-file`: Path for the output CSV file with risk classification.

### Processing:
1. Reads the z-scores from the input file.
2. Calculates the z-score cutoffs corresponding to the specified percentiles using the inverse cumulative distribution function of the standard normal distribution.
3. Classifies individuals into low, typical, or high risk based on their z-scores and the calculated cutoffs.

### Output:
- Adds a `risk_category` column to the DataFrame indicating whether each individual is classified as low, typical, or high risk.
- Saves the updated DataFrame to a new CSV file specified by `--out-file`.

## How to Use the Script

### 1. Ensure You Have the Required Packages Installed:

```bash
pip install pandas numpy scipy click
```

### 2. Save the Script:
Save the script to a file, e.g., `classify_risk.py`.

### 3. Prepare Your Z-Score File:
Make sure you have the z-scores calculated and saved in a CSV file (e.g., `z_scores_output.csv`) from your first script. The CSV file should contain at least two columns:
- `sample_id`: Unique identifiers for each individual.
- `z_score`: Calculated z-scores.

### 4. Run the Script:
Open a terminal and navigate to the directory containing the script. Run the script using Python, specifying your z-score file and desired percentile cutoffs.

Example Command:
```bash
python classify_risk.py \
    --z-score-file z_scores_output.csv \
    --out-file risk_classification_output.csv \
    --low-risk-percentile 20 \
    --high-risk-percentile 90
```

Parameters:
- `--z-score-file`: Path to your z-scores CSV file (output from the first script).
- `--out-file`: Path where the output CSV file with risk classification will be saved.
- `--low-risk-percentile`: The percentile cutoff for low-risk classification (e.g., 20 for bottom 20%).
- `--high-risk-percentile`: The percentile cutoff for high-risk classification (e.g., 90 for top 10%).

### 5. Interpreting the Output:
- The script will print the z-score cutoffs corresponding to your specified percentiles.
- An output CSV file (e.g., `risk_classification_output.csv`) will be generated, containing:
  - `sample_id`: Individual identifiers.
  - `z_score`: Original z-scores.
  - `risk_category`: Classification of 'Low', 'Typical', or 'High' risk.

## Example Usage

Suppose you have a z-score file `z_scores_output.csv` that looks like this:

```csv
sample_id,z_score
1,-1.5
2,0.5
3,0.0
4,2.0
5,1.0
```

Run the script:

```bash
python classify_risk.py \
    --z-score-file z_scores_output.csv \
    --out-file risk_classification_output.csv \
    --low-risk-percentile 20 \
    --high-risk-percentile 90
```

Expected Output:

```
The z-score cutoff for low risk (bottom 20.0%) is: -0.8416
The z-score cutoff for high risk (top 10.0%) is: 1.2816
Risk classification has been saved to 'risk_classification_output.csv'.
```

Output CSV (`risk_classification_output.csv`):

```csv
sample_id,z_score,risk_category
1,-1.5,Low
2,0.5,Typical
3,0.0,Typical
4,2.0,High
5,1.0,Typical
```

## Adjusting the Percentile Cutoffs

To classify individuals with different cutoffs, adjust the `--low-risk-percentile` and `--high-risk-percentile` arguments:

```bash
python classify_risk.py \
    --z-score-file z_scores_output.csv \
    --out-file risk_classification_output.csv \
    --low-risk-percentile 30 \
    --high-risk-percentile 95
```

This would classify the bottom 30% as low risk, the top 5% as high risk, and the remaining 65% as typical risk.

## Script Explanation

### Calculating the Z-Score Cutoffs:
```python
low_cutoff = norm.ppf(low_risk_percentile / 100.0)
high_cutoff = norm.ppf(high_risk_percentile / 100.0)
```
- Uses `norm.ppf()` from `scipy.stats` to get the z-scores corresponding to the specified percentiles.

### Classifying Individuals:
```python
risk_classification = pd.cut(z_scores, 
                             bins=[-np.inf, low_cutoff, high_cutoff, np.inf], 
                             labels=['Low', 'Typical', 'High'])
```
- Uses `pd.cut()` to categorize z-scores into 'Low', 'Typical', and 'High' risk categories based on the calculated cutoffs.

## Error Handling

The script checks if the `z_score` column exists in the input file and raises an error if not:

```python
if 'z_score' not in z_scores_df.columns:
    raise ValueError("The input file must contain a 'z_score' column.")
```

## Additional Notes

- **Assumption of Normality**: This method assumes that the z-scores are normally distributed with a mean of 0 and a standard deviation of 1.
- **Data Integrity**: Ensure that the z-scores in your input file are correctly calculated and not corrupted.
- **Flexibility**: You can specify any percentile cutoffs you desire for low and high risk.
- **Dependencies**: The script uses standard Python libraries and `click` for command-line argument parsing.

## Integration into Workflow

This script allows you to modularize your analysis:

1. Run your initial script to calculate z-scores from raw PRS scores, outputting a file like `z_scores_output.csv`.
2. Use this new script to classify individuals based on desired percentile cutoffs for low and high risk.

This separation makes it easy to experiment with different cutoffs without recalculating z-scores each time.
