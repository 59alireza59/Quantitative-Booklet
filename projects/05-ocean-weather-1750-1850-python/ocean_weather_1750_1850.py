"""
Quick Exploring Global Ocean Weather Data (1750–1850)
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "ocean-weather" / "CLIWOC15.csv"

OUT_DIR = Path(__file__).resolve().parent / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATA_FILE}")

    data = pd.read_csv(DATA_FILE)
    cols = ["Year", "Rain", "Fog", "Gusts", "Snow", "Thunder", "Hail", "SeaIce"]
    rain_info = data[cols].copy()

    pivot = rain_info.pivot_table(index="Year", aggfunc=np.sum)

    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind="line", ax=ax)
    ax.set_title("Climatological Changes of the Global Oceans (1750–1850)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count / Sum of events")
    ax.locator_params(nbins=10)

    out = OUT_DIR / "Globe_Ocean.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
