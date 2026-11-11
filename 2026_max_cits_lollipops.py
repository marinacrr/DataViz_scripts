'''
Create a multiple axis figure to showcase MaX codes citation trend over time.
For each code, citations have been renormalized to the max value.
'''

import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from pypalettes import load_cmap
import sys

# Extremes for annotation
extremes = {
    "QE": ("5k", "32k"),
    "SIESTA": ("7k", "16k"),
    "YAMBO": ("0.2k", "1.4k"),
    "BigDFT": ("0.1k", "0.5k"),
    "FLEUR": (0, "0.03k")
}

path = "/home/jeanne/Desktop/Dataviz/images"

c = "Antique"
colors = load_cmap(c).colors

style_other = dict(color="grey", alpha=0.4, linewidth=0.6)
style_code = dict(ha="center", va="center", fontsize=8, weight="bold")
style_grid = dict(color="gray", lw=0.1, linestyle="dashed")
style_extremes = dict(ha="center", va="center", fontsize=6, weight="bold")

# Load data from Google Sheet
sheet_id = "1c7-F5h6zkg2YfET8vISMCT9Dz5Gr4h121obIF2IpSmI"
gid = "1463414175"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Download CSV data
response = requests.get(url)
response.raise_for_status()

# Parse CSV into a DataFrame
data = pd.read_csv(StringIO(response.text))

years = data["Year"]
max_codes = data.columns.drop("Year")

fig, axs = plt.subplots(ncols=2, nrows=3, layout="tight")

for color, code, ax in zip(colors, max_codes, axs.flat):

    # plot all codes on background
    other_codes = max_codes.drop(code)
    ax.plot(years, data[other_codes], **style_other)

    # highlight current code
    ax.scatter(years, data[code], s=10, color=color, alpha=0.8)
    ax.bar(years, data[code], width=0.1, color=color, alpha=0.6)
    ax.text(0.1, 0.95, code, transform=ax.transAxes, color=color, **style_code)

    # Annotate extremes
    series = data[code]
    first_idx = series.first_valid_index()
    last_idx  = series.last_valid_index()

    if last_idx is not None:
        ax.text(
            data.loc[last_idx, "Year"],
            series.loc[last_idx]+0.1,
            str(extremes[code][0]),
            color=color,
            **style_extremes
        )

    if first_idx is not None:
        ax.text(
            data.loc[first_idx, "Year"],
            series.loc[first_idx]+0.1,
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
    ax.set_xlim(2014, 2027)
    ax.set_xticks(range(2015, 2027))
    ax.set_ylim(-0.05, 1.14)
    ax.tick_params(axis="x", labelsize=4)

# Remove unused subplot
for ax in axs.flat[len(max_codes):]:
    ax.remove()

plt.savefig("%s/2026_max_cits_lollipops.png" %path, bbox_inches='tight', dpi=150)