import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

MASTER_CSV = os.path.join(DATA_DIR, "master_stocks.csv")
YEARLY_METRICS_CSV = os.path.join(DATA_DIR, "summary_yearly_metrics.csv")
TOP_GAINERS_CSV = os.path.join(DATA_DIR, "top10_gainers.csv")
TOP_LOSERS_CSV = os.path.join(DATA_DIR, "top10_losers.csv")
MONTHLY_GNL_CSV = os.path.join(DATA_DIR, "monthly_gainers_losers.csv")
SECTOR_MAP_CSV = os.path.join(DATA_DIR, "sector_mapping.csv")  # optional

# Load
master = pd.read_csv(MASTER_CSV, parse_dates=["date"])
yearly = pd.read_csv(YEARLY_METRICS_CSV)
top_gainers = pd.read_csv(TOP_GAINERS_CSV)
top_losers = pd.read_csv(TOP_LOSERS_CSV)
monthly_gnl = pd.read_csv(MONTHLY_GNL_CSV)

# 1. Market summary -> text file
latest_year = yearly["year"].max()
latest = yearly[yearly["year"] == latest_year]
market_summary = {
    "year": int(latest_year),
    "num_symbols": int(latest["symbol"].nunique()),
    "green": int((latest["yearly_return"] > 0).sum()),
    "red": int((latest["yearly_return"] <= 0).sum()),
    "avg_close": float(latest["avg_close"].mean()),
    "avg_volume": float(latest["avg_volume"].mean())
}
pd.Series(market_summary).to_csv(os.path.join(DATA_DIR, "market_summary.csv"))

# 2. Top 10 volatile stocks (by volatility) for latest year
vol_latest = latest.sort_values("volatility", ascending=False).head(10)
vol_latest.to_csv(os.path.join(DATA_DIR, "top10_volatile.csv"), index=False)

plt.figure(figsize=(10,6))
plt.bar(vol_latest['symbol'], vol_latest['volatility'])
plt.title(f"Top 10 Volatile Stocks ({latest_year})")
plt.xlabel("Symbol")
plt.ylabel("Volatility (std of daily returns)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "top10_volatile.png"))
plt.close()

# 3. Cumulative return lines for top 5 performing stocks (latest year)
top5 = latest.sort_values("yearly_return", ascending=False).head(5)["symbol"].tolist()
df_top5 = master[master["symbol"].isin(top5)].copy()
# convert date if needed
df_top5['date'] = pd.to_datetime(df_top5['date'])
plt.figure(figsize=(10,6))
for s in top5:
    sub = df_top5[df_top5['symbol']==s].sort_values('date')
    # cumulative already present, but compute relative cumulative per year start:
    sub = sub.copy()
    sub['cum'] = (1 + sub['daily_return']).cumprod() - 1
    plt.plot(sub['date'], sub['cum'], label=s)
plt.legend()
plt.title("Cumulative Returns - Top 5 Stocks")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "cumulative_top5.png"))
plt.close()

# 4. Correlation heatmap (returns) for N largest symbols by data availability
symbols_by_count = master['symbol'].value_counts().head(50).index.tolist()
pivot = master[master['symbol'].isin(symbols_by_count)].pivot_table(
    index='date', columns='symbol', values='daily_return'
)
corr = pivot.corr()
plt.figure(figsize=(12,10))
sns.heatmap(corr, center=0, cmap='coolwarm')
plt.title("Correlation heatmap (daily returns) - top 50 symbols by data count")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "correlation_heatmap.png"))
plt.close()
# save correlation matrix
corr.to_csv(os.path.join(DATA_DIR, "correlation_matrix.csv"))

# 5. Sector-wise performance (if mapping exists)
if os.path.exists(SECTOR_MAP_CSV):
    sectors = pd.read_csv(SECTOR_MAP_CSV)  # columns: symbol, sector
    yearly_sector = yearly.merge(sectors, left_on='symbol', right_on='symbol', how='left')
    sector_agg = yearly_sector.groupby('sector').agg(
        avg_yearly_return=('yearly_return','mean'),
        count=('symbol','count')
    ).reset_index().sort_values('avg_yearly_return', ascending=False)
    sector_agg.to_csv(os.path.join(DATA_DIR, "sector_performance.csv"), index=False)

    plt.figure(figsize=(10,6))
    plt.bar(sector_agg['sector'], sector_agg['avg_yearly_return'])
    plt.xticks(rotation=45, ha="right")
    plt.title("Sector-wise average yearly return")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "sector_performance.png"))
    plt.close()
else:
    print("[INFO] No sector_mapping.csv found — skipping sector charts.")

# 6. Monthly top 5 gainers & losers charts (generate one plot per month)
if not monthly_gnl.empty:
    months = monthly_gnl['month'].unique()
    for m in months:
        sub = monthly_gnl[monthly_gnl['month']==m]
        gainers = sub[sub['type']=='gainer'].sort_values('monthly_return', ascending=False).head(5)
        losers = sub[sub['type']=='loser'].sort_values('monthly_return', ascending=True).head(5)

        plt.figure(figsize=(10,4))
        plt.bar(gainers['symbol'], gainers['monthly_return'])
        plt.title(f"{m} - Top 5 Monthly Gainers")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, f"{m}_gainers.png"))
        plt.close()

        plt.figure(figsize=(10,4))
        plt.bar(losers['symbol'], losers['monthly_return'])
        plt.title(f"{m} - Top 5 Monthly Losers")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, f"{m}_losers.png"))
        plt.close()

print("Analysis & plots saved in:", PLOTS_DIR)
