# High-Risk Classification Script

This script classifies individuals as high-risk based on their Polygenic Risk Score (PRS) z-scores and a specified percentile cutoff.

## How the Script Works

### Input:
- `--z-score-file`: Path to your CSV file containing the sample IDs and z-scores (output from your first script).
- `--percentile-cutoff`: The desired percentile cutoff (e.g., 9 for the top 9%).
- `--out-file`: Path for the output CSV file with high-risk classification.

### Processing:
1. Reads the z-scores from the input file.
2. Calculates the z-score cutoff corresponding to the specified percentile using the inverse cumulative distribution function of the standard normal distribution.
3. Classifies individuals as high risk if their z-score exceeds the cutoff.

### Output:
- Adds a `high_risk` column to the DataFrame indicating whether each individual is classified as high risk (True or False).
- Saves the updated DataFrame to a new CSV file specified by `--out-file`.

## How to Use the Script

### 1. Ensure You Have the Required Packages Installed:

```bash
pip install pandas numpy scipy click
```

### 2. Save the Script:
Save the script to a file, e.g., `classify_high_risk.py`.

### 3. Prepare Your Z-Score File:
Make sure you have the z-scores calculated and saved in a CSV file (e.g., `z_scores_output.csv`) from your first script. The CSV file should contain at least two columns:
- `sample_id`: Unique identifiers for each individual.
- `z_score`: Calculated z-scores.

### 4. Run the Script:
Open a terminal and navigate to the directory containing the script. Run the script using Python, specifying your z-score file and desired percentile cutoff.

Example Command:
```bash
python classify_high_risk.py \
    --z-score-file z_scores_output.csv \
    --out-file high_risk_output.csv \
    --percentile-cutoff 9
```

Parameters:
- `--z-score-file`: Path to your z-scores CSV file (output from the first script).
- `--out-file`: Path where the output CSV file with high-risk classification will be saved.
- `--percentile-cutoff`: The desired percentile cutoff (e.g., 9 for the top 9%).

### 5. Interpreting the Output:
- The script will print the z-score cutoff corresponding to your specified percentile.
- An output CSV file (e.g., `high_risk_output.csv`) will be generated, containing:
  - `sample_id`: Individual identifiers.
  - `z_score`: Original z-scores.
  - `high_risk`: Boolean flag indicating whether the individual is classified as high risk.

## Example Usage

Suppose you have a z-score file `z_scores_output.csv` that looks like this:

```csv
sample_id,z_score
1,-0.6546536707079774
2,0.9819805060619656
3,0.0
4,2.9445298291028864
5,1.6356631267699425
```

Run the script:

```bash
python classify_high_risk.py \
    --z-score-file z_scores_output.csv \
    --out-file high_risk_output.csv \
    --percentile-cutoff 20
```

Expected Output:

```
The z-score cutoff for the top 20.0% is: 0.8416
High-risk classification has been saved to 'high_risk_output.csv'.
```

Output CSV (`high_risk_output.csv`):

```csv
sample_id,z_score,high_risk
1,-0.6546536707079774,False
2,0.9819805060619656,True
3,0.0,False
4,2.9445298291028864,True
5,1.6356631267699425,True
```

## Adjusting the Percentile Cutoff

To classify individuals in the top 5% as high risk:

```bash
python classify_high_risk.py \
    --z-score-file z_scores_output.csv \
    --out-file high_risk_output.csv \
    --percentile-cutoff 5
```

Output:

```
The z-score cutoff for the top 5.0% is: 1.6449
High-risk classification has been saved to 'high_risk_output.csv'.
```

## Script Explanation

### Calculating the Z-Score Cutoff:
```python
percentile = 1 - (percentile_cutoff / 100.0)
z_cutoff = norm.ppf(percentile)
```
- Converts the top X% cutoff to a cumulative probability.
- Uses `norm.ppf()` from `scipy.stats` to get the z-score corresponding to that cumulative probability.

### Classifying Individuals:
```python
high_risk = z_scores > z_cutoff
z_scores_df['high_risk'] = high_risk
```
- Compares each individual's z-score to the cutoff.
- Adds a `high_risk` column to the DataFrame.

## Error Handling

The script checks if the `z_score` column exists in the input file and raises an error if not:

```python
if 'z_score' not in z_scores_df.columns:
    raise ValueError("The input file must contain a 'z_score' column.")
```

## Additional Notes

- **Assumption of Normality**: This method assumes that the z-scores are normally distributed with a mean of 0 and a standard deviation of 1. Since z-scores are standardized scores, this assumption generally holds.
- **Data Integrity**: Ensure that the z-scores in your input file are correctly calculated and not corrupted.
- **Flexibility**: You can specify any percentile cutoff you desire.
- **Dependencies**: The script uses standard Python libraries and `click` for command-line argument parsing.

## Integration into Workflow

This separate script allows you to modularize your analysis:

1. Run your initial script to calculate z-scores from raw PRS scores, outputting a file like `z_scores_output.csv`.
2. Use this new script to classify individuals based on any desired percentile cutoff.

This separation makes it easy to experiment with different cutoffs without recalculating z-scores each time.
