import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from constraints import is_valid
from objectives import calculate_objective

BACKGROUND = "#fcfcfb"
PRIMARY = "#0b0b0b"
GRID = "#e1e0d9"
CATEGORY = [
    "#196cb1",
    "#d63230",
    "#1c77c3",
    "#39a9db",
    "#40bcd8",
    "#c79d60",
    "#f39237",
    "#e56234",
]


def plot_state(
    state,
    title="",
    save_path=None,
    iterations=None,
    duration=None,
    algorithm=None,
    max_sideways=None,
    max_restarts=None,
    stuck_frequency=None,
    population_size=None,
    iteration=None,
    **kwargs,
):
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

    inside = []
    outside = []

    for i, placement in enumerate(state.placements):
        vehicle = placement.vehicle
        if not placement.on_ship:
            outside.append(vehicle.id)
            continue

        inside.append(vehicle.id)
        w, l = placement.effective_dimensions()
        color = CATEGORY[i % len(CATEGORY)]

        box = patches.Rectangle(
            (placement.x, placement.y),
            w,
            l,
            facecolor=color,
            edgecolor=PRIMARY,
            linewidth=1,
            alpha=0.85,
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
            fontweight="bold",
        )

    # ini soalnya aliasnya aga aga
    if iterations is None:
        iterations = iteration if iteration is not None else kwargs.get("iterasi", kwargs.get("iteration", None))
    if duration is None:
        duration = kwargs.get("durasi", None)
    if max_sideways is None:
        max_sideways = kwargs.get("max_sideway", None)
    if max_restarts is None:
        max_restarts = kwargs.get("max_restart", kwargs.get("restarts", None))
    if stuck_frequency is None:
        stuck_frequency = kwargs.get("stuck_count", kwargs.get("frekuensi_stuck", None))
    if population_size is None:
        population_size = kwargs.get("populasi", kwargs.get("population", None))

    value = calculate_objective(state)
    total_weight = sum(p.vehicle.Weight for p in state.placements if p.on_ship)

    inside_str = ", ".join(inside) if inside else "None"
    outside_str = ", ".join(outside) if outside else "None"

    if iterations is not None:
        try:
            iteration_str = str(int(iterations))
        except (ValueError, TypeError):
            iteration_str = str(iterations)
    else:
        iteration_str = "-"

    if duration is not None:
        if isinstance(duration, (int, float)):
            duration_str = f"{duration:.3f}s"
        else:
            duration_str = str(duration)
    else:
        duration_str = "-"

    info_lines = [
        f"Objective: {value}",
        f"Weight: {total_weight} / {ship.MaxCapacity}",
        f"Vehicle Inside: {len(inside)} ({inside_str})",
        f"Vehicle Outside: {len(outside)} ({outside_str})",
        f"Iteration: {iteration_str}",
        f"Duration: {duration_str}",
    ]

    algo = str(algorithm).lower().strip() if algorithm else ""

    if "sideways" in algo or max_sideways is not None:
        val = max_sideways if max_sideways is not None else "-"
        info_lines.append(f"Maximum sideways move: {val}")

    if ("restart" in algo or "rr" in algo) or max_restarts is not None:
        val = max_restarts if max_restarts is not None else "-"
        info_lines.append(f"maximum restart: {val}")

    if ("anneal" in algo or algo == "sa") or stuck_frequency is not None:
        val = stuck_frequency if stuck_frequency is not None else "-"
        info_lines.append(f"stuck frequency: {val}")

    if ("gene" in algo or algo == "ga") or population_size is not None:
        val = population_size if population_size is not None else "-"
        info_lines.append(f"jumlah populasi: {val}")

    info = "\n\n".join(info_lines)

    ax_text.axis("off")
    ax_text.text(0, 1, info, va="top", ha="left", fontsize=9.5, color=PRIMARY, wrap=True)

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

def plot_value_prob(
    value_history,
    prob_history=None,
    title="Simulated Annealing: Nilai Objektif & e^(ΔE/T) vs Iterasi",
    save_path=None,
):
    if prob_history is None and value_history and isinstance(value_history[0], (tuple, list)):
        prob_history = value_history
        value_history = []

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6.5), sharex=True)
    fig.patch.set_facecolor(BACKGROUND)

    # Nilai Objektif kek buat subplot 1
    ax1.set_facecolor(BACKGROUND)
    ax1.grid(True, color=GRID, linewidth=0.8)
    if value_history:
        ax1.plot(
            range(len(value_history)),
            value_history,
            color=CATEGORY[0],
            linewidth=1.5,
            label="Nilai Objektif",
        )
        ax1.legend(loc="lower right")
    ax1.set_ylabel("nilai objektif")
    ax1.set_title(title, color=PRIMARY)

    # Subplot 2 buat si e^(ΔE/T)
    ax2.set_facecolor(BACKGROUND)
    ax2.grid(True, color=GRID, linewidth=0.8)
    if prob_history:
        if isinstance(prob_history[0], (tuple, list)):
            x = [item[0] for item in prob_history]
            y = [item[1] for item in prob_history]
        else:
            x = list(range(len(prob_history)))
            y = prob_history

        ax2.scatter(
            x,
            y,
            color=CATEGORY[1],
            s=6,
            alpha=0.4,
            edgecolors="none",
            label="e^(ΔE/T)",
        )
        ax2.legend(loc="upper right")
    ax2.set_xlabel("iterasi")
    ax2.set_ylabel("e^(ΔE/T)")
    ax2.set_ylim(-0.05, 1.05)

    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=120, facecolor=BACKGROUND)

    plt.close(fig)
    return fig

def plot_value_ga(max_history, avg_history, title="GA: Objective vs Iteration", save_path=None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.grid(True, color=GRID, linewidth=0.8)

    ax.plot(range(len(max_history)), max_history, color=CATEGORY[0], linewidth=1.5, label="Maksimum")
    ax.plot(range(len(avg_history)), avg_history, color=CATEGORY[1], linewidth=1.5, label="Rata-rata")
    ax.set_xlabel("iterasi")
    ax.set_ylabel("nilai objektif")
    ax.set_title(title, color=PRIMARY)
    ax.legend()
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=120, facecolor=BACKGROUND)

    plt.close(fig)
    return fig

def plot_value_rr(
    value_history,
    best_history=None,
    restart_indices=None,
    title="Random Restart: Objective vs Iterasi",
    save_path=None,
):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.grid(True, color=GRID, linewidth=0.8)

    ax.plot(
        range(len(value_history)),
        value_history,
        color=CATEGORY[0],
        linewidth=1.2,
        alpha=0.75,
        label="Nilai Objektif",
    )
    if best_history:
        ax.plot(
            range(len(best_history)),
            best_history,
            color=CATEGORY[1],
            linewidth=1.8,
            label="Nilai Terbaik (Best)",
        )

    if restart_indices and len(restart_indices) > 1:
        first = True
        for idx in restart_indices[1:]:
            label = "Restart" if first else None
            ax.axvline(
                x=idx,
                color="#898781",
                linestyle="--",
                linewidth=0.9,
                alpha=0.6,
                label=label,
            )
            first = False

    ax.set_xlabel("iterasi")
    ax.set_ylabel("nilai objektif")
    ax.set_title(title, color=PRIMARY)
    ax.legend(loc="lower right")
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=120, facecolor=BACKGROUND)

    plt.close(fig)
    return fig
