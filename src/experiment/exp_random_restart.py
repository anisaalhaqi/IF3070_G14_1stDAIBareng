import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.random_restart import random_restart_hill_climbing
from data.loader import load_data
from objectives import calculate_objective
from state import State
from visualisasi import plot_state, plot_value_rr

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output", "random_restart")


def main():
    inp = input("Masukkan maximum restart (default 10): ").strip()
    try:
        max_restarts = int(inp) if inp else 10
        if max_restarts <= 0:
            print("Nilai harus > 0, menggunakan default 10.")
            max_restarts = 10
    except ValueError:
        print("Input tidak valid, menggunakan default 10.")
        max_restarts = 10

    max_iterations = 1000

    ship, vehicles = load_data(DATA_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rekap = []
    jumlah_percobaan = 3

    print(f"\n--- Eksperimen Random Restart Hill-Climbing (max_restart={max_restarts}) ---")

    for i in range(1, jumlah_percobaan + 1):
        initial_state = State.random(ship, vehicles)
        initial_value = calculate_objective(initial_state)

        hasil = random_restart_hill_climbing(
            initial_state,
            max_restarts=max_restarts,
            max_iterations_per_restart=max_iterations,
            vehicles=vehicles,
        )

        final_state = hasil["final_state"]
        final_value = hasil["final_value"]
        durasi = hasil["duration"]
        iterasi = hasil["iterations"]
        restarts = hasil["restarts"]
        iter_per_restart = hasil["iterations_per_restart"]
        stop_reason = hasil["stop_reason"]
        history = hasil["value_history"]
        best_history = hasil["best_value_history"]
        restart_indices = hasil["restart_indices"]

        path_init = os.path.join(OUTPUT_DIR, f"percobaan_{i}_initial.png")
        path_final = os.path.join(OUTPUT_DIR, f"percobaan_{i}_final.png")
        path_plot = os.path.join(OUTPUT_DIR, f"percobaan_{i}_objective.png")

        plot_state(initial_state, title=f"Percobaan {i} - Initial State", save_path=path_init)
        plot_state(
            final_state,
            title=f"Percobaan {i} - Final State",
            save_path=path_final,
            iterations=hasil["iterations"],
            duration=hasil["duration"],
            algorithm="random restart",
            max_restarts=max_restarts,
        )
        plot_value_rr(
            history,
            best_history=best_history,
            restart_indices=restart_indices,
            title=f"Percobaan {i} - Objective vs Iterasi (RRHC)",
            save_path=path_plot,
        )

        rekap.append({
            "percobaan": i,
            "max_restart": max_restarts,
            "banyak_restart": restarts,
            "nilai_awal": initial_value,
            "nilai_akhir": final_value,
            "durasi_detik": f"{durasi:.4f}",
            "total_iterasi": iterasi,
            "iterasi_per_restart": str(iter_per_restart),
            "stop_reason": stop_reason,
            "state_awal_img": f"percobaan_{i}_initial.png",
            "state_akhir_img": f"percobaan_{i}_final.png",
            "plot_obj_img": f"percobaan_{i}_objective.png",
        })

        kondisi = "mencapai max_restart" if stop_reason == "max_restarts" else stop_reason
        print(
            f"Percobaan {i}: awal={initial_value}, akhir={final_value}, "
            f"restart={restarts}/{max_restarts}, total_iterasi={iterasi}, "
            f"iterasi_per_restart={iter_per_restart}, berhenti={kondisi}, waktu={durasi:.3f}s"
        )

    csv_path = os.path.join(OUTPUT_DIR, "rekap_random_restart.csv")
    fieldnames = [
        "percobaan",
        "max_restart",
        "banyak_restart",
        "nilai_awal",
        "nilai_akhir",
        "durasi_detik",
        "total_iterasi",
        "iterasi_per_restart",
        "stop_reason",
        "state_awal_img",
        "state_akhir_img",
        "plot_obj_img",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rekap)

    print(f"\nRekap disimpan ke {csv_path}")


if __name__ == "__main__":
    main()
