uji_tom.py
# -*- coding: utf-8 -*-
"""Skrip uji perilaku model bahasa pada tugas keyakinan keliru (protokol Bagian 2).
 
Jalankan:  python3 uji_tom.py --model M1
Skrip hanya memanggil API resmi penyedia model. Tidak ada upaya melewati
pengaman model dan tidak ada konten berbahaya yang dihasilkan.
"""
 
import argparse
import csv
import hashlib
import json
import os
import random
import time
 
from materi import SEMUA  # K1, K2, K3 -> 50 butir per kondisi
 
SUHU = 0.0
ULANGAN = 3
JEDA = 1.5  # detik, untuk menghormati rate limit API
 
 
def sidik(teks: str) -> str:
    return hashlib.sha256(teks.encode("utf-8")).hexdigest()[:16]
 
 
def undi_opsi(item: dict, rng: random.Random) -> list:
    """Mengacak urutan pilihan jawaban agar bias posisi terukur."""
    opsi = [item["kunci"], item["realitas"]]
    if opsi[0] == opsi[1]:
        opsi = [item["kunci"], "di luar rumah"]
    rng.shuffle(opsi)
    return opsi
 
 
def prompt(item: dict, opsi: list, skafold: bool) -> str:
    inti = item["teks"] + "\n\nPilihan: (A) " + opsi[0] + " (B) " + opsi[1]
    if skafold:
        inti += ("\n\nSebelum menjawab, pertimbangkan secara eksplisit apa yang "
                 "diketahui dan tidak diketahui oleh tokoh utama pada saat ia kembali.")
    return inti + "\n\nJawab hanya dengan satu huruf: A atau B."
 
 
def panggil(model: str, teks: str) -> str:
    """Placeholder pemanggilan API resmi; isi sesuai penyedia yang dipakai."""
    raise NotImplementedError(
        "Hubungkan fungsi ini ke SDK resmi penyedia (mis. openai, anthropic, "
        "google-genai) dengan kunci API dari variabel lingkungan.")
 
 
def klasifikasi(jawaban: str, opsi: list, item: dict) -> str:
    huruf = jawaban.strip().upper()[:1]
    if huruf not in ("A", "B"):
        return "tidak_valid"
    pilih = opsi[0] if huruf == "A" else opsi[1]
    if pilih == item["kunci"]:
        return "benar_keyakinan"
    if pilih == item["realitas"]:
        return "benar_realitas"
    return "lain"
 
 
def jalan(model: str, keluaran: str) -> None:
    baris = []
    for kondisi, daftar in SEMUA.items():
        for item in daftar:
            for skafold in (False, True):
                for u in range(ULANGAN):
                    rng = random.Random(sidik(item["id"]) + u)
                    opsi = undi_opsi(item, rng)
                    t = prompt(item, opsi, skafold)
                    try:
                        jwb = panggil(model, t)
                    except NotImplementedError:
                        raise
                    except Exception as e:  # noqa: BLE001
                        jwb = "ERROR:" + type(e).__name__
                    baris.append({
                        "model": model, "butir": item["id"], "kondisi": kondisi,
                        "skafold": int(skafold), "ulangan": u,
                        "opsi_A": opsi[0], "opsi_B": opsi[1], "jawaban": jwb,
                        "kategori": klasifikasi(jwb, opsi, item),
                        "sidik_prompt": sidik(t)})
                    time.sleep(JEDA)
    with open(keluaran, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(baris[0].keys()))
        w.writeheader()
        w.writerows(baris)
    with open(keluaran.replace(".csv", "_meta.json"), "w") as f:
        json.dump({"model": model, "suhu": SUHU, "ulangan": ULANGAN,
                   "jumlah_trial": len(baris)}, f, indent=2)
 
 
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, help="ID model persis seperti di API")
    p.add_argument("--keluaran", default="hasil_tom.csv")
    a = p.parse_args()
    os.makedirs("data", exist_ok=True)
    jalan(a.model, os.path.join("data", a.keluaran))
 
