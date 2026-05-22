import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams.update({
    "font.family":      "serif",
    "font.serif":       ["Georgia", "Times New Roman", "DejaVu Serif"],
    "figure.facecolor": "#0d0d0d",
    "axes.facecolor":   "#0d0d0d",
    "text.color":       "#e8e0d0",
    "axes.labelcolor":  "#e8e0d0",
    "xtick.color":      "#9a9080",
    "ytick.color":      "#9a9080",
    "axes.edgecolor":   "#3a3530",
    "grid.color":       "#2a2520",
    "grid.linewidth":   0.6,
})

a        = 1.0
n_vals   = np.linspace(1, 15, 300)
bc_vals  = np.linspace(0.5, 10, 300)
N, BC    = np.meshgrid(n_vals, bc_vals)

CS_cournot   = (N**2 * BC**2) / (2 * a * (N + 1)**2)
CS_collusion = BC**2 / (8 * a)
delta_CS     = CS_cournot - CS_collusion

cmap = LinearSegmentedColormap.from_list(
    "econ",
    ["#1a1060", "#3d2b8a", "#8b4513", "#c8860a", "#e8c840", "#f5f0dc"],
    N=512
)

fig = plt.figure(figsize=(14, 9), dpi=300)
ax  = fig.add_subplot(111, projection="3d")
ax.set_facecolor("#0d0d0d")

surf = ax.plot_surface(
    N, BC, delta_CS,
    cmap=cmap,
    linewidth=0,
    antialiased=True,
    alpha=0.95,
    rcount=200,
    ccount=200,
)

cbar = fig.colorbar(surf, ax=ax, shrink=0.45, aspect=12, pad=0.02)
cbar.set_label(r"$\Delta CS$", fontsize=12, labelpad=10, color="#e8e0d0")
cbar.ax.yaxis.set_tick_params(color="#9a9080")
plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#9a9080", fontsize=9)
cbar.outline.set_edgecolor("#3a3530")

ax.set_xlabel(r"$n$  (number of firms)",
              fontsize=12, labelpad=14, color="#c8b898")
ax.set_ylabel(r"$b - c$  (demand–cost spread)",
              fontsize=12, labelpad=14, color="#c8b898")
ax.set_zlabel(r"$\Delta CS$",
              fontsize=12, labelpad=10, color="#c8b898")

ax.set_title(
    "Consumer Welfare Gain from Cartel Breakdown\n"
    r"$\Delta CS = \dfrac{n^{2}(b-c)^{2}}{2a(n+1)^{2}} - \dfrac{(b-c)^{2}}{8a}$",
    fontsize=13, color="#e8e0d0", pad=22, linespacing=1.8
)

ax.set_xlim(1, 15)

ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
ax.tick_params(axis="both", labelsize=9)

for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
    pane.fill = False
    pane.set_edgecolor("#2a2520")

ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.4)

# Looking along the b-c axis, forward into the n direction
ax.view_init(elev=22, azim=10)

fig.text(0.13, 0.03,
         r"Parameters: $a = 1$,  $n \in [1,\,15]$,  $b-c \in [0.5,\,10]$",
         fontsize=9, color="#6a6058", style="italic")

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/delta_cs_surface_v4.png",
            dpi=300, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved.")