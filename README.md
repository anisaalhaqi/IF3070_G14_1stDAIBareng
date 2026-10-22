# Tugas Besar 1 IF2220 / II2220 Dasar Inteligensi Artifisial
---

## Deskripsi Singkat Repository

Repository ini berisi implementasi  algoritma **Local Search** untuk memecahkan permasalahan optimasi penataan muatan kendaraan pada kapal. 

Tujuan utama dari optimasi ini adalah memaksimalkan total pendapatan pengiriman (*shipping fee*) dari kendaraan yang dimuat ke dalam kapal, dengan tetap mematuhi batasan-batasan (*constraints*) fisik dan teknis:
1. **Kapasitas Beban Maksimum**: Total berat kendaraan tidak boleh melebihi kapasitas beban kapal (*MaxCapacity*).
2. **Dimensi Kapal**: Semua kendaraan yang dimuat harus berada di dalam batas dimensi dek kapal (lebar $W$ dan panjang $L$).
3. **Pencegahan Tumpang Tindih (No Overlap)**: Posisi setiap kendaraan yang dimuat tidak boleh saling bertumpukan satu sama lain.

Algoritma-algoritma yang diimplementasikan dalam proyek ini mencakup:
1. **Steepest Ascent Hill-Climbing**
2. **Hill-Climbing with Sideways Move**
3. **Stochastic Hill-Climbing**
4. **Random Restart Hill-Climbing**
5. **Simulated Annealing**
6. **Genetic Algorithm**

**Bonus yang diambil :** menerapkan semua Hill - Climbing

---

## Cara Setup dan Menjalankan Program

### 1. Prasyarat Sistem
- **Python**: Versi 3.8 atau yang lebih baru.
- **Git** (opsional, jika mengkloning repositori).

### 2. Kloning Repository & Menyiapkan Environment
Buka terminal / Command Prompt / PowerShell, lalu clone repository ini:
```bash
git clone https://github.com/Tubes1-1stDAIBareng.git
cd Tubes1-1stDAIBareng
```

### 3. Instalasi Dependensi
Program ini menggunakan pustaka eksternal `matplotlib` untuk visualisasi:
```bash
pip install matplotlib
```

### 4. Menjalankan Program
Jalankan program utama dari *root directory*:
```bash
python src/main.py
```
*(Atau masuk ke direktori `src` terlebih dahulu dengan `cd src` lalu jalankan `python main.py`)*

### 5. Penggunaan Menu Interaktif (CLI)
Setelah program dijalankan, program akan menghasilkan 3 *random initial state* yang sama untuk digunakan sebagai basis perbandingan yang adil antar algoritma. Anda akan disajikan menu:

```text
==============
Program Utama
==============

3 Random Initial State :
  * Percobaan 1 : Nilai Objective Awal = ...
  * Percobaan 2 : Nilai Objective Awal = ...
  * Percobaan 3 : Nilai Objective Awal = ...

==================
PILIHAN ALGORITMA
==================
  1. Steepest Ascent Hill-Climbing       [BELUM DICOBA]
  2. Sideways Move Hill-Climbing         [BELUM DICOBA]
  3. Stochastic Hill-Climbing            [BELUM DICOBA]
  4. Random Restart Hill-Climbing        [BELUM DICOBA]
  5. Simulated Annealing                 [BELUM DICOBA]
  6. Genetic Algorithm                   [BELUM DICOBA]
  7. Jalankan SEMUA Algoritma yang Belum Dicoba
  0. Selesai (Keluar)

Masukkan nomor pilihan Anda:
```

- Masukkan angka **`1` - `6`** untuk menjalankan algoritma tertentu.
- Masukkan angka **`7`** untuk mengeksekusi semua algoritma secara berurutan.
- Masukkan angka **`0`** untuk keluar dari program.
- Hasil keluaran visualisasi denah penataan dek kapal dan grafik perkembangan nilai fungsi objektif akan otomatis disimpan ke dalam folder `output/<nama_algoritma>/`.

---

## 👥 Pembagian Tugas Anggota Kelompok

| Nama | NIM | Tugas & Tanggung Jawab |
| :--- | :---: | :--- |
| **Nadine Arindy Octavia** | **18224012** | - Implementasi `main.py`<br>- Implementasi `algorithms/genetic.py`<br>- Implementasi `algorithms/stochastic.py`<br>- Implementasi `experiment/exp_genetic.py`<br>- Implementasi `experiment/exp_stochastic.py`<br>- Implementasi modul `visualisasi.py`<br>- Mengisi laporan dokumen bagian **BAB II Implementasi Algoritma Local Search**<br>- Mengisi laporan dokumen bagian **Kesimpulan dan Saran** |
| **Anisa Aulia Alhaqi** | **18224080** | - Implementasi `model.py`<br>- Implementasi `constraints.py`<br>- Implementasi `neighbors.py`<br>- Implementasi `objectives.py`<br>- Implementasi `state.py`<br>- Implementasi `algorithms/simulated_annealing.py`<br>- Implementasi `algorithms/sideways_move.py`<br>- Implementasi `algorithms/random_restart.py`<br>- Implementasi `experiment/exp_simulated_annealing.py` |
| **Riko Satriya Giovanni** | **18224108** | - Implementasi `algorithms/steepest_ascent.py`<br>- Implementasi `algorithms/random_restart.py`<br>- Implementasi `experiment/exp_steepest_ascent.py`<br>- Implementasi `experiment/exp_random_restart.py`<br>- Implementasi modul `visualisasi.py`<br>- Mengisi laporan dokumen bagian **BAB III Hasil dan Analisis Eksperimen**<br>- Mengisi laporan dokumen bagian **Kesimpulan dan Saran** |
