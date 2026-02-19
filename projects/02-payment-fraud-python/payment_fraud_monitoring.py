"""
Payment Fraud Monitoring

Reproduces key visuals from the booklet:
- Strip plots over time, amount, and error balance
- 3D scatter in engineered "error" feature space
- Correlation heatmaps for genuine vs fraudulent transactions

Data:
    data/payment-fraud/Synthetic_Financial_Dataset.csv
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "payment-fraud" / "Synthetic_Financial_Dataset.csv"

OUT_DIR = Path(__file__).resolve().parent / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_and_clean(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    df = pd.read_csv(path)
    df = df.rename(
        columns={
            "oldbalanceOrg": "oldBalanceOrig",
            "newbalanceOrig": "newBalanceOrig",
            "oldbalanceDest": "oldBalanceDest",
            "newbalanceDest": "newBalanceDest",
        }
    )

    X = df.loc[(df["type"] == "TRANSFER") | (df["type"] == "CASH_OUT")].copy()
    y = X["isFraud"].copy()
    X = X.drop(["isFraud", "nameOrig", "nameDest", "isFlaggedFraud"], axis=1)

    X.loc[X["type"] == "TRANSFER", "type"] = 0
    X.loc[X["type"] == "CASH_OUT", "type"] = 1
    X["type"] = X["type"].astype(int)

    X.loc[
        (X["oldBalanceDest"] == 0) & (X["newBalanceDest"] == 0) & (X["amount"] != 0),
        ["oldBalanceDest", "newBalanceDest"],
    ] = -1

    X.loc[
        (X["oldBalanceOrig"] == 0) & (X["newBalanceOrig"] == 0) & (X["amount"] != 0),
        ["oldBalanceOrig", "newBalanceOrig"],
    ] = np.nan

    X["errorBalanceOrig"] = X["newBalanceOrig"] + X["amount"] - X["oldBalanceOrig"]
    X["errorBalanceDest"] = X["oldBalanceDest"] + X["amount"] - X["newBalanceDest"]
    return X, y


def plot_strip(x, y, hue, title: str, ylabel: str, out_name: str, figsize=(9, 7)):
    fig = plt.figure(figsize=figsize)
    colours = plt.cm.tab10(np.linspace(0, 1, 9))
    with sns.axes_style("ticks"):
        ax = sns.stripplot(
            x=x, y=y, hue=hue,
            jitter=0.4, marker=".", size=4,
            palette=colours,
        )
        ax.set_xlabel("")
        ax.set_xticklabels(["Genuine", "Fraudulent"], size=12)
        for axis in ["top", "bottom", "left", "right"]:
            ax.spines[axis].set_linewidth(2)
        handles, _ = ax.get_legend_handles_labels()
        plt.legend(handles, ["Transfer", "Cash out"], bbox_to_anchor=(1, 1), loc=2, fontsize=12)

    ax.set_ylabel(ylabel, size=12)
    ax.set_title(title, size=14)
    fig.tight_layout()
    fig.savefig(OUT_DIR / out_name, dpi=200)
    plt.close(fig)


def plot_3d_errors(X: pd.DataFrame, y: pd.Series, out_name: str = "04_3d_errors.png"):
    x = "errorBalanceDest"
    y_axis = "step"
    z = "errorBalanceOrig"
    z_offset = 0.02

    sns.reset_orig()
    fig = plt.figure(figsize=(7, 9))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(X.loc[y == 0, x], X.loc[y == 0, y_axis], -np.log10(X.loc[y == 0, z] + z_offset),
               c="g", marker=".", s=1)
    ax.scatter(X.loc[y == 1, x], X.loc[y == 1, y_axis], -np.log10(X.loc[y == 1, z] + z_offset),
               c="r", marker=".", s=1)

    ax.set_xlabel(x, size=12)
    ax.set_ylabel(f"{y_axis} [hour]", size=12)
    ax.set_zlabel(f"-log10({z})", size=12)
    ax.set_title("Error-based features", size=14)
    ax.grid(True)

    no_fraud_marker = mlines.Line2D([], [], linewidth=0, color="g", marker=".", markersize=10)
    fraud_marker = mlines.Line2D([], [], linewidth=0, color="r", marker=".", markersize=10)
    plt.legend([no_fraud_marker, fraud_marker], ["genuine", "fraudulent"], bbox_to_anchor=(1.2, 0.4), frameon=False)

    fig.tight_layout()
    fig.savefig(OUT_DIR / out_name, dpi=200)
    plt.close(fig)


def plot_correlation_heatmaps(X: pd.DataFrame, y: pd.Series, out_name: str = "05_corr_heatmaps.png"):
    X_fraud = X.loc[y == 1].copy()
    X_non = X.loc[y == 0].copy()

    corr_non = X_non.loc[:, X.columns != "step"].corr()
    mask = np.zeros_like(corr_non)
    mask[np.triu_indices_from(corr_non)] = True

    fig, (ax1, ax2, cbar_ax) = plt.subplots(1, 3, gridspec_kw={"width_ratios": (0.9, 0.9, 0.05)}, figsize=(14, 9))
    cmap = sns.diverging_palette(220, 8, as_cmap=True)

    sns.heatmap(corr_non, ax=ax1, vmin=-1, vmax=1, cmap=cmap, mask=mask, cbar=False, linewidths=0.5)
    ax1.set_title("Genuine\nTransactions", size=14)

    corr_fraud = X_fraud.loc[:, X.columns != "step"].corr()
    sns.heatmap(corr_fraud, ax=ax2, vmin=-1, vmax=1, cmap=cmap, mask=mask, yticklabels=False,
                cbar_ax=cbar_ax, linewidths=0.5,
                cbar_kws={"orientation": "vertical", "ticks": [-1, -0.5, 0, 0.5, 1]})
    ax2.set_title("Fraudulent\nTransactions", size=14)

    fig.tight_layout()
    fig.savefig(OUT_DIR / out_name, dpi=200)
    plt.close(fig)


def main():
    X, y = load_and_clean(DATA_FILE)

    plot_strip(y, X["step"], X["type"], "Striped vs homogenous fingerprints over time", "Time [hour]", "01_strip_time.png")
    plot_strip(y, X["amount"], X["type"], "Same-signed fingerprints over amount", "Amount", "02_strip_amount.png")
    plot_strip(y, -X["errorBalanceDest"], X["type"], "Opposite-polarity fingerprints over the error", "-errorBalanceDest", "03_strip_error.png")

    plot_3d_errors(X, y)
    plot_correlation_heatmaps(X, y)

    print(f"Done. Figures saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
