# Student Performance Data Cleaning & Visualization Report

## 1. Objective
To clean a student performance dataset, handle missing and duplicate data, inspect unusual values, and visualize patterns in study habits and scores.

## 2. Dataset
- Source: Synthetic sample dataset created for this educational project.
- Original rows: 243
- Columns in raw dataset: 10
- After exact duplicate removal: 240 rows
- The dataset contains study hours, attendance, parent education, internet access, tutoring, and Math/Reading/Writing scores.

## 3. Data Cleaning Performed
1. Counted missing values before cleaning: 40.
2. Detected exact duplicate rows before cleaning: 3; removed them.
3. Converted numeric fields to numeric data types.
4. Replaced impossible values with missing values: attendance outside 0–100%, study hours outside 0–16 per day, and scores outside 0–100.
5. Filled missing numeric values using each column's median.
6. Filled missing categorical values using the mode where required.
7. Checked remaining statistical outliers with the Interquartile Range (IQR) rule. Statistical outliers were reported rather than automatically deleted, because unusual values can sometimes be valid observations.
8. Created Average_Score and Performance_Level fields.

## 4. Results
- Rows in cleaned dataset: 240
- Missing values after cleaning: 0
- Duplicate rows after cleaning: 0
- Average study hours per day: 2.77
- Average attendance: 81.05%
- Study-hours / average-score correlation: 0.59

### Average score by subject
- Math: 58.13
- Reading: 61.60
- Writing: 59.85

### Performance levels
- Average: 116 students
- Good: 105 students
- Excellent: 10 students
- Needs Improvement: 9 students

### IQR outlier counts (after invalid values were corrected)
- Study_Hours_Per_Day: 0
- Attendance_Percent: 1
- Math_Score: 3
- Reading_Score: 4
- Writing_Score: 3

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
