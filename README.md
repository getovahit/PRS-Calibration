# PRS-Calibration
Ancestry Adjusted PRS Calibration

# PRS Ancestry Calibration Tool

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Data Preparation](#data-preparation)
5. [Usage](#usage)
6. [Output](#output)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [Additional Tips](#additional-tips)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

The PRS Ancestry Calibration Tool is a Python-based implementation of the method described in the paper [insert paper reference here]. This tool calibrates Polygenic Risk Scores (PRS) across different genetic ancestries, adjusting for both the mean and variance of PRS distributions based on principal components (PCs) of genetic ancestry.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package installer)
- Basic knowledge of command-line operations
- Your PRS and PC data in CSV format (see [Data Preparation](#data-preparation) for details)

## Installation

1. **Clone this repository or download the source code:**

   ```bash
   git clone https://github.com/your-username/prs-ancestry-calibration.git
   cd prs-ancestry-calibration
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install click numpy scipy pandas scikit-learn
   ```

## Data Preparation

Your input data should be in CSV format. You need two separate files:

1. **PRS Data File:**
   - Filename: `prs_data.csv`
   - Columns:
     - `sample_id`: Unique identifier for each sample (must match between files)
     - `PRS`: Raw PRS value for each sample (numeric)

   Example:
   ```csv
   sample_id,PRS
   SAMPLE001,0.5
   SAMPLE002,-0.2
   SAMPLE003,1.1
   ```

2. **PC Data File:**
   - Filename: `pc_data.csv`
   - Columns:
     - `sample_id`: Unique identifier for each sample (must match PRS file)
     - `PC1`, `PC2`, ..., `PCn`: Principal component values (numeric)

   Example:
   ```csv
   sample_id,PC1,PC2,PC3,PC4,PC5
   SAMPLE001,0.1,0.2,-0.1,0.05,0.3
   SAMPLE002,-0.2,0.1,0.3,-0.1,0.2
   SAMPLE003,0.3,-0.1,0.2,0.1,-0.2
   ```

**Important Notes:**
- Both files must have a header row.
- The `sample_id` values must match between the two files to ensure correct data alignment.
- There should be no missing values in either file.
- All values in the PRS and PC columns must be numeric (floats or integers).
- The `sample_id` column should not be included in the numeric computations; ensure it is treated as a string identifier.

**Data Alignment and Merging:**
- The order of samples in the two files does not need to be the same; the script will merge the data based on `sample_id`.
- Ensure that your `sample_id` values are unique and consistent across both files.

## Usage

Execute the script by providing the paths to the PRS and PCs data files. You can also optionally modify the output file path (by default, it is saved in the same folder as the running script):

   ```bash
   python prs_ancestry_calibration.py --prs-file=/path/to/prs_data.csv --pc-file=/path/to/pc_data.csv --out-file=z_scores_output.csv
   ```

## Output

The output file `calibrated_prs_results.csv` will contain:

- `sample_id`: The original sample identifier
- `raw_prs`: The original, uncalibrated PRS
- `z_score`: The ancestry-calibrated PRS z-score

## Customization

1. **Number of PCs:**
   To change the number of PCs used for calibration, modify the `n_pcs` variable in the `main` function:

   ```python
   n_pcs = pcs.shape[1]  # Use all PCs provided
   # or set a specific number, e.g.,
   n_pcs = 5  # Use only the first 5 PCs
   ```

2. **Column Names:**
   If your input files have different column names, update the `load_data` function accordingly. For example, if your PRS column is named `PRS_value`, change:

   ```python
   prs = merged_data['PRS_value'].values
   ```

3. **Optimization Method:**
   To use a different optimization method, change the `method` parameter in the `minimize` function call within the `fit` method of the `PRSAncestryCalibration` class.

## Troubleshooting

1. **ValueError: could not convert string to float: 'SAMPLE1'**
   - Cause: The `sample_id` column containing strings is being included in the numeric computations.
   - Solution: Ensure that only numeric columns are included when extracting `prs` and `pcs` values.
   - Modify the `load_data` function to exclude `sample_id` from the numeric data.

2. **Incorrect Method Definitions:**
   - Ensure that special methods like `__init__` are defined with double underscores:
     ```python
     def __init__(self, n_pcs):
         self.n_pcs = n_pcs
         self.params = None
         self.scaler = StandardScaler()
     ```

3. **Script Not Executing Main Function:**
   - Ensure the script ends with the correct `if __name__ == '__main__':` block:
     ```python
     if __name__ == '__main__':
         main()
     ```

4. **ImportError:**
   - Make sure you've installed all required packages:
     ```bash
     pip install numpy scipy pandas scikit-learn
     ```

5. **FileNotFoundError:**
   - Check that the file paths in the `main` function are correct and that the CSV files are in the specified location.

6. **ValueError: Model not fitted. Call fit() first.**
   - Ensure you're calling the `fit` method before `calculate_z_score`.

7. **Data Consistency Errors:**
   - Ensure all PRS and PC values are numeric and that there are no missing (NaN) values.

8. **Memory Issues:**
   - For very large datasets, consider processing data in chunks using `pandas.read_csv` with the `chunksize` parameter.

9. **Convergence Warnings:**
   - If you encounter convergence warnings during optimization, try increasing the maximum number of iterations or using a different optimization method in the `minimize` function.

## Additional Tips

1. **Testing with Sample Data:**
   - Before running the script on your full dataset, test it with a small sample dataset to ensure everything works as expected.

2. **Logging and Debugging:**
   - Add print statements or logging to display intermediate values for debugging purposes.

3. **Exception Handling:**
   - Wrap code blocks in try-except statements to catch and handle exceptions gracefully.

4. **Reproducibility:**
   - Set a random seed at the beginning of your script if reproducibility is important:
     ```python
     np.random.seed(42)
     ```

5. **Data Verification:**
   - Verify that the PC columns are correctly identified and that only numeric data is being processed.

## Contributing

Contributions to improve the tool are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add YourFeature'`)
5. Push to the branch (`git push origin feature/YourFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For any questions or issues not covered in this README, please open an issue on the GitHub repository or contact [your contact information].
