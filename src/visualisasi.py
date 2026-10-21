import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from objectives import calculate_objective
from constraints import (
    check_overlap,
    check_capacity,
    check_within_ship
)


SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"

WARNA_KATEGORIKAL = [
    "#2a78d6",
    "#eb6834",
    "#1baf7a",
    "#eda100",
    "#e87ba4",
    "#008300",
    "#4a3aa7",
    "#e34948"
]

WARNA_MAKS = "#2a78d6"


def _siapkan_dir(path):
    if path:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)


def _gaya_sumbu(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(
        True,
        color=GRID,
        linewidth=0.8
    )
    ax.set_axisbelow(True)

    for sisi in ("top", "right"):
        ax.spines[sisi].set_visible(False)

    for sisi in ("left", "bottom"):
        ax.spines[sisi].set_color(BASELINE)

    ax.tick_params(colors=MUTED)


def gambar_state(
    state,
    judul="",
    simpan_path=None
):
    kapal = state.ship

    fig, (
        ax_grid,
        ax_teks
    ) = plt.subplots(
        1,
        2,
        figsize=(11, 6),
        gridspec_kw={
            "width_ratios": [2.2, 1]
        }
    )

    fig.patch.set_facecolor(SURFACE)

    ax_grid.set_facecolor(SURFACE)
    ax_grid.set_xlim(0, kapal.w)
    ax_grid.set_ylim(0, kapal.l)
    ax_grid.set_aspect("equal")
    ax_grid.invert_yaxis()

    ax_grid.set_xticks(range(kapal.w + 1))
    ax_grid.set_yticks(range(kapal.l + 1))
    ax_grid.grid(
        True,
        color=GRID,
        linewidth=0.8
    )

    for sisi in ax_grid.spines.values():
        sisi.set_color(BASELINE)

    ax_grid.tick_params(
        colors=MUTED,
        labelsize=7
    )

    daftar_luar = []

    for i, placement in enumerate(state.placements):
        vehicle = placement.vehicle

        if not placement.on_ship:
            daftar_luar.append(vehicle.id)
            continue

        lebar, panjang = placement.effective_dimensions()

        warna = WARNA_KATEGORIKAL[i % len(WARNA_KATEGORIKAL)]

        kotak = patches.Rectangle(
            (placement.x, placement.y),
            lebar,
            panjang,
            facecolor=warna,
            edgecolor=TEXT_PRIMARY,
            linewidth=1,
            alpha=0.85
        )

        ax_grid.add_patch(kotak)

        ax_grid.text(
            placement.x + lebar / 2,
            placement.y + panjang / 2,
            placement.vehicle.id,
            ha="center",
            va="center",
            fontsize=8,
            color=TEXT_PRIMARY,
            fontweight="bold"
        )

    nilai = calculate_objective(state)

    berat_total = 0
    for placement in state.placements:
        if placement.on_ship:
            berat_total += placement.vehicle.Weight

    overlap = not check_overlap(state)
    kapasitas_valid = check_capacity(state)
    dalam_ship = all(
        check_within_ship(placement, state.ship)
        for placement in state.placements
    )

    feasible = not overlap and kapasitas_valid and dalam_ship

    teks = (
        f"Nilai objektif: {nilai}\n"
        f"Berat total: {berat_total} / {kapal.MaxCapacity}\n"
        f"Feasible: {feasible}\n"
        f"Overlap: {overlap}\n"
        f"Luar batas: {not dalam_ship}\n\n"
        f"Di luar kapal ({len(daftar_luar)}):\n"
    )

    if daftar_luar:
        teks += ", ".join(daftar_luar)
    else:
        teks += "None"

    ax_teks.axis("off")
    ax_teks.text(
        0,
        1,
        teks,
        va="top",
        ha="left",
        fontsize=9,
        color=TEXT_PRIMARY,
        wrap=True,
        transform=ax_teks.transAxes
    )

    fig.suptitle(judul, color=TEXT_PRIMARY)
    fig.tight_layout()

    if simpan_path:
        _siapkan_dir(simpan_path)
        fig.savefig(
            simpan_path,
            dpi=120,
            facecolor=SURFACE,
            bbox_inches="tight"
        )

    plt.close(fig)
    return fig


def plot_nilai(
    riwayat_nilai,
    judul="Nilai vs Iterasi",
    simpan_path=None
):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(SURFACE)

    _gaya_sumbu(ax)

    ax.plot(
        range(len(riwayat_nilai)),
        riwayat_nilai,
        color=WARNA_MAKS,
        linewidth=1.5
    )

    ax.set_xlabel("iterasi", color=TEXT_SECONDARY)
    ax.set_ylabel("nilai objektif", color=TEXT_SECONDARY)
    ax.set_title(judul, color=TEXT_PRIMARY)

    fig.tight_layout()

    if simpan_path:
        _siapkan_dir(simpan_path)
        fig.savefig(
            simpan_path,
            dpi=120,
            facecolor=SURFACE
        )

    plt.close(fig)
    return fig


def plot_probabilitas(
    riwayat_probabilitas,
    judul="e^(ΔE/T) vs Iterasi",
    simpan_path=None
):
    if not riwayat_probabilitas:
        return None

    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor(SURFACE)

    _gaya_sumbu(ax)

    if isinstance(riwayat_probabilitas[0], (tuple, list)):
        x = [item[0] for item in riwayat_probabilitas]
        y = [item[1] for item in riwayat_probabilitas]
    else:
        x = list(range(len(riwayat_probabilitas)))
        y = riwayat_probabilitas

    ax.scatter(x, y, color="#eb6834", s=6, alpha=0.4, edgecolors="none")

    ax.set_xlabel("iterasi", color=TEXT_SECONDARY)
    ax.set_ylabel("e^(ΔE/T)", color=TEXT_SECONDARY)
    ax.set_title(judul, color=TEXT_PRIMARY)
    ax.set_ylim(-0.05, 1.05)

    fig.tight_layout()

    if simpan_path:
        _siapkan_dir(simpan_path)
        fig.savefig(
            simpan_path,
            dpi=120,
            facecolor=SURFACE
        )

    plt.close(fig)
    return fig
