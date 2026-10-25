analisis.py
# -*- coding: utf-8 -*-
"""Analisis hasil uji_tom.py.
 
Jalankan: python3 analisis.py data/hasil_tom.csv
Keluaran: tabel proporsi + CI Wilson, model efek campuran, McNemar, TOST.
"""
import sys
import numpy as np
import pandas as pd
from math import sqrt
from scipy import stats
import statsmodels.formula.api as smf
 
 
def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return p, max(0, c - h), min(1, c + h)
 
 
def main(path):
    df = pd.read_csv(path)
    df["benar"] = df["kategori"].str.startswith("benar_").astype(int)
 
    # 1. Proporsi benar per model x kondisi x instruksi + CI Wilson
    ringkas = []
    for kunci, g in df.groupby(["model", "kondisi", "skafold"]):
        k, n = int(g["benar"].sum()), len(g)
        p, lo, hi = wilson(k, n)
        ringkas.append({"model": kunci[0], "kondisi": kunci[1],
                        "skafold": kunci[2], "k": k, "n": n,
                        "proporsi": round(p, 3),
                        "ci95": "[%.3f, %.3f]" % (lo, hi)})
    out = pd.DataFrame(ringkas).sort_values(["model", "kondisi", "skafold"])
    print("\n=== Proporsi jawaban benar (CI Wilson 95%) ===")
    print(out.to_string(index=False))
    out.to_csv(path.replace(".csv", "_ringkas.csv"), index=False)
 
    # 2. Model efek campuran: benar ~ kondisi * skafold + (1|butir)
    print("\n=== Regresi logistik efek campuran ===")
    for m, g in df.groupby("model"):
        try:
            fit = smf.mixedlm("benar ~ C(kondisi) * skafold", g,
                              groups=g["butir"]).fit()
            print("\n[%s]" % m)
            print(fit.summary().tables[1])
        except Exception as e:  # noqa: BLE001
            print("[%s] gagal: %s" % (m, e))
 
    # 3. Uji ekuivalensi (TOST) untuk H2 pada margin delta = 0,15
    print("\n=== TOST H2 (margin 15 poin persentase) ===")
    for m, g in df.groupby("model"):
        a = g[(g.kondisi == "K1") & (g.skafold == 0)]["benar"]
        b = g[(g.kondisi == "K2") & (g.skafold == 0)]["benar"]
        d = a.mean() - b.mean()
        se = sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        lo = d - 1.96 * se
        hi = d + 1.96 * se
        setara = (lo > -0.15) and (hi < 0.15)
        print("%s: selisih=%.3f CI=[%.3f, %.3f] setara=%s"
              % (m, d, lo, hi, setara))
 
    # 4. McNemar untuk efek instruksi (berpasangan per butir)
    print("\n=== McNemar: skafold vs netral (kondisi pengecoh) ===")
    for m, g in df.groupby("model"):
        piv = (g[g.kondisi == "K2"]
               .pivot_table(index="butir", columns="skafold",
                            values="benar", aggfunc="mean"))
        if piv.shape[1] < 2:
            continue
        b_ = int(((piv[0] == 1) & (piv[1] == 0)).sum())
        c_ = int(((piv[0] == 0) & (piv[1] == 1)).sum())
        if b_ + c_ == 0:
            print("%s: tidak ada diskordan" % m)
            continue
        stat = (abs(b_ - c_) - 1) ** 2 / (b_ + c_)
        print("%s: b=%d c=%d chi2=%.3f p=%.4f"
              % (m, b_, c_, stat, 1 - stats.chi2.cdf(stat, 1)))
 
 
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/hasil_tom.csv")
 


