materi.py
# -*- coding: utf-8 -*-
"""Membangun 150 butir uji keyakinan keliru (3 kondisi x 50 butir).
K1 = keyakinan keliru standar (pelaku tidak melihat pemindahan)
K2 = pengecoh akses perseptual melalui wadah tembus pandang (pelaku MELIHAT)
K3 = pembalikan (benda dikembalikan ke wadah awal)
"""
 
NAMA_M = ["Nurdin", "Bayu", "Iwan", "Farhan", "Rangga", "Yosef",
          "Tegar", "Bambang", "Surya", "Adit"]
NAMA_F = ["Sari", "Ratih", "Dewi", "Lestari", "Mila", "Putri",
          "Ayu", "Ningsih", "Rara", "Sinta"]
OBJEK = ["gula aren", "kacang mede", "koin loyang", "benang tenun", "baterai kecil",
         "kapur barus", "butir merica", "kunci loyang", "pita merah", "bola karet"]
W_BURAM = ["kaleng biskuit", "kotak kayu", "keranjang rotan", "tas kain",
           "laci meja", "peti kecil"]
W_BENING = ["toples kaca bening", "kotak plastik transparan",
            "mangkok kaca", "akuarium kecil"]
LOK_A = ["dapur", "teras belakang", "gudang", "kamar depan", "kolong meja", "rak pojok"]
LOK_B = ["kamar mandi", "halaman belakang", "ruang tamu", "garasi",
         "kamar tengah", "balkon"]
 
 
def build():
    k1, k2, k3 = [], [], []
    for i in range(50):
        # rotasi agar tidak ada butir yang identik
        A = NAMA_M[i % 10] if i % 2 == 0 else NAMA_M[(i + 3) % 10]
        B = NAMA_F[i % 10] if i % 3 != 0 else NAMA_F[(i + 2) % 10]
        obj = OBJEK[(i + i // 10) % 10]
        w1 = W_BURAM[i % 6]
        w2 = W_BURAM[(i + 3) % 6]
        wb = W_BENING[i % 4]
        LA = LOK_A[i % 6]
        LB = LOK_B[(i + 1) % 6]
 
        # --- K1: keyakinan keliru standar ---
        k1.append({
            "id": "K1-%02d" % (i + 1),
            "teks": ("%s menaruh %s di dalam %s yang berada di %s, lalu pergi ke %s. "
                     "Selagi %s pergi, %s memindahkan %s ke dalam %s yang juga ada di %s. "
                     "%s kembali dan hendak mengambil %s. Menurut %s, di mana %s berada sekarang?"
                     % (A, obj, w1, LA, LB, A, B, obj, w2, LA, A, obj, A, obj)),
            "kunci": w1, "realitas": w2,
            "jenis": "keyakinan_keliru"})
 
        # --- K2: pengecoh akses perseptual (wadah tembus pandang) ---
        k2.append({
            "id": "K2-%02d" % (i + 1),
            "teks": ("%s menaruh %s di dalam %s yang tembus pandang dan berada di %s, "
                     "lalu duduk di %s yang berhadapan langsung dengan %s sehingga %s "
                     "masih dapat melihat isi %s dari jauh. Selagi %s duduk di %s, %s "
                     "memindahkan %s ke dalam %s yang juga ada di %s. %s kembali dan hendak "
                     "mengambil %s. Menurut %s, di mana %s berada sekarang?"
                     % (A, obj, wb, LA, LB, LA, A, wb, A, LB, B, obj, w2, LA, A, obj, A, obj)),
            "kunci": w2, "realitas": w2,
            "jenis": "akses_perseptual"})
 
        # --- K3: pembalikan (benda dikembalikan) ---
        k3.append({
            "id": "K3-%02d" % (i + 1),
            "teks": ("%s menaruh %s di dalam %s yang berada di %s, lalu pergi ke %s. "
                     "Selagi %s pergi, %s memindahkan %s ke dalam %s yang juga ada di %s, "
                     "tetapi kemudian mengembalikan %s ke dalam %s sebelum %s kembali. "
                     "%s kembali dan hendak mengambil %s. Menurut %s, di mana %s berada sekarang?"
                     % (A, obj, w1, LA, LB, A, B, obj, w2, LA, obj, w1, A, A, obj, A, obj)),
            "kunci": w1, "realitas": w1,
            "jenis": "pembalikan"})
    return k1, k2, k3
 
 
K1, K2, K3 = build()
SEMUA = {"K1": K1, "K2": K2, "K3": K3}
 
if __name__ == "__main__":
    for k, v in SEMUA.items():
        print(k, len(v))
        print(v[0]["teks"])
        print("--")
