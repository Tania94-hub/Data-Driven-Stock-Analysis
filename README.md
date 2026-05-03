# 📈 Data-Driven Stock Market Analysis

> Comprehensive stock market analysis of **50 NSE-listed companies across 21 sectors** — covering trend, volatility, sector, and correlation analysis with an interactive **Streamlit dashboard** and **Power BI report**.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=flat-square)

---

## 📌 Project Overview

This project performs a **multi-dimensional stock market analysis** on 50 NSE-listed companies spanning 21 industry sectors. Raw stock data stored in YAML format is extracted, preprocessed into structured CSVs, and analyzed across four key dimensions — trend, volatility, sector performance, and inter-stock correlation. Results are visualized through Python charts, an interactive Streamlit dashboard, and a Power BI report.

---

## 🎯 Problem Statement

Stock market data is often stored in unstructured formats and spread across multiple sources. This project builds a full pipeline — from raw YAML extraction to interactive dashboarding — answering key investment questions:
- Which sectors are trending upward vs declining?
- Which stocks show the highest/lowest volatility?
- How correlated are stocks within and across sectors?
- What are the yearly performance metrics for each company?

---

## 📊 Dataset Summary

| Metric | Value |
|--------|-------|
| **Total companies** | 50 NSE-listed stocks |
| **Sectors covered** | 21 |
| **Data format** | Raw YAML → Preprocessed CSV |
| **Analysis types** | Trend, Volatility, Sector, Correlation |
| **Output files** | Per-symbol CSVs + master_stocks.csv |
| **Dashboard** | Streamlit (live) + Power BI (.pbix) |

**Top Sectors Covered:**
`Banking (6)` `Automobiles (6)` `Software (5)` `Energy (4)` `Pharmaceuticals (3)` `Finance (3)` and 15 more

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| PyYAML | Extracting raw YAML stock data |
| Pandas & NumPy | Data preprocessing and analysis |
| Matplotlib & Seaborn | Static chart generation |
| Streamlit | Interactive web dashboard |
| Power BI | Business intelligence report (.pbix) |

---

## 🔍 Project Workflow

```
Raw YAML Data → Extract → Preprocess → Analyse → Visualize → Streamlit App + Power BI
```

### 1. Data Extraction (`extract_yaml.py`)
- Reads raw YAML files for all 50 NSE companies
- Parses stock price data and converts to structured DataFrames
- Saves individual symbol-level CSV files to `output_csv/`

### 2. Preprocessing (`preprocess.py`)
- Cleans and standardizes all extracted CSVs
- Handles missing values and date formatting
- Computes derived metrics (daily returns, moving averages)
- Generates `master_stocks.csv` with all companies combined

### 3. Sector Mapping (`create_sector_mapping.py`)
- Maps all 50 companies to their respective sectors
- Groups companies by industry for sector-level analysis
- References `Sector_data.csv` with 21 unique sector classifications

### 4. Analysis (`analysis.py`)
Four types of analysis performed:

| Analysis | What It Reveals |
|----------|----------------|
| **Trend Analysis** | Price direction and moving averages per stock |
| **Volatility Analysis** | Standard deviation of returns — risk assessment |
| **Sector Analysis** | Average performance by industry sector |
| **Correlation Analysis** | How stocks move in relation to each other |

### 5. Visualization
- 📊 Static charts saved to `plots/` folder
- 🖥️ Interactive Streamlit dashboard for real-time exploration
- 📋 Power BI `.pbix` report for business stakeholders

---

## 💡 Key Insights

- **Banking and Automobile** sectors show the highest trading volumes across 50 companies
- **Software sector** (5 companies) demonstrates the strongest consistent upward trend
- High volatility stocks are concentrated in **Energy and Defence** sectors
- Strong positive correlation found within **FMCG** companies
- **Pharmaceutical** stocks show the most sector-independent price movements

---

## 📁 Project Structure

```
Data-Driven-Stock-Analysis/
│
├── data/
│   ├── raw_yaml/                    # Source YAML files (50 companies)
│   ├── output_csv/                  # Cleaned symbol-level CSVs
│   ├── plots/                       # Generated analysis charts
│   ├── Sector_data.csv              # Sector mapping (50 companies, 21 sectors)
│   ├── summary_yearly_metrics.csv   # Yearly performance summary
│   └── master_stocks.csv            # Combined master dataset
│
├── scripts/
│   ├── extract_yaml.py              # YAML data extraction
│   ├── preprocess.py                # Data cleaning & preprocessing
│   ├── analysis.py                  # Trend, volatility, sector & correlation analysis
│   ├── streamlit_app.py             # Interactive Streamlit dashboard
│   └── create_sector_mapping.py     # Sector classification script
│
├── dashboards/
│   └── powerbi.pbix                 # Power BI dashboard
│
└── README.md
```

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Tania94-hub/Data-Driven-Stock-Analysis.git

# 2. Navigate to the project folder
cd Data-Driven-Stock-Analysis

# 3. Install dependencies
pip install pandas numpy matplotlib seaborn streamlit pyyaml

# 4. Run the full pipeline
python scripts/extract_yaml.py
python scripts/preprocess.py
python scripts/analysis.py

# 5. Launch Streamlit dashboard
streamlit run scripts/streamlit_app.py
```

---

## 📈 Results Summary

```
✅ Companies Analyzed     : 50 NSE-listed stocks
✅ Sectors Covered        : 21
✅ Analysis Types         : Trend, Volatility, Sector, Correlation
✅ Data Format            : YAML → CSV pipeline
✅ Static Visualizations  : Saved to plots/ folder
✅ Interactive Dashboard  : Streamlit web app
✅ BI Report              : Power BI (.pbix)
```

---

## 🙋‍♀️ About the Author

**Tania Banerjee** — Data Analyst with 5+ years of experience at Wipro, skilled in Python, SQL, Power BI, and Business Intelligence.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/tania-banerjee)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Tania94-hub)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:diya1994.banerjee@gmail.com)

---

<p align="center">⭐ If you found this useful, please star the repo! ⭐</p>
<p align="center">Made with ❤️ by Tania Banerjee</p>
