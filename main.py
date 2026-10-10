"""
Student Performance Data Cleaning & Visualization Project
Run from VS Code with: python3 main.py
The input CSV is synthetic and includes intentional missing values, duplicate rows,
and invalid numeric values for demonstration.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHART_DIR = BASE_DIR / "charts"
RAW_FILE = DATA_DIR / "student_performance_raw.csv"
CLEAN_FILE = DATA_DIR / "student_performance_cleaned.csv"
REPORT_FILE = BASE_DIR / "project_report.md"

NUMERIC_COLUMNS = [
    "Study_Hours_Per_Day", "Attendance_Percent",
    "Math_Score", "Reading_Score", "Writing_Score"
]
SCORE_COLUMNS = ["Math_Score", "Reading_Score", "Writing_Score"]

def main():
    CHART_DIR.mkdir(exist_ok=True)
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}\\n"
            "Make sure data/student_performance_raw.csv exists."
        )

    df = pd.read_csv(RAW_FILE)
    original_rows, original_cols = df.shape
    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    # 1. Remove exact duplicate rows
    df = df.drop_duplicates().copy()

    # 2. Convert numeric columns safely
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Treat impossible values as missing rather than silently accepting them
    df.loc[~df["Attendance_Percent"].between(0, 100), "Attendance_Percent"] = pd.NA
    df.loc[~df["Study_Hours_Per_Day"].between(0, 16), "Study_Hours_Per_Day"] = pd.NA
    for col in SCORE_COLUMNS:
        df.loc[~df[col].between(0, 100), col] = pd.NA

    # 4. Fill missing numeric values with each column's median
    for col in NUMERIC_COLUMNS:
        df[col] = df[col].fillna(df[col].median())

    # 5. Fill missing categorical values with the most frequent category
    categorical_columns = ["Gender", "Parent_Education", "Internet_Access", "Tutoring"]
    for col in categorical_columns:
        if df[col].isna().any():
            mode = df[col].mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else "Unknown"
            df[col] = df[col].fillna(fill_value)

    # 6. Detect remaining statistical outliers with the IQR rule.
    # We report these; we do not automatically delete valid high/low scores.
    outlier_counts = {}
    for col in NUMERIC_COLUMNS:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outlier_counts[col] = int(((df[col] < low) | (df[col] > high)).sum())

    # Add a useful derived field
    df["Average_Score"] = df[SCORE_COLUMNS].mean(axis=1).round(2)
    df["Performance_Level"] = pd.cut(
        df["Average_Score"],
        bins=[-0.01, 39.99, 59.99, 79.99, 100],
        labels=["Needs Improvement", "Average", "Good", "Excellent"]
    ).astype(str)

    # Save cleaned data
    df.to_csv(CLEAN_FILE, index=False)

    # 7. Visualizations
    plt.figure(figsize=(8, 5))
    df[SCORE_COLUMNS].mean().plot(kind="bar")
    plt.title("Average Score by Subject")
    plt.ylabel("Average marks (out of 100)")
    plt.xlabel("Subject")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_score_by_subject.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(df["Average_Score"], bins=12, edgecolor="black")
    plt.title("Distribution of Student Average Scores")
    plt.xlabel("Average score")
    plt.ylabel("Number of students")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_score_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(df["Study_Hours_Per_Day"], df["Average_Score"], alpha=0.7)
    plt.title("Study Hours vs Average Score")
    plt.xlabel("Study hours per day")
    plt.ylabel("Average score")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "study_hours_vs_score.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    df["Performance_Level"].value_counts().reindex(
        ["Needs Improvement", "Average", "Good", "Excellent"], fill_value=0
    ).plot(kind="bar")
    plt.title("Students by Performance Level")
    plt.xlabel("Performance level")
    plt.ylabel("Number of students")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "performance_level_counts.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    df[SCORE_COLUMNS].plot(kind="box", figsize=(8, 5))
    plt.title("Score Spread by Subject")
    plt.ylabel("Marks (out of 100)")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "score_boxplot.png", dpi=150)
    plt.close()

    # 8. Write a report based on the actual run
    final_missing = int(df.isna().sum().sum())
    final_duplicates = int(df.duplicated().sum())
    avg_scores = df[SCORE_COLUMNS].mean().round(2)
    mean_study = df["Study_Hours_Per_Day"].mean()
    mean_attendance = df["Attendance_Percent"].mean()
    corr = df["Study_Hours_Per_Day"].corr(df["Average_Score"])
    levels = df["Performance_Level"].value_counts()

    report = f"""# Student Performance Data Cleaning & Visualization Report

## 1. Objective
To clean a student performance dataset, handle missing and duplicate data, inspect unusual values, and visualize patterns in study habits and scores.

## 2. Dataset
- Source: Synthetic sample dataset created for this educational project.
- Original rows: {original_rows}
- Columns in raw dataset: {original_cols}
- After exact duplicate removal: {len(df)} rows
- The dataset contains study hours, attendance, parent education, internet access, tutoring, and Math/Reading/Writing scores.

## 3. Data Cleaning Performed
1. Counted missing values before cleaning: {missing_before}.
2. Detected exact duplicate rows before cleaning: {duplicates_before}; removed them.
3. Converted numeric fields to numeric data types.
4. Replaced impossible values with missing values: attendance outside 0–100%, study hours outside 0–16 per day, and scores outside 0–100.
5. Filled missing numeric values using each column's median.
6. Filled missing categorical values using the mode where required.
7. Checked remaining statistical outliers with the Interquartile Range (IQR) rule. Statistical outliers were reported rather than automatically deleted, because unusual values can sometimes be valid observations.
8. Created Average_Score and Performance_Level fields.

## 4. Results
- Rows in cleaned dataset: {len(df)}
- Missing values after cleaning: {final_missing}
- Duplicate rows after cleaning: {final_duplicates}
- Average study hours per day: {mean_study:.2f}
- Average attendance: {mean_attendance:.2f}%
- Study-hours / average-score correlation: {corr:.2f}

### Average score by subject
- Math: {avg_scores['Math_Score']:.2f}
- Reading: {avg_scores['Reading_Score']:.2f}
- Writing: {avg_scores['Writing_Score']:.2f}

### Performance levels
{chr(10).join(f"- {level}: {int(count)} students" for level, count in levels.items())}

### IQR outlier counts (after invalid values were corrected)
{chr(10).join(f"- {col}: {count}" for col, count in outlier_counts.items())}

## 5. Visualizations
The `charts/` folder contains:
- `average_score_by_subject.png`
- `average_score_distribution.png`
- `study_hours_vs_score.png`
- `performance_level_counts.png`
- `score_boxplot.png`

## 6. Conclusion
This project demonstrates a repeatable workflow for inspecting raw data, correcting invalid entries, handling missing values, removing duplicate records, identifying statistical outliers, and communicating findings with charts. The correlation describes an association in this synthetic dataset; it does not prove that studying more causes higher scores.

## 7. Limitations
The dataset is synthetic and relatively small. Results should not be generalized to real students. Median/mode imputation can also affect the distribution of values, so imputation choices should be explained in any real-world analysis.
"""
    REPORT_FILE.write_text(report, encoding="utf-8")

    print("\\nPROJECT COMPLETED SUCCESSFULLY")
    print(f"Raw dataset: {RAW_FILE}")
    print(f"Cleaned dataset: {CLEAN_FILE}")
    print(f"Charts saved in: {CHART_DIR}")
    print(f"Report saved to: {REPORT_FILE}")
    print(f"Rows: {original_rows} raw -> {len(df)} cleaned")
    print(f"Missing values: {missing_before} before -> {final_missing} after")
    print(f"Duplicate rows found: {duplicates_before}; remaining: {final_duplicates}")
    print("\\nAverage scores:")
    print(avg_scores.to_string())

if __name__ == "__main__":
    main()
