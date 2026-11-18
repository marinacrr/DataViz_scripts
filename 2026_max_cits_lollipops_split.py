'''
Create a multiple axis figure to showcase MaX codes citation trend over time.
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
    "QE": ("0", "3k"),
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
style_grid = dict(color="gray", lw=0.1, linestyle="dashed")
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

fig, axs = plt.subplots(ncols=2, nrows=3, figsize=(8, 6), layout="constrained")

for color, code, ax in zip(colors, max_codes, axs.flat):

    # year of maximum citations
    idx = data[code].idxmax()
    max_value = data.loc[idx, code]
    max_year = data.loc[idx, "Year"]

    # plot all codes on background
    other_codes = max_codes.drop(code)
    ax.plot(years, data[other_codes], **style_other)

    # highlight current code
    ax.scatter(years, data[code], s=10, color=color, alpha=0.8)
    ax.bar(years, data[code], width=0.1, color=color, alpha=0.6)
    ax.text(0.1, 0.95, code, transform=ax.transAxes, color=color, **style_code)

    # Annotate extremes
    series = data[code]

    valid = series.notna() & years.notna()
    valid_idx = data.index[valid]

    if len(valid_idx) > 0:
        first_idx = valid_idx[0]
        last_idx = valid_idx[-1]

        # Last available year
        ax.text(
            years.loc[last_idx],
            series.loc[last_idx] + 0.1,
            str(extremes[code][0]),
            color=color,
            **style_extremes
        )

        # year of maximum citations
        ax.text(max_year, max_value + 0.1, s=max_cits[code],
            color=color,
            **style_extremes
        )

        # First available year
        ax.text(
            years.loc[first_idx],
            series.loc[first_idx] + 0.1,
            str(extremes[code][1]),
            color=color,
            **style_extremes
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("black")
    ax.spines["bottom"].set_linewidth(0.5)

    ax.grid(axis="both", **style_grid)

    ax.set_yticks([])
    ax.set_ylabel("")
    #ax.set_xlim(2014, 2027)
    #ax.set_xticks(range(2015, 2027))
    ax.set_ylim(-0.05, 1.14)
    ax.tick_params(axis="x", labelsize=4)

# Remove unused subplot
for ax in axs.flat[len(max_codes):]:
    ax.remove()

plt.savefig("%s/2026_max_cits_lollipops_split.png" %path, bbox_inches='tight', dpi=150)
