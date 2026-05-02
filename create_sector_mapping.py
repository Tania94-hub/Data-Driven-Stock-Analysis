# scripts/create_sector_mapping.py
import os
import pandas as pd

base = os.getcwd()
data_dir = os.path.join(base, "data")
path1 = os.path.join(data_dir, "summary_yearly_metrics.csv")
path2 = os.path.join(data_dir, "master_stocks.csv")

# load symbols
if os.path.exists(path1):
    df = pd.read_csv(path1)
elif os.path.exists(path2):
    df = pd.read_csv(path2)
else:
    raise SystemExit("summary_yearly_metrics.csv or master_stocks.csv not found in data/")

symbols = sorted(df['symbol'].unique())

# best-effort mapping (extend as needed)
known = {
    "RELIANCE":"Energy","TCS":"IT","INFY":"IT","HDFCBANK":"Banking","HDFC":"Financials",
    "ICICIBANK":"Banking","SBIN":"Banking","AXISBANK":"Banking","LT":"Engineering",
    "ITC":"FMCG","HINDUNILVR":"FMCG","MARUTI":"Auto","TATAMOTORS":"Auto",
    "BHARTIARTL":"Telecom","JSWSTEEL":"Metals","BAJFINANCE":"Financials","KOTAKBANK":"Banking",
    "SUNPHARMA":"Pharma","DRREDDY":"Pharma","HCLTECH":"IT","WIPRO":"IT","ONGC":"Energy",
    "BPCL":"Energy","GAIL":"Energy","ADANIENT":"Energy","POWERGRID":"Utilities",
    "ULTRACEMCO":"Cement","TITAN":"Consumer","NESTLEIND":"FMCG","ASHOKLEY":"Auto",
    "COALINDIA":"Energy","EICHERMOT":"Auto","SBILIFE":"Insurance"
}

rows = []
for s in symbols:
    rows.append({"symbol": s, "sector": known.get(s, "")})

out = pd.DataFrame(rows)
out_path = os.path.join(data_dir, "sector_mapping.csv")
out.to_csv(out_path, index=False)
print("Created", out_path)
print("Open the file and edit sectors for any blank/incorrect entries.")
