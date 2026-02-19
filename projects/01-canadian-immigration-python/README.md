# Canadian Immigration Analysis (1980–2013) — Python

This booklet visualizes immigration patterns to Canada using the commonly shared IBM / Kaggle “Canada.xlsx” dataset.

## What it does
- Total immigration trend (1980–2013) + best-fit line
- Country bar chart example (Italy)
- Area chart for top-3 source countries
- Bubble scatter comparison (China vs India)
- Decade aggregation for top-7 countries (barh + boxplot)

## Data
Put the Excel dataset here:
`data/canadian-immigration/Canada.xlsx`

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python canadian_immigration_analysis.py
