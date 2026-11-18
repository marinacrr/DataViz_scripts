'''
Create a single plot to showcase MaX codes citation trend over time.
For each code, citations have been renormalized to the max value.
'''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from pypalettes import load_cmap
import numpy as np
import sys

# Extremes for annotation
extremes = {
    "QE": ("0", "3043"),
    "YAMBO": ("0", "119"),
    "SIESTA": ("23", "751"),
    "FLEUR": ("0", "6"),
    "BigDFT": ("0", "24"),
}

max_cits = {
    "QE": "3476",
    "YAMBO": "144",
    "SIESTA": "934",
    "FLEUR": "9",
    "BigDFT": "41",
}

path = "/home/jeanne/Desktop/Dataviz/images"

c = "Lively"  # "EdwardHopper"  #"Antique" Moreau
colors = load_cmap(c).colors

style_other = dict(color="grey", alpha=0.4, linewidth=0.6)
style_code = dict(ha="center", va="center", fontsize=8, weight="bold")
style_grid = dict(color="gray", lw=0.2, linestyle="dashed")
style_extremes = dict(ha="center", va="center", fontsize=6, weight="bold")

# Load data from Google Sheet
sheet_id = "1c7-F5h6zkg2YfET8vISMCT9Dz5Gr4h121obIF2IpSmI"
gid = "2098494709"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Download CSV data
response = requests.get(url)
response.raise_for_status()

# Parse CSV into a DataFrame
data = pd.read_csv(StringIO(response.text))

# Convert all columns to numeric values
data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
max_codes = data.columns.drop("Year")
data[max_codes] = data[max_codes].apply(pd.to_numeric, errors="coerce")

# Remove infinite values
data = data.replace([np.inf, -np.inf], np.nan)
years = data["Year"]

# Create a single plot
fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")

for color, code in zip(colors, max_codes):

    series = data[code]

    # Plot all citation trends
    ax.plot(years, series, color=color, alpha=0.8,
            linewidth=1.4, marker="o", markersize=4,
            label=code)

    # Find year of maximum citations
    valid = series.notna() & years.notna()

    if valid.any():
        valid_series = series[valid]
        idx = valid_series[::-1].idxmax()

        max_value = data.loc[idx, code]
        max_year = data.loc[idx, "Year"]


# Styling
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.6)

ax.grid(axis="both", **style_grid)
ax.set_yticks([])
ax.set_ylim(-0.05, 1.14)

ax.tick_params(axis="x", labelsize=8)

ax.legend(frameon=False, fontsize=8, ncol=5)

plt.savefig("%s/2026_max_cits_lollipops_all.png" % path, bbox_inches="tight", dpi=150)
