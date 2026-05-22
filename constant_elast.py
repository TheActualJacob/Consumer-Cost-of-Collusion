import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap
from scipy import integrate

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

cmap = LinearSegmentedColormap.from_list(
    "econ",
    ["#1a1060", "#3d2b8a", "#8b4513", "#c8860a", "#e8c840", "#f5f0dc"],
    N=512
)

def compute_delta_cs(n, mc_ratio, eps):
    """
    mc_ratio = m/c (demand scale over marginal cost)
    eps      = price elasticity (> 1 for finite equilibrium)
    """
    c = 1.0
    m = mc_ratio * c

    # Cournot equilibrium output
    factor_c = (n * eps - 1) / (n * eps)
    if factor_c <= 0:
        return np.nan
    Q_cournot = (m / c * factor_c) ** eps

    # Collusive equilibrium output
    factor_k = (eps - 1) / eps
    if factor_k <= 0:
        return np.nan
    Q_collusion = (m / c * factor_k) ** eps

    # Consumer surplus via numerical integration
    # CS = integral from P* to P_max of D(p) dp
    # Equivalently CS = integral from Q* to Q_max of P(Q) dQ - P(Q*)*Q*
    def P(Q):
        return m * Q ** (-1.0 / eps)

    def cs_from_output(Q_star):
        Q_upper = Q_star * 1000  # large upper bound
        val, _ = integrate.quad(lambda Q: P(Q), Q_star, Q_upper)
        val -= P(Q_star) * Q_star
        return val

    CS_cournot   = cs_from_output(Q_cournot)
    CS_collusion = cs_from_output(Q_collusion)
    return CS_cournot - CS_collusion

# ── Grid ───────────────────────────────────────────────────────────────────
n_vals    = np.linspace(1, 15, 40)
mc_vals   = np.linspace(1.05, 4, 40)
eps       = 2.0   # baseline elasticity

N, MC = np.meshgrid(n_vals, mc_vals)
DCS   = np.vectorize(compute_delta_cs)(N, MC, eps)

# ── Plot ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 9), dpi=300)
ax  = fig.add_subplot(111, projection="3d")
ax.set_facecolor("#0d0d0d")

surf = ax.plot_surface(
    N, MC, DCS,
    cmap=cmap,
    linewidth=0,
    antialiased=True,
    alpha=0.95,
    rcount=100,
    ccount=100,
)

cbar = fig.colorbar(surf, ax=ax, shrink=0.45, aspect=12, pad=0.02)
cbar.set_label(r"$\Delta CS$", fontsize=12, labelpad=10, color="#e8e0d0")
cbar.ax.yaxis.set_tick_params(color="#9a9080")
plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#9a9080", fontsize=9)
cbar.outline.set_edgecolor("#3a3530")

ax.set_xlabel(r"$n$  (number of firms)",
              fontsize=12, labelpad=14, color="#c8b898")
ax.set_ylabel(r"$m/c$  (demand-cost ratio)",
              fontsize=12, labelpad=14, color="#c8b898")
ax.set_zlabel(r"$\Delta CS$",
              fontsize=12, labelpad=10, color="#c8b898")

ax.set_title(
    r"$\Delta CS$ under Constant Elasticity Demand  $P(Q)=mQ^{-1/\varepsilon}$,  $\varepsilon=2$",
    fontsize=13, color="#e8e0d0", pad=22
)

ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.tick_params(axis="both", labelsize=9)

for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
    pane.fill = False
    pane.set_edgecolor("#2a2520")

ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.4)
ax.view_init(elev=25, azim=10)

fig.text(0.13, 0.03,
         r"Parameters: $\varepsilon = 2$,  $n \in [1,\,15]$,  $m/c \in [1.05,\,4]$",
         fontsize=9, color="#6a6058", style="italic")

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/delta_cs_constant_elasticity.png",
            dpi=300, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved.")