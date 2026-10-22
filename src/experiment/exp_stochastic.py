import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.stochastic import stochastic_hill_climbing
from data.loader import load_data
from objectives import calculate_objective
from visualisasi import plot_state, plot_value

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output", "stochastic")


def main(initial_states=None):
    ship, vehicles = load_data(DATA_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rekap = []
    jumlah_percobaan = 3

    print("--- Eksperimen Stochastic Hill-Climbing ---")

    for i in range(1, jumlah_percobaan + 1):
        initial_state = initial_states[i - 1].copy()
        initial_value = calculate_objective(initial_state)

        hasil = stochastic_hill_climbing(initial_state.copy(), max_iterations=1000)

        final_state = hasil["final_state"]
        final_value = hasil["final_value"]
        durasi = hasil["duration"]
        iterasi = hasil["iterations"]
        stop_reason = hasil["stop_reason"]
        history = hasil["value_history"]

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
        )
        plot_value(history, title=f"Percobaan {i} - Objective vs Iterasi", save_path=path_plot)

        rekap.append({
            "percobaan": i,
            "nilai_awal": initial_value,
            "nilai_akhir": final_value,
            "durasi_detik": f"{durasi:.4f}",
            "iterasi": iterasi,
            "stop_reason": stop_reason,
            "state_awal_img": f"percobaan_{i}_initial.png",
            "state_akhir_img": f"percobaan_{i}_final.png",
            "plot_obj_img": f"percobaan_{i}_objective.png",
        })

        print(f"Percobaan {i}: awal={initial_value}, akhir={final_value}, iterasi={iterasi}, berhenti={stop_reason}, waktu={durasi:.3f}s")

    csv_path = os.path.join(OUTPUT_DIR, "rekap_stochastic.csv")
    fieldnames = [
        "percobaan",
        "nilai_awal",
        "nilai_akhir",
        "durasi_detik",
        "iterasi",
        "stop_reason",
        "state_awal_img",
        "state_akhir_img",
        "plot_obj_img",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rekap)

    print(f"Rekap disimpan ke {csv_path}")


if __name__ == "__main__":
    main()
