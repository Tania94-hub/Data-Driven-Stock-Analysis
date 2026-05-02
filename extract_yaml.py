import os
import glob
from collections import defaultdict

import pandas as pd
import yaml


# --------- CONFIG (paths) ---------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw_yaml")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output_csv")
# ----------------------------------


def load_yaml_file(path):
    with open(path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[WARN] Could not parse YAML file: {path} -> {e}")
            return None


def collect_stock_rows():
    """
    This version supports your YAML structure:

    - Ticker: SBIN
      close: 602.95
      date: '2023-10-03 05:30:00'
      high: 604.9
      low: 589.6
      open: 596.6
      volume: 15322196
    """

    symbol_rows = defaultdict(list)

    pattern_yaml = os.path.join(RAW_DATA_DIR, "**", "*.yaml")
    pattern_yml = os.path.join(RAW_DATA_DIR, "**", "*.yml")
    all_files = glob.glob(pattern_yaml, recursive=True) + glob.glob(pattern_yml, recursive=True)

    if not all_files:
        print(f"[ERROR] No YAML files found in: {RAW_DATA_DIR}")
        return symbol_rows

    print(f"[INFO] Found {len(all_files)} YAML files.")

    for file_path in sorted(all_files):
        data = load_yaml_file(file_path)
        if data is None:
            continue

        # Your YAML: Top-level is ALWAYS a list
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue

                symbol = item.get("Ticker") or item.get("symbol") or item.get("ticker")

                if not symbol:
                    continue

                row = {
                    "date": item.get("date"),
                    "symbol": symbol,
                    "open": item.get("open"),
                    "high": item.get("high"),
                    "low": item.get("low"),
                    "close": item.get("close"),
                    "volume": item.get("volume")
                }

                symbol_rows[symbol].append(row)

        else:
            print(f"[WARN] Unexpected YAML structure in file: {file_path}")

    return symbol_rows


def save_symbol_csvs(symbol_rows):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    for symbol, rows in symbol_rows.items():
        df = pd.DataFrame(rows)

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df = df.sort_values("date")

        file_path = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
        df.to_csv(file_path, index=False)
        print(f"[OK] Saved: {file_path} ({len(df)} rows)")


def main():
    print(f"[INFO] Reading YAML files from: {RAW_DATA_DIR}")
    symbol_rows = collect_stock_rows()

    if not symbol_rows:
        print("[ERROR] No stock data collected.")
        return

    print(f"[INFO] Extracted symbols: {len(symbol_rows)}")
    save_symbol_csvs(symbol_rows)
    print("[DONE] YAML → CSV conversion completed.")


if __name__ == "__main__":
    main()
