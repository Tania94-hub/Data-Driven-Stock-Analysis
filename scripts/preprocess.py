import os
import glob
import numpy as np
import pandas as pd

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "data", "output_csv")
DATA_DIR = os.path.join(BASE_DIR, "data")

MASTER_CSV_PATH = os.path.join(DATA_DIR, "master_stocks.csv")
YEARLY_METRICS_PATH = os.path.join(DATA_DIR, "summary_yearly_metrics.csv")
TOP_GAINERS_PATH = os.path.join(DATA_DIR, "top10_gainers.csv")
TOP_LOSERS_PATH = os.path.join(DATA_DIR, "top10_losers.csv")
MONTHLY_GAINERS_LOSERS_PATH = os.path.join(DATA_DIR, "monthly_gainers_losers.csv")
# -----------------------

def load_all_stock_csvs():
    pattern = os.path.join(CSV_DIR, "*.csv")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No CSV files found in {CSV_DIR}. Run extract_yaml.py first.")

    frames = []
    for path in files:
        symbol = os.path.splitext(os.path.basename(path))[0]
        df = pd.read_csv(path)
        # if date column missing, skip
        if "date" not in df.columns or "close" not in df.columns:
            print(f"[WARN] {symbol}.csv missing 'date' or 'close' -> skipping")
            continue
        df["symbol"] = symbol
        frames.append(df)

    if not frames:
        raise ValueError("No valid CSVs loaded.")
    all_data = pd.concat(frames, ignore_index=True)
    return all_data

def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

    # numeric cast
    for col in ["open","high","low","close","volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["close"])

    # prev_close & daily_return
    df["prev_close"] = df.groupby("symbol")["close"].shift(1)
    df["daily_return"] = (df["close"] - df["prev_close"]) / df["prev_close"]
    df["daily_return"] = df["daily_return"].replace([np.inf, -np.inf], np.nan)

    # cumulative return per symbol (reset starts at first available)
    df["cumulative_return"] = (1 + df["daily_return"]).groupby(df["symbol"]).cumprod() - 1

    # year & month
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df

def compute_yearly_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # first & last close per symbol-year
    fl = df.sort_values("date").groupby(["symbol","year"]).agg(
        first_close=("close","first"),
        last_close=("close","last")
    )
    fl["yearly_return"] = (fl["last_close"] - fl["first_close"]) / fl["first_close"]

    vol = df.groupby(["symbol","year"]).agg(
        volatility=("daily_return","std"),
        avg_close=("close","mean"),
        avg_volume=("volume","mean")
    )

    yearly = fl.join(vol, how="left").reset_index()
    return yearly

def compute_top_gainers_losers(yearly: pd.DataFrame):
    latest_year = yearly["year"].max()
    latest = yearly[yearly["year"] == latest_year].copy()
    top_gainers = latest.sort_values("yearly_return", ascending=False).head(10)
    top_losers = latest.sort_values("yearly_return", ascending=True).head(10)
    top_gainers.to_csv(TOP_GAINERS_PATH, index=False)
    top_losers.to_csv(TOP_LOSERS_PATH, index=False)
    print(f"[OK] Top gainers/losers saved: {TOP_GAINERS_PATH}, {TOP_LOSERS_PATH}")
    return top_gainers, top_losers

def compute_monthly_gainers_losers(df: pd.DataFrame):
    mg = df.sort_values("date").groupby(["symbol","month"]).agg(
        first_close=("close","first"),
        last_close=("close","last")
    ).reset_index()
    mg["monthly_return"] = (mg["last_close"] - mg["first_close"]) / mg["first_close"]

    rows = []
    for m, sub in mg.groupby("month"):
        top = sub.sort_values("monthly_return", ascending=False).head(5)
        top["type"] = "gainer"
        low = sub.sort_values("monthly_return", ascending=True).head(5)
        low["type"] = "loser"
        rows.append(top); rows.append(low)
    if rows:
        month_result = pd.concat(rows, ignore_index=True)
    else:
        month_result = pd.DataFrame()
    month_result.to_csv(MONTHLY_GAINERS_LOSERS_PATH, index=False)
    print(f"[OK] Monthly gainers/losers saved: {MONTHLY_GAINERS_LOSERS_PATH}")
    return month_result

def main():
    print(f"[INFO] Loading CSV files from {CSV_DIR}")
    df = load_all_stock_csvs()
    print(f"[INFO] Loaded {len(df)} rows from CSVs")
    df = clean_and_enrich(df)
    print(f"[INFO] After cleaning: {len(df)} rows")

    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(MASTER_CSV_PATH, index=False)
    print(f"[OK] Master saved: {MASTER_CSV_PATH}")

    yearly = compute_yearly_metrics(df)
    yearly.to_csv(YEARLY_METRICS_PATH, index=False)
    print(f"[OK] Yearly metrics saved: {YEARLY_METRICS_PATH}")

    compute_top_gainers_losers(yearly)
    compute_monthly_gainers_losers(df)

    print("[DONE] Preprocessing complete.")

if __name__ == "__main__":
    main()
