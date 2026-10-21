import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.simulated_annealing import simulated_annealing
from data.loader import load_data
from objectives import calculate_objective
from state import State
from visualisasi import gambar_state, plot_nilai, plot_probabilitas

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output", "simulated_annealing")


def main():
    ship, vehicles = load_data(DATA_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rekap = []
    jumlah_percobaan = 3

    print("--- Eksperimen Simulated Annealing ---")

    for i in range(1, jumlah_percobaan + 1):
        initial_state = State.random(ship, vehicles)
        initial_value = calculate_objective(initial_state)

        hasil = simulated_annealing(
            initial_state,
            initial_temp=100.0,
            min_temp=1.0,
            stuck_limit=50,
            max_iterations=5000
        )

        final_state = hasil["final_state"]
        final_value = hasil["final_value"]
        durasi = hasil["duration"]
        iterasi = hasil["iterations"]
        stuck_count = hasil["stuck_count"]
        history_value = hasil["value_history"]
        history_prob = hasil["probability_history"]

        path_init = os.path.join(OUTPUT_DIR, f"percobaan_{i}_initial.png")
        path_final = os.path.join(OUTPUT_DIR, f"percobaan_{i}_final.png")
        path_plot_obj = os.path.join(OUTPUT_DIR, f"percobaan_{i}_objective.png")
        path_plot_prob = os.path.join(OUTPUT_DIR, f"percobaan_{i}_probabilitas.png")

        gambar_state(initial_state, judul=f"Percobaan {i} - Initial State", simpan_path=path_init)
        gambar_state(final_state, judul=f"Percobaan {i} - Final State", simpan_path=path_final)
        plot_nilai(history_value, judul=f"Percobaan {i} - Objective vs Iterasi", simpan_path=path_plot_obj)
        plot_probabilitas(history_prob, judul=f"Percobaan {i} - e^(ΔE/T) vs Iterasi", simpan_path=path_plot_prob)

        rekap.append({
            "percobaan": i,
            "nilai_awal": initial_value,
            "nilai_akhir": final_value,
            "durasi_detik": f"{durasi:.4f}",
            "iterasi": iterasi,
            "frekuensi_stuck": stuck_count,
            "state_awal_img": f"percobaan_{i}_initial.png",
            "state_akhir_img": f"percobaan_{i}_final.png",
            "plot_obj_img": f"percobaan_{i}_objective.png",
            "plot_exp_prob_img": f"percobaan_{i}_probabilitas.png",
        })

        print(f"Percobaan {i}: awal={initial_value}, akhir={final_value}, iterasi={iterasi}, stuck={stuck_count}, waktu={durasi:.3f}s")

    csv_path = os.path.join(OUTPUT_DIR, "rekap_simulated_annealing.csv")
    fieldnames = [
        "percobaan",
        "nilai_awal",
        "nilai_akhir",
        "durasi_detik",
        "iterasi",
        "frekuensi_stuck",
        "state_awal_img",
        "state_akhir_img",
        "plot_obj_img",
        "plot_exp_prob_img",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rekap)

    print(f"Rekap disimpan ke {csv_path}")


if __name__ == "__main__":
    main()
