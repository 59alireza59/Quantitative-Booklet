"""
Canadian Immigration Analysis (1980–2013)

This script reproduces the main plots from the booklet:
- Total immigration trend + best-fit line
- Country-specific bar chart (example: Italy)
- Area chart for top 3 source countries
- Bubble scatter comparison (China vs India)
- Decade aggregation for top 7 countries (barh + boxplot)

Data:
Place the Excel file at:
    data/canadian-immigration/Canada.xlsx
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "canadian-immigration" / "Canada.xlsx"
SHEET_NAME = "Canada by Citizenship"

OUT_DIR = Path(__file__).resolve().parent / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    df = pd.read_excel(
        path,
        sheet_name=SHEET_NAME,
        skiprows=range(20),
        skipfooter=2,
        engine="openpyxl",
    )

    df = df.drop(["AREA", "REG", "DEV", "Type", "Coverage"], axis=1)
    df = df.rename(columns={"OdName": "Country", "AreaName": "Continent", "RegName": "Region"})
    years = list(range(1980, 2014))
    df["Total"] = df[years].sum(axis=1)
    df = df.set_index("Country")
    return df


def plot_total_trend(df: pd.DataFrame) -> None:
    years = list(range(1980, 2014))
    total = pd.DataFrame(df[years].sum()).reset_index()
    total.columns = ["year", "total"]

    ax = total.plot(kind="scatter", x="year", y="total", figsize=(10, 6))
    ax.set_title("Total immigration to Canada (1980–2013)", fontsize=16)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of immigrants")

    points = total["year"]
    fit = np.polyfit(points, total["total"], deg=1)
    ax.plot(points, fit[0] * points + fit[1])
    ax.annotate(f"y={fit[0]:.0f}x + {fit[1]:.0f}", xy=(2000, 150000))

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "01_total_trend.png", dpi=200)
    plt.close(fig)


def plot_country_bar(df: pd.DataFrame, country: str = "Italy") -> None:
    years = list(range(1980, 2014))
    series = df.loc[[country], years].transpose()
    ax = series.plot(kind="bar", figsize=(15, 6))
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of immigrants")
    ax.set_title(f"{country} immigrants to Canada (1980–2013)", fontsize=16)

    ax.annotate(
        "",
        xy=(32, float(series[country].max())),
        xytext=(0, float(series[country].median())),
        xycoords="data",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3", lw=2),
    )

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "02_country_bar_italy.png", dpi=200)
    plt.close(fig)


def plot_top3_area(df: pd.DataFrame) -> None:
    years = list(range(1980, 2014))
    df_sorted = df.sort_values("Total", ascending=False)
    top3 = df_sorted[years].head(3).transpose()

    ax = top3.plot(kind="area", alpha=0.25, figsize=(18, 8))
    ax.set_title("Immigration trend of top 3 countries", fontsize=16)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of immigrants")

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "03_top3_area.png", dpi=200)
    plt.close(fig)


def plot_china_india_bubble(df: pd.DataFrame) -> None:
    years = list(range(1980, 2014))
    chindia = df.loc[["India", "China"], years].transpose().reset_index()
    chindia = chindia.rename(columns={"index": "Year"})

    china_s = (chindia["China"] - chindia["China"].min()) / (chindia["China"].max() - chindia["China"].min())
    india_s = (chindia["India"] - chindia["India"].min()) / (chindia["India"].max() - chindia["India"].min())

    ax0 = chindia.plot(
        kind="scatter", x="Year", y="China",
        figsize=(14, 8), alpha=0.5,
        s=china_s * 2000 + 10, xlim=(1975, 2015)
    )
    ax1 = chindia.plot(
        kind="scatter", x="Year", y="India",
        alpha=0.5, s=india_s * 2000 + 10, ax=ax0
    )

    ax0.set_ylabel("Number of immigrants")
    ax0.set_title("Immigration from China and India (1980–2013)", fontsize=16)
    ax0.legend(["China", "India"], loc="upper left")

    fig = ax1.get_figure()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "04_china_india_bubble.png", dpi=200)
    plt.close(fig)


def plot_top7_by_decade(df: pd.DataFrame) -> None:
    years = list(range(1980, 2014))
    df_sorted = df.sort_values("Total", ascending=False)
    top7 = df_sorted.loc[:, years].head(7)

    years_80s = list(range(1980, 1990))
    years_90s = list(range(1990, 2000))
    years_00s = list(range(2000, 2010))

    d80 = top7.loc[:, years_80s].sum(axis=1)
    d90 = top7.loc[:, years_90s].sum(axis=1)
    d00 = top7.loc[:, years_00s].sum(axis=1)

    decades = pd.DataFrame({"1980s": d80, "1990s": d90, "2000s": d00})

    ax = decades.transpose().plot(kind="barh", figsize=(15, 8))
    ax.set_xlabel("Number of immigrants")
    ax.set_title("Immigration from top 7 countries by decade", fontsize=16)

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "05_top7_decades_barh.png", dpi=200)
    plt.close(fig)

    fig = plt.figure(figsize=(12, 6))
    box = plt.boxplot(decades.transpose(), patch_artist=True)
    colors = ["#c8d5a0", "#922e74", "#b877af"]
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)

    plt.title("Top 7 countries: decade distribution", fontsize=16)
    plt.ylabel("Number of immigrants")
    plt.xlabel("Decade")
    plt.xticks([1, 2, 3], ["1980s", "1990s", "2000s"])
    fig.tight_layout()
    fig.savefig(OUT_DIR / "06_top7_decades_boxplot.png", dpi=200)
    plt.close(fig)


def main() -> None:
    df = load_data(DATA_FILE)
    plot_total_trend(df)
    plot_country_bar(df, "Italy")
    plot_top3_area(df)
    plot_china_india_bubble(df)
    plot_top7_by_decade(df)
    print(f"Done. Figures saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
