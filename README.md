# PRS-Calibration
Ancestry Adjusted PRS calibration
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
9. [Contributing](#contributing)
10. [License](#license)

## Introduction

The PRS Ancestry Calibration Tool is a Python-based implementation of the method described in the paper [insert paper reference here]. This tool calibrates Polygenic Risk Scores (PRS) across different genetic ancestries, adjusting for both the mean and variance of PRS distributions based on principal components (PCs) of genetic ancestry.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package installer)
- Basic knowledge of command-line operations
- Your PRS and PC data in CSV format (see [Data Preparation](#data-preparation) for details)

## Installation

1. Clone this repository or download the source code:
   ```
   git clone https://github.com/your-username/prs-ancestry-calibration.git
   cd prs-ancestry-calibration
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install numpy scipy pandas scikit-learn
   ```

## Data Preparation

Your input data should be in CSV format. You need two separate files:

1. PRS Data File:
   - Filename: `prs_data.csv`
   - Columns:
     - `sample_id`: Unique identifier for each sample
     - `PRS`: Raw PRS value for each sample

   Example:
   ```
   sample_id,PRS
   SAMPLE001,0.5
   SAMPLE002,-0.2
   SAMPLE003,1.1
   ```

2. PC Data File:
   - Filename: `pc_data.csv`
   - Columns:
     - `sample_id`: Unique identifier for each sample (must match PRS file)
     - `PC1`, `PC2`, ..., `PCn`: Principal component values

   Example:
   ```
   sample_id,PC1,PC2,PC3,PC4,PC5
   SAMPLE001,0.1,0.2,-0.1,0.05,0.3
   SAMPLE002,-0.2,0.1,0.3,-0.1,0.2
   SAMPLE003,0.3,-0.1,0.2,0.1,-0.2
   ```

Ensure that:
- Both files have a header row
- The `sample_id` values match between the two files
- There are no missing values
- The order of samples doesn't need to be the same in both files, but all samples in the PRS file should have corresponding entries in the PC file

## Usage

1. Place your prepared `prs_data.csv` and `pc_data.csv` files in the same directory as the script.

2. Open the `prs_ancestry_calibration.py` file and update the file paths in the `main` function:

   ```python
   prs_file = 'path/to/your/prs_data.csv'
   pc_file = 'path/to/your/pc_data.csv'
   ```

3. Run the script:
   ```
   python prs_ancestry_calibration.py
   ```

4. The script will process your data and output the results to `calibrated_prs_results.csv` in the same directory.

## Output

The output file `calibrated_prs_results.csv` will contain:

- `sample_id`: The original sample identifier
- `raw_prs`: The original, uncalibrated PRS
- `calibrated_z_score`: The ancestry-calibrated PRS z-score

## Customization

- To change the number of PCs used for calibration, modify the `n_pcs` variable in the `main` function.
- If your input files have different column names, update the `load_data` function accordingly.
- To use a different optimization method, change the `method` parameter in the `minimize` function call within the `fit` method of the `PRSAncestryCalibration` class.

## Troubleshooting

1. **ImportError**: Make sure you've installed all required packages (`numpy`, `scipy`, `pandas`, `scikit-learn`).

2. **FileNotFoundError**: Check that the file paths in the `main` function are correct and the CSV files are in the specified location.

3. **ValueError: Model not fitted**: Ensure you're calling `fit` before `calculate_z_score`.

4. **Memory Issues**: For very large datasets, you may need to process the data in batches. Consider modifying the script to read and process data in chunks using `pandas.read_csv` with the `chunksize` parameter.

5. **Convergence Warnings**: If you see warnings about convergence, try increasing the maximum number of iterations in the `minimize` function or use a different optimization method.

## Contributing

Contributions to improve the tool are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For any questions or issues not covered in this README, please open an issue on the GitHub repository or contact [your contact information].
