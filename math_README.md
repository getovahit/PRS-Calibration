# Polygenic Risk Score (PRS) Z-Score Calculation

This project implements a method to calculate ancestry-adjusted z-scores for polygenic risk scores (PRS), accounting for population structure using principal components (PCs). The goal is to derive z-scores that reflect deviations in PRS from the population mean, adjusted for ancestral background.

## Mathematical Background

### Z-Score Calculation

Z-scores are a measure of how many standard deviations an element is from the mean. The formula for a basic z-score is:

$$
z = \frac{\text{PRS} - \mu}{\sigma}
$$

Where:
- $\text{PRS}$ is the polygenic risk score for an individual.
- $\mu$ is the mean PRS of the population.
- $\sigma$ is the standard deviation of the PRS in the population.

However, for genetic data, population stratification can lead to biased PRS calculations if ancestral background is not considered. To adjust for this, we use principal components (PCs) that represent population structure.

### Adjusting for Ancestry Using Principal Components (PCs)

In this method, the mean ($\mu$) and standard deviation ($\sigma$) of the PRS are modeled as functions of the principal components:

$$
\mu = \alpha_0 + \sum_{i=1}^{n_{\text{PCs}}} \alpha_i \cdot \text{PC}_i
$$

$$
\sigma = \exp(\eta_0 + \sum_{i=1}^{n_{\text{PCs}}} \eta_i \cdot \text{PC}_i)
$$

Where:
- $\alpha_0$ and $\eta_0$ are intercept terms.
- $\alpha_i$ and $\eta_i$ are coefficients for the PCs.
- $\text{PC}_i$ are the principal components for each individual, which capture ancestry-related variation.

#### Negative Log-Likelihood (NLL)

The parameters $\alpha$ and $\eta$ are estimated by minimizing the negative log-likelihood of the PRS data given the PCs:

$$
\text{NLL} = \sum \left( \log(\sigma) + 0.5 \cdot \left(\frac{\text{PRS} - \mu}{\sigma}\right)^2 \right)
$$

This ensures that the model provides the best fit for the PRS values, accounting for ancestry.

### Fitting the Model

The `fit()` method uses the `scipy.optimize.minimize` function to estimate the parameters $\alpha$ and $\eta$ by minimizing the NLL. This provides the best ancestry-adjusted estimates of the mean and standard deviation of PRS.

### Z-Score Calculation

Once the model is fitted, we calculate z-scores for individuals as:

$$
z = \frac{\text{PRS} - \mu}{\sigma}
$$

Where $\mu$ and $\sigma$ are ancestry-adjusted based on the PCs.

### Standardization of Z-Scores

By default, the calculated z-scores are adjusted for population structure. If desired, the z-scores can be further standardized to have a global mean of 0 and standard deviation of 1 across the entire dataset:

$$
z_{\text{standardized}} = \frac{z - \text{mean}(z)}{\text{std}(z)}
$$

This step ensures the z-scores follow a standard normal distribution.

## Code Overview

The project contains the following main components:

### PRSAncestryCalibration Class

This class handles the calibration of PRS using principal components and the calculation of z-scores.

- **`fit(prs, pcs)`**: Fits the model by estimating the parameters $\alpha$ and $\eta$ using the provided PRS values and PCs.
- **`calculate_z_score(prs, pcs)`**: After fitting the model, calculates the z-scores for the provided PRS values and PCs.

### Load Data

The `load_data()` function loads the PRS and PC data from CSV files, merges them, and extracts the necessary columns.

### Main Function

The script can be run from the command line using Click. It fits the model to the PRS and PC data and outputs the z-scores.

```bash
python main.py --prs-file <path_to_prs_file> --pc-file <path_to_pc_file> --out-file <path_to_output_file>
```

## Example

Assume we have two CSV files, one containing PRS data (`prs_data.csv`) and another containing principal components (`pc_data.csv`). The data should be structured as follows:

### PRS Data (`prs_data.csv`)

| sample_id | PRS    |
|-----------|--------|
| id1       | 1.2345 |
| id2       | 0.9876 |
| ...       | ...    |

### PC Data (`pc_data.csv`)

| sample_id | PC1    | PC2    | PC3    | ... |
|-----------|--------|--------|--------|-----|
| id1       | 0.0123 | 0.0345 | 0.0567 | ... |
| id2       | -0.0234| 0.0678 | 0.0890 | ... |
| ...       | ...    | ...    | ...    | ... |

Running the script:

```bash
python main.py --prs-file prs_data.csv --pc-file pc_data.csv --out-file z_scores_output.csv
```

## Dependencies

- Python 3.8+
- Required packages: `click`, `numpy`, `pandas`, `scipy`, `sklearn`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Output

The output will be a CSV file containing the sample IDs and their corresponding z-scores:

| sample_id | z_score |
|-----------|---------|
| id1       | 1.23    |
| id2       | -0.98   |
| ...       | ...     |

## Determining Percentile from Z-Score

To determine what percentage of the population has a z-score below or above a specific value, such as 1.3, we can use the **cumulative distribution function (CDF)** of the standard normal distribution.

### General Overview of Z-Scores and CDF:

A **z-score** represents how many standard deviations a particular value is away from the mean. The mean of a standard normal distribution is 0, and its standard deviation is 1. The **CDF** provides the probability that a standard normal variable is less than or equal to a given z-score.

The **CDF** value for a specific z-score `z` represents the proportion of the population that falls below that z-score. To find the proportion above a z-score, you subtract the CDF from 1.

Mathematically:
- CDF(z) = Probability of z-score ≤ z
- 1 - CDF(z) = Probability of z-score > z

### Example for z = 1.3:

Let's say we have a z-score of **1.3**:
- Using a standard normal distribution, the **CDF(1.3)** ≈ **0.9032**.
- This means that about **90.32%** of the population has a z-score below **1.3**.
- To find the proportion of the population above this z-score, you subtract it from 1:
  
  $$
  1 - CDF(1.3) = 1 - 0.9032 = 0.0968
  $$
  
  So, **9.68%** of the population has a z-score above 1.3.

### General Formula for Any Z-Score:

For any z-score, you can calculate the proportion of the population that has a z-score below or above it using the same method:
1. Find the **CDF(z)** for the z-score value using a standard normal distribution.
2. To get the proportion of individuals above the z-score, calculate **1 - CDF(z)**.

#### Using Python to Calculate Percentiles for Any Z-Score:

In Python, you can use the `scipy.stats.norm.cdf()` function to get the CDF value for any z-score. Here's an example:

```python
from scipy.stats import norm

z = 1.3  # Example z-score
cdf_value = norm.cdf(z)

percent_below = cdf_value * 100  # Percentage of individuals below this z-score
percent_above = (1 - cdf_value) * 100  # Percentage of individuals above this z-score

print(f"For a z-score of {z}, {percent_below:.2f}% of the population falls below this value.")
print(f"For a z-score of {z}, {percent_above:.2f}% of the population falls above this value.")
```

### Summary:

- The **CDF** allows us to determine the proportion of the population that falls below a given z-score.
- The complement **(1 - CDF)** gives the proportion of the population that falls above that z-score.
- This method is applicable to any z-score, allowing you to quantify an individual's relative position within the population.
