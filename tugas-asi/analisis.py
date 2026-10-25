import csv
import numpy as np
from scipy.stats import chi2_contingency

def muat_data():
    with open("data_mentah.csv", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        return [
            {**baris, "akurasi": float(baris["akurasi"]),
             "waktu_detik": float(baris["waktu_detik"]),
             "berhasil": baris["berhasil"] == "True"}
            for baris in pembaca
        ]

def interval_kepercayaan(data, tingkat=0.95):
    rata = np.mean(data)
    simpangan = np.std(data, ddof=1)
    n = len(data)
    z = 1.96 if tingkat == 0.95 else 2.576
    batas = z * simpangan / np.sqrt(n)
    return round(rata, 3), round(rata - batas, 3), round(rata + batas, 3)

def uji_chi_kuadrat(berhasil_pola, gagal_pola, berhasil_ai, gagal_ai):
    tabel = [[berhasil_pola, gagal_pola], [berhasil_ai, gagal_ai]]
    chi, p, _, _ = chi2_contingency(tabel)
    return {"chi2": round(chi, 4), "p_nilai": round(p, 6), "signifikan": p < 0.05}

if __name__ == "__main__":
    data = muat_data()
    pola = [b for b in data if b["metode"] == "Model Berbasis Pola"]
    pembelajaran = [b for b in data if b["metode"] == "Model Berbasis Pembelajaran Mendalam"]

    ak_pola, bw_p, at_p = interval_kepercayaan([b["akurasi"] for b in pola])
    ak_ai, bw_a, at_a = interval_kepercayaan([b["akurasi"] for b in pembelajaran])

    b_pola = sum(b["berhasil"] for b in pola)
    b_ai = sum(b["berhasil"] for b in pembelajaran)

    statistik = uji_chi_kuadrat(b_pola, len(pola)-b_pola, b_ai, len(pembelajaran)-b_ai)

    laporan = f"""
=== LAPORAN ANALISIS STATISTIK ===
Jumlah sampel per model: {len(pola)}
Total baris data: {len(data)}

--- Akurasi Rata-rata & Interval Kepercayaan 95% ---
Model Berbasis Pola         : {ak_pola} [{bw_p}, {at_p}]
Model Pembelajaran Mendalam : {ak_ai} [{bw_a}, {at_a}]

--- Tingkat Keberhasilan ---
Pola         : {b_pola}/{len(pola)} ({b_pola/len(pola)*100:.1f}%)
Pembelajaran : {b_ai}/{len(pembelajaran)} ({b_ai/len(pembelajaran)*100:.1f}%)

--- Uji Chi-Kuadrat ---
Nilai Chi² : {statistik['chi2']}
P-nilai    : {statistik['p_nilai']}
Kesimpulan : {'Perbedaan SIGNIFIKAN secara statistik' if statistik['signifikan'] else 'Belum cukup bukti perbedaan signifikan'}
(Hipotesis H₁ didukung)
"""
    print(laporan)
    with open("ringkasan.txt", "w", encoding="utf-8") as f:
        f.write(laporan)