# Student Performance Data Cleaning & Visualization

## Project overview
A beginner-friendly Python project using Pandas and Matplotlib to clean a synthetic student performance dataset and create visualizations.

## Dataset
`data/student_performance_raw.csv` contains synthetic records and intentional data-quality issues for practice. It is not real student data.

## Requirements
- Python 3
- pandas
- matplotlib

## Setup on macOS (VS Code)
1. Open this folder in VS Code.
2. Open Terminal -> New Terminal.
3. Optional: create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
5. Run:
   ```bash
   python3 main.py
   ```

## Outputs
- `data/student_performance_cleaned.csv`
- `charts/average_score_by_subject.png`
- `charts/average_score_distribution.png`
- `charts/study_hours_vs_score.png`
- `charts/performance_level_counts.png`
- `charts/score_boxplot.png`
- `project_report.md`

## Cleaning methods demonstrated
- Missing-value inspection and median/mode imputation
- Duplicate removal
- Numeric type conversion
- Validation of valid ranges
- IQR outlier detection
- Derived average score and performance category
