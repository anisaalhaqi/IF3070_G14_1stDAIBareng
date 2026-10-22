import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.genetic import genetic_algorithm
from data.loader import load_data
from objectives import calculate_objective
from visualisasi import plot_state, plot_value_ga

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output", "genetic")


def main(initial_states=None):
    try:
        inp = input("Masukkan jumlah populasi kontrol untuk exp1 (default 50): ").strip()
        pop_kontrol = int(inp) if inp else 50
        inp = input("Masukkan 3 variasi iterasi, pisah koma (default 50,100,200): ").strip()
        var_iter = [int(x) for x in inp.split(",")] if inp else [50, 100, 200]
        inp = input("Masukkan banyak iterasi kontrol untuk exp2 (default 100): ").strip()
        iter_kontrol = int(inp) if inp else 100
        inp = input("Masukkan 3 variasi populasi, pisah koma (default 20,50,100): ").strip()
        var_pop = [int(x) for x in inp.split(",")] if inp else [20, 50, 100]
    except ValueError:
        print("Input tidak valid, menggunakan semua nilai default.")
        pop_kontrol, var_iter = 50, [50, 100, 200]
        iter_kontrol, var_pop = 100, [20, 50, 100]

    ship, vehicles = load_data(DATA_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rekap = []
    jumlah_percobaan = 3

    konfigurasi = [("exp1", pop_kontrol, it) for it in var_iter]
    konfigurasi += [("exp2", pop, iter_kontrol) for pop in var_pop]

    for nama, populasi, iterasi in konfigurasi:
        folder = f"{nama}_pop{populasi}_iter{iterasi}"
        os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

        print(f"\n--- Eksperimen Genetic Algorithm ({nama}: populasi={populasi}, iterasi={iterasi}) ---")

        for i in range(1, jumlah_percobaan + 1):
            initial_state = initial_states[i - 1].copy()
            initial_value = calculate_objective(initial_state)

            hasil = genetic_algorithm(initial_state.copy(), population_size=populasi, max_iterations=iterasi)

            final_state = hasil["final_state"]
            final_value = hasil["final_value"]
            durasi = hasil["duration"]

            path_init = os.path.join(OUTPUT_DIR, folder, f"percobaan_{i}_initial.png")
            path_final = os.path.join(OUTPUT_DIR, folder, f"percobaan_{i}_final.png")
            path_plot = os.path.join(OUTPUT_DIR, folder, f"percobaan_{i}_objective.png")

            plot_state(initial_state, title=f"Percobaan {i} - Initial State", save_path=path_init)
            plot_state(
                final_state,
                title=f"Percobaan {i} - Final State",
                save_path=path_final,
                iterations=hasil["iterations"],
                duration=hasil["duration"],
                algorithm="genetic",
                population_size=populasi,
            )
            plot_value_ga(
                hasil["max_history"],
                hasil["avg_history"],
                title=f"Percobaan {i} - Objective vs Iterasi",
                save_path=path_plot,
            )

            rekap.append({
                "eksperimen": nama,
                "percobaan": i,
                "populasi": populasi,
                "iterasi": iterasi,
                "nilai_awal": initial_value,
                "nilai_akhir": final_value,
                "durasi_detik": f"{durasi:.4f}",
                "state_awal_img": f"{folder}/percobaan_{i}_initial.png",
                "state_akhir_img": f"{folder}/percobaan_{i}_final.png",
                "plot_obj_img": f"{folder}/percobaan_{i}_objective.png",
            })

            print(f"Percobaan {i}: awal={initial_value}, akhir={final_value}, populasi={populasi}, iterasi={iterasi}, waktu={durasi:.3f}s")

    csv_path = os.path.join(OUTPUT_DIR, "rekap_genetic.csv")
    fieldnames = [
        "eksperimen",
        "percobaan",
        "populasi",
        "iterasi",
        "nilai_awal",
        "nilai_akhir",
        "durasi_detik",
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
