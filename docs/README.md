# Nassau Candy Distributor — Profitability & Margin Analysis

🔗 Live Dashboard: dataanalytics1234.streamlit.app 
📂 Repository: github.com/VaishnaviH119/nassau-candy-analysis

An end-to-end data analysis project examining product-line profitability and margin performance for a multi-division candy distributor, from raw transactional data to an interactive dashboard.

## Overview

Sales volume alone can hide whether a product is actually profitable. This project analyzes 10,194 order-level records (2024–2025) across 15 products and 3 divisions to identify which products genuinely drive profit, which carry hidden margin risk, and how concentrated the business's profitability really is.


## Key Findings
- Profit concentration: 5 of 15 products (all Wonka Bar chocolate variants) generate 95.1% of total gross profit — a concentration risk well beyond the classic 80/20 rule.
- Margin risk: Kazookles sells in meaningful volume but returns only a 7.7% gross margin — the lowest in the catalog. Lickable Wallpaper shows a similar, less severe pattern (50% margin on high sales volume).
- Division performance: The "Other" division underperforms on margin (37.7%) more than the smaller Sugar division (57.7%) — despite Sugar having far fewer records.
- Margin stability: Overall gross margin has stayed remarkably stable over two years (±0.32 percentage points month to month), indicating consistent pricing discipline.


Full methodology, data quality checks, and findings are documented in the research paper.

## Dashboard

An interactive Streamlit dashboard lets stakeholders explore the findings directly:

Filters: Division, margin threshold slider, product search, date range

Tabs: 1) Product Profitability Overview 
      2) Division Performance 
      3) Cost vs. Margin Diagnostics 
      4) Pareto (Profit Concentration) Analysis
      
Summary statistics: Descriptive statistics (count, mean, std, min/max) for Sales, Units, Cost, and Gross Profit, shown at the end of the dashboard

(Add a dashboard screenshot here)

## Tech Stack

      Analysis: Python, pandas, numpy

      Visualization: matplotlib, seaborn, plotly

      Dashboard: Streamlit

      Environment: Jupyter (VS Code)

## Project Structure
'''text
nassau-candy-analysis/
│
├── app/
│   └── app.py                         # Streamlit dashboard
│
├── data/
│   ├── Nassau_Candy_Distributor.csv   # Raw dataset
│   └── kpi_data.csv                   # Cleaned and KPI-enriched dataset
│
├── notebooks/
│   └── 01_eda.ipynb                   # EDA, data cleaning, KPI engineering & analysis
│
├── docs/
│   ├── Research_Paper.docx            # Detailed project research paper
│   └── Executive_Summary.docx         # Executive-level project summary
│
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
'''

## How to Run

bash
#### Clone the repo

git clone https://github.com/VaishnaviH119/nassau-candy-analysis.git

cd nassau-candy-analysis

### Set up environment

python -m venv venv

venv\Scripts\activate                    # Windows

source venv/bin/activate                 # Mac/Linux

pip install -r requirements.txt


## Run the dashboard
cd app

streamlit run app.py

## Methodology

1) Data cleaning & validation — structural checks, datetime conversion, outlier investigation
2) KPI engineering — Gross Margin, Profit per Unit, Revenue Contribution, Profit Contribution, Margin Volatility
3) Product & division analysis — profitability ranking, cross-division comparison
4) Pareto analysis — profit concentration across the product catalog
5) Cost structure diagnostics — cost-vs-sales deviation to flag repricing candidates
6) Dashboard deployment — interactive Streamlit app for self-service exploration

## Deliverables

Research Paper — full methodology and findings

Executive Summary — condensed findings for non-technical stakeholders

Interactive dashboard (this repo)


## Author

Vaishnavi N. Helwatkar — Data Analysis Project
