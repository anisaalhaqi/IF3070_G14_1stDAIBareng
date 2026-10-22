import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == "src":
    SRC_DIR = BASE_DIR
    BASE_DIR = os.path.dirname(BASE_DIR)
else:
    SRC_DIR = os.path.join(BASE_DIR, "src")

EXP_DIR = os.path.join(SRC_DIR, "experiment")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if EXP_DIR not in sys.path:
    sys.path.insert(0, EXP_DIR)

from data.loader import load_data
from objectives import calculate_objective
from state import State

# Import modul eksperimen langsung dari folder src/experiment
import exp_steepest_ascent
import exp_sideways
import exp_stochastic
import exp_random_restart
import exp_simulated_annealing
import exp_genetic

DATA_PATH = os.path.join(SRC_DIR, "data", "data.json")

DAFTAR_ALGORITMA = {
    1: ("Steepest Ascent Hill-Climbing", exp_steepest_ascent.main),
    2: ("Sideways Move Hill-Climbing", exp_sideways.main),
    3: ("Stochastic Hill-Climbing", exp_stochastic.main),
    4: ("Random Restart Hill-Climbing", exp_random_restart.main),
    5: ("Simulated Annealing", exp_simulated_annealing.main),
    6: ("Genetic Algorithm", exp_genetic.main),
}


def main():
    print("\n" + "=" * 65)
    print("      PROGRAM UTAMA EVALUASI ALGORITMA (APPLES-TO-APPLES)")
    print("=" * 65)

    ship, vehicles = load_data(DATA_PATH)

    # 1. Bangkitkan 3 initial state terpusat di awal program
    print("\nMembangkitkan 3 Initial State awal terpusat...")
    initial_states = [State.random(ship, vehicles) for _ in range(3)]

    print("\n3 Initial State berhasil dibuat (akan digunakan oleh SEMUA algoritma):")
    for i, st in enumerate(initial_states, 1):
        print(f"  * Percobaan {i} : Nilai Objective Awal = {calculate_objective(st)}")

    sudah_dijalankan = set()

    # 2. Loop menu pilihan algoritma
    while True:
        belum_dicoba = [k for k in DAFTAR_ALGORITMA if k not in sudah_dijalankan]

        print("\n" + "=" * 65)
        print("                   PILIHAN ALGORITMA")
        print("=" * 65)
        for num, (nama, _) in DAFTAR_ALGORITMA.items():
            status = "[SUDAH DIJALANKAN]" if num in sudah_dijalankan else "[BELUM DICOBA]"
            print(f"  {num}. {nama:<35} {status}")

        print("  7. Jalankan SEMUA Algoritma yang Belum Dicoba")
        print("  0. Selesai (Keluar)")

        if belum_dicoba:
            nama_sisa = ", ".join([f"{k} ({DAFTAR_ALGORITMA[k][0]})" for k in belum_dicoba])
            print(f"\nAlgoritma yang belum dicoba: {nama_sisa}")
        else:
            print("\nSemua algoritma sudah selesai dicoba!")

        pilihan = input("\nMasukkan nomor pilihan Anda: ").strip()

        if pilihan in ["0", "selesai", "exit", "keluar"]:
            print("\nTerima kasih! Seluruh grafik gambar dan rekap CSV tersimpan di folder 'output/'.")
            break

        elif pilihan == "7":
            targets = [k for k in range(1, 7) if k not in sudah_dijalankan]
            if not targets:
                print("Semua algoritma sudah pernah dijalankan.")
                continue

            for k in targets:
                nama, func = DAFTAR_ALGORITMA[k]
                print(f"\n>>> Memulai: {nama} <<<")
                func(initial_states=initial_states)
                sudah_dijalankan.add(k)

        elif pilihan.isdigit() and int(pilihan) in DAFTAR_ALGORITMA:
            pilih_num = int(pilihan)
            nama, func = DAFTAR_ALGORITMA[pilih_num]
            func(initial_states=initial_states)
            sudah_dijalankan.add(pilih_num)

        else:
            print("Pilihan tidak valid, silakan masukkan nomor menu yang benar.")


if __name__ == "__main__":
    main()
