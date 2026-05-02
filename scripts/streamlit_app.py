# scripts/streamlit_app.py
import os
from typing import Tuple

import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(DATA_DIR, "plots")


# ---------- Helpers ----------
@st.cache_data
def load_csv_safe(name: str) -> pd.DataFrame:
    """
    Safely load a CSV from the data folder.
    Returns an empty DataFrame if the file is missing or unreadable.
    """
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Failed to read {name}: {e}")
        return pd.DataFrame()


def load_market_summary() -> Tuple[bool, pd.DataFrame]:
    """
    Load market_summary.csv and return (ok_flag, dataframe).
    Handles different simple shapes that file might have.
    """
    df = load_csv_safe("market_summary.csv")
    if df.empty:
        return False, df
    # If it's a single-row with two columns like key,value
    if df.shape[1] == 2 and "Unnamed: 0" in df.columns:
        try:
            df = df.set_index(df.columns[0])
        except Exception:
            pass
    return True, df


# ---------- App layout ----------
st.set_page_config(page_title="Data-Driven Stock Analysis", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Top Performers",
        "Volatility",
        "Cumulative Returns",
        "Sectors",
        "Correlation",
        "Monthly",
        "Download Data",
    ],
)

# Load common datasets (cached)
master_df = load_csv_safe("master_stocks.csv")
yearly_df = load_csv_safe("summary_yearly_metrics.csv")
top_gainers_df = load_csv_safe("top10_gainers.csv")
top_losers_df = load_csv_safe("top10_losers.csv")
monthly_df = load_csv_safe("monthly_gainers_losers.csv")
market_ok, market_summary_df = load_market_summary()


# ---------- Pages ----------
if page == "Home":
    st.title("Market Summary")
    if market_ok and not market_summary_df.empty:
        st.subheader("Quick Market Summary")
        st.dataframe(market_summary_df)
    else:
        st.info("market_summary.csv not found. Run analysis.py to generate it.")

    st.markdown("### Top 10 Gainers (latest year)")
    if not top_gainers_df.empty:
        st.dataframe(top_gainers_df)
    else:
        st.write("top10_gainers.csv not found. Run preprocessing.py")

    st.markdown("### Top 10 Losers (latest year)")
    if not top_losers_df.empty:
        st.dataframe(top_losers_df)
    else:
        st.write("top10_losers.csv not found. Run preprocessing.py")


elif page == "Top Performers":
    st.title("Top Performers (Latest Year)")
    if yearly_df.empty:
        st.write("Yearly metrics not found. Run preprocess.py first.")
    else:
        latest_year = int(yearly_df["year"].max())
        st.write(f"Showing yearly metrics for latest year: {latest_year}")
        latest = yearly_df[yearly_df["year"] == latest_year].copy()
        st.dataframe(latest.sort_values("yearly_return", ascending=False).reset_index(drop=True))


elif page == "Volatility":
    st.title("Volatility — Top 10 (Latest Year)")
    vol_df = load_csv_safe("top10_volatile.csv")
    if not vol_df.empty:
        st.dataframe(vol_df)
    else:
        st.info("top10_volatile.csv not found. Run analysis.py to generate it.")

    vol_img = os.path.join(PLOTS_DIR, "top10_volatile.png")
    if os.path.exists(vol_img):
        st.image(vol_img, use_column_width=True)


elif page == "Cumulative Returns":
    st.title("Cumulative Returns — Top 5 (Latest Year)")
    cum_img = os.path.join(PLOTS_DIR, "cumulative_top5.png")
    if os.path.exists(cum_img):
        st.image(cum_img, use_column_width=True)
    else:
        st.info("cumulative_top5.png not found. Run analysis.py to generate it.")


elif page == "Sectors":
    st.title("Sector Performance")
    sector_perf = load_csv_safe("sector_performance.csv")
    if sector_perf.empty:
        st.info(
            "No sector performance data found. Create data/sector_mapping.csv (columns: symbol,sector) and re-run analysis.py"
        )
    else:
        st.dataframe(sector_perf)
    sp_img = os.path.join(PLOTS_DIR, "sector_performance.png")
    if os.path.exists(sp_img):
        st.image(sp_img, use_column_width=True)


elif page == "Correlation":
    st.title("Correlation Heatmap (Daily Returns)")
    corr_img = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
    if os.path.exists(corr_img):
        st.image(corr_img, use_column_width=True)
    else:
        st.info("correlation_heatmap.png not found. Run analysis.py to generate it.")

    if st.checkbox("Show correlation matrix CSV"):
        corr_df = load_csv_safe("correlation_matrix.csv")
        if corr_df.empty:
            st.write("correlation_matrix.csv not found.")
        else:
            st.dataframe(corr_df.round(3))


elif page == "Monthly":
    st.title("Monthly Gainers & Losers")
    if monthly_df.empty:
        st.info("monthly_gainers_losers.csv not found. Run preprocess.py / analysis.py to create it.")
    else:
        months = sorted(monthly_df["month"].unique().tolist(), reverse=True)
        if not months:
            st.write("No monthly data available.")
        else:
            month_choice = st.selectbox("Month", months)
            sub = monthly_df[monthly_df["month"] == month_choice].copy()
            st.subheader(f"Top Gainers — {month_choice}")
            st.dataframe(sub[sub["type"] == "gainer"].sort_values("monthly_return", ascending=False).head(10))
            st.subheader(f"Top Losers — {month_choice}")
            st.dataframe(sub[sub["type"] == "loser"].sort_values("monthly_return", ascending=True).head(10))

            # show plots if available
            g_img = os.path.join(PLOTS_DIR, f"{month_choice}_gainers.png")
            l_img = os.path.join(PLOTS_DIR, f"{month_choice}_losers.png")
            if os.path.exists(g_img):
                st.image(g_img)
            if os.path.exists(l_img):
                st.image(l_img)


elif page == "Download Data":
    st.title("Download data files")
    st.write("Available files in the data/ folder:")
    files = sorted([f for f in os.listdir(DATA_DIR) if f.lower().endswith(".csv")])
    if not files:
        st.write("No CSV files found in data/. Run preprocessing / analysis scripts first.")
    else:
        for fn in files:
            path = os.path.join(DATA_DIR, fn)
            st.write(fn)
            with open(path, "rb") as f:
                st.download_button(label=f"Download {fn}", data=f, file_name=fn)


