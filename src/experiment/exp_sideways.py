import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.sideways_move import hill_climbing_sideways
from data.loader import load_data
from objectives import calculate_objective
from state import State
from visualisasi import gambar_state, plot_nilai

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output", "sideways")


def main():
    inp = input("Masukkan maximum sideways move (default 100): ").strip()
    try:
        max_sideways = int(inp) if inp else 100
    except ValueError:
        print("Input tidak valid, menggunakan default 100.")
        max_sideways = 100

    ship, vehicles = load_data(DATA_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rekap = []
    jumlah_percobaan = 3

    print(f"\n--- Eksperimen Hill-Climbing Sideways Move (max_sideways={max_sideways}) ---")

    for i in range(1, jumlah_percobaan + 1):
        initial_state = State.random(ship, vehicles)
        initial_value = calculate_objective(initial_state)

        hasil = hill_climbing_sideways(initial_state, max_sideways=max_sideways, max_iterations=1000)

        final_state = hasil["final_state"]
        final_value = hasil["final_value"]
        durasi = hasil["duration"]
        iterasi = hasil["iterations"]
        sideways = hasil["sideways_moves"]
        stop_reason = hasil["stop_reason"]
        history = hasil["value_history"]

        path_init = os.path.join(OUTPUT_DIR, f"percobaan_{i}_initial.png")
        path_final = os.path.join(OUTPUT_DIR, f"percobaan_{i}_final.png")
        path_plot = os.path.join(OUTPUT_DIR, f"percobaan_{i}_objective.png")

        gambar_state(initial_state, judul=f"Percobaan {i} - Initial State", simpan_path=path_init)
        gambar_state(final_state, judul=f"Percobaan {i} - Final State", simpan_path=path_final)
        plot_nilai(history, judul=f"Percobaan {i} - Objective vs Iterasi", simpan_path=path_plot)

        rekap.append({
            "percobaan": i,
            "max_sideways": max_sideways,
            "nilai_awal": initial_value,
            "nilai_akhir": final_value,
            "durasi_detik": f"{durasi:.4f}",
            "iterasi": iterasi,
            "sideways_moves": sideways,
            "stop_reason": stop_reason,
            "state_awal_img": f"percobaan_{i}_initial.png",
            "state_akhir_img": f"percobaan_{i}_final.png",
            "plot_obj_img": f"percobaan_{i}_objective.png",
        })

        kondisi = "mencapai max_sideways" if stop_reason == "max_sideways" else stop_reason
        print(f"Percobaan {i}: awal={initial_value}, akhir={final_value}, iterasi={iterasi}, sideways={sideways}/{max_sideways}, berhenti={kondisi}, waktu={durasi:.3f}s")

    csv_path = os.path.join(OUTPUT_DIR, "rekap_sideways.csv")
    fieldnames = [
        "percobaan",
        "max_sideways",
        "nilai_awal",
        "nilai_akhir",
        "durasi_detik",
        "iterasi",
        "sideways_moves",
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
