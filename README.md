# Data-Driven Stock Analysis

## 📌 Project Overview
This project performs end-to-end data processing and visualization of stock market data provided in YAML format.

It includes:
- Extraction of daily stock data from YAML files  
- Data cleaning & preprocessing  
- Calculation of financial metrics (daily return, yearly return, volatility, etc.)  
- Generation of analytical plots  
- Sector-wise performance analysis  
- Interactive Streamlit dashboard  

---

## 📂 Folder Structure
Data-Driven-Stock-Analysis/
├── data/
│ ├── raw_yaml/ # Original YAML files
│ ├── master_stocks.csv
│ ├── summary_yearly_metrics.csv
│ ├── sector_mapping.csv
│ ├── top10_gainers.csv
│ ├── top10_losers.csv
│ ├── monthly_gainers_losers.csv
│ ├── correlation_matrix.csv
│ └── plots/
│ ├── sector_performance.png
│ ├── correlation_heatmap.png
│ ├── cumulative_top5.png
│ ├── top10_volatile.png
│ └── monthly charts...
├── scripts/
│ ├── extract_yaml.py
│ ├── preprocess.py
│ ├── analysis.py
│ ├── streamlit_app.py
│ ├── create_sector_mapping.py
│ └── database_upload.py
├── README.md
└── requirements.txt
