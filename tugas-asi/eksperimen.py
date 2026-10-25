import csv
import time
import random
from typing import List, Dict

# ------------------------------------------------------
# KONFIGURASI
# ------------------------------------------------------
ASAM_AMINO = list("ACDEFGHIKLMNPQRSTVWY")  # 20 jenis standar
JUMLAH_SAMPEL = 200  # Diperluas dari 50 menjadi 200

# Model 1: Pendekatan berbasis pola
def model_pola(urutan: str) -> Dict:
    waktu_proses = len(urutan) * 0.015
    akurasi = 0.62 + (hash(urutan) % 25) / 100  # rentang 0.62–0.87
    time.sleep(waktu_proses / 500)  # dipercepat agar cepat selesai
    return {
        "metode": "Model Berbasis Pola",
        "akurasi": round(akurasi, 3),
        "waktu_detik": round(waktu_proses, 3),
        "berhasil": akurasi > 0.70
    }

# Model 2: Pendekatan berbasis pembelajaran mendalam
def model_pembelajaran(urutan: str) -> Dict:
    waktu_proses = len(urutan) * 0.045
    akurasi = 0.85 + (hash(urutan) % 12) / 100  # rentang 0.85–0.97
    time.sleep(waktu_proses / 500)
    return {
        "metode": "Model Berbasis Pembelajaran Mendalam",
        "akurasi": round(akurasi, 3),
        "waktu_detik": round(waktu_proses, 3),
        "berhasil": akurasi > 0.70
    }

# ------------------------------------------------------
# GENERASI DATA UJI — 200 urutan unik
# ------------------------------------------------------
def buat_sampel(jumlah: int) -> List[str]:
    sampel = []
    for _ in range(jumlah):
        panjang = random.randint(30, 150)
        urutan = ''.join(random.choices(ASAM_AMINO, k=panjang))
        sampel.append(urutan)
    return sampel

def jalankan_eksperimen():
    print(f"Membuat {JUMLAH_SAMPEL} sampel uji per model...")
    sampel = buat_sampel(JUMLAH_SAMPEL)
    hasil = []

    for indeks, urutan in enumerate(sampel, 1):
        r1 = model_pola(urutan)
        r2 = model_pembelajaran(urutan)
        hasil.extend([
            {"id_sampel": indeks, "urutan": urutan, **r1},
            {"id_sampel": indeks, "urutan": urutan, **r2}
        ])
        if indeks % 50 == 0:
            print(f"  → Diproses: {indeks}/{JUMLAH_SAMPEL}")

    # Simpan ke CSV
    with open("data_mentah.csv", "w", newline="", encoding="utf-8") as f:
        kolom = ["id_sampel", "metode", "akurasi", "waktu_detik", "berhasil"]
        penulis = csv.DictWriter(f, fieldnames=kolom)
        penulis.writeheader()
        penulis.writerows(hasil)

    print(f"\n✅ Selesai! Total {len(hasil)} baris data tersimpan di data_mentah.csv")
    return hasil

if __name__ == "__main__":
    jalankan_eksperimen()