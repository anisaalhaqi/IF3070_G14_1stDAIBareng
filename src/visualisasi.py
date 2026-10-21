import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from constraints import is_valid
from objectives import calculate_objective

BACKGROUND = "#fcfcfb"
PRIMARY = "#0b0b0b"
GRID = "#e1e0d9"
CATEGORY = [
    "#2a78d6",
    "#eb6834",
    "#1baf7a",
    "#eda100",
    "#e87ba4",
    "#008300",
    "#4a3aa7",
    "#e34948"
]


def plot_state(state, title="", save_path=None):
    ship = state.ship

    fig, (ax_grid, ax_text) = plt.subplots(
        1, 2, figsize=(11, 6), gridspec_kw={"width_ratios": [2.2, 1]}
    )
    fig.patch.set_facecolor(BACKGROUND)

    ax_grid.set_facecolor(BACKGROUND)
    ax_grid.set_xlim(0, ship.w)
    ax_grid.set_ylim(0, ship.l)
    ax_grid.set_aspect("equal")
    ax_grid.invert_yaxis()
    ax_grid.set_xticks(range(ship.w + 1))
    ax_grid.set_yticks(range(ship.l + 1))
    ax_grid.grid(True, color=GRID, linewidth=0.8)

    outside = []

    for i, placement in enumerate(state.placements):
        vehicle = placement.vehicle
        if not placement.on_ship:
            outside.append(vehicle.id)
            continue

        w, l = placement.effective_dimensions()
        color = CATEGORY[i % len(CATEGORY)]

        box = patches.Rectangle(
            (placement.x, placement.y),
            w,
            l,
            facecolor=color,
            edgecolor=PRIMARY,
            linewidth=1,
            alpha=0.85
        )
        ax_grid.add_patch(box)
        ax_grid.text(
            placement.x + w / 2,
            placement.y + l / 2,
            vehicle.id,
            ha="center",
            va="center",
            fontsize=8,
            color=PRIMARY,
            fontweight="bold"
        )

    value = calculate_objective(state)
    total_weight = sum(p.vehicle.Weight for p in state.placements if p.on_ship)
    valid = is_valid(state)

    info = (
        f"Objective: {value}\n"
        f"Weight: {total_weight} / {ship.MaxCapacity}\n"
        f"Valid: {valid}\n\n"
        f"Outside ({len(outside)}):\n"
    )
    info += ", ".join(outside) if outside else "None"

    ax_text.axis("off")
    ax_text.text(0, 1, info, va="top", ha="left", fontsize=9, color=PRIMARY, wrap=True)

    if title:
        fig.suptitle(title, color=PRIMARY)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=120, facecolor=BACKGROUND, bbox_inches="tight")

    plt.close(fig)
    return fig


def plot_value(value_history, title="Value vs Iteration", save_path=None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.grid(True, color=GRID, linewidth=0.8)

    ax.plot(range(len(value_history)), value_history, color=CATEGORY[0], linewidth=1.5)
    ax.set_xlabel("iterasi")
    ax.set_ylabel("nilai objektif")
    ax.set_title(title, color=PRIMARY)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=120, facecolor=BACKGROUND)

    plt.close(fig)
    return fig


def plot_prob(prob_history, title="e^(ΔE/T) vs Iteration", save_path=None):
    if not prob_history:
        return None

    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.grid(True, color=GRID, linewidth=0.8)

    if isinstance(prob_history[0], (tuple, list)):
        x = [item[0] for item in prob_history]
        y = [item[1] for item in prob_history]
    else:
        x = list(range(len(prob_history)))
        y = prob_history

    ax.scatter(x, y, color=CATEGORY[1], s=6, alpha=0.4, edgecolors="none")
    ax.set_xlabel("iterasi")
    ax.set_ylabel("e^(ΔE/T)")
    ax.set_title(title, color=PRIMARY)
    ax.set_ylim(-0.05, 1.05)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=120, facecolor=BACKGROUND)

    plt.close(fig)
    return fig
