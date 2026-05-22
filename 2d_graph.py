import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family":      "serif",
    "font.serif":       ["Georgia", "Times New Roman", "DejaVu Serif"],
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "text.color":       "#1a1a1a",
    "axes.labelcolor":  "#1a1a1a",
    "xtick.color":      "#444444",
    "ytick.color":      "#444444",
    "axes.edgecolor":   "#cccccc",
    "grid.color":       "#e8e8e8",
    "grid.linewidth":   0.6,
})

a    = 1.0
n    = 4
bc   = np.linspace(0, 50, 500)

CS_cournot   = (n**2 * bc**2) / (2 * a * (n + 1)**2)
CS_collusion = bc**2 / (8 * a)
delta_CS     = CS_cournot - CS_collusion

fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

ax.fill_between(bc, delta_CS, alpha=0.08, color="#c8860a")

ax.plot(bc, delta_CS,     color="#c8860a", linewidth=2.5, label=r"$\Delta CS$")
ax.plot(bc, CS_cournot,   color="#2166ac", linewidth=1.6, linestyle="--",
        alpha=0.85, label=r"$CS_{\mathrm{Cournot}}$")
ax.plot(bc, CS_collusion, color="#d6191b", linewidth=1.6, linestyle="--",
        alpha=0.85, label=r"$CS_{\mathrm{collusion}}$")

ax.set_xlabel(r"$b - c$  (demand–cost spread)", fontsize=13, labelpad=10)
ax.set_ylabel(r"Consumer Surplus", fontsize=13, labelpad=10)
ax.set_title(
    r"Consumer Surplus vs. Demand–Cost Spread  ($n = 4$,  $a = 1$)",
    fontsize=14, color="#1a1a1a", pad=16
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#cccccc")
ax.spines["bottom"].set_color("#cccccc")

ax.legend(fontsize=11, framealpha=0, labelcolor="#1a1a1a")
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

fig.text(0.13, 0.01,
         r"Parameters: $n = 4$,  $a = 1$,  $b-c \in [0,\,50]$",
         fontsize=9, color="#888888", style="italic")

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/delta_cs_2d_v2.png",
            dpi=300, bbox_inches="tight",
            facecolor="white")
print("Saved.")