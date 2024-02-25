# nama,id,kode,tingkat,provinsi,kode_provinsi,kab_kota,kode_kab_kota,kecamatan,kode_kecamatan,desa,kode_desa
# TPS 001,33653004,3201011001001,5,JAWA BARAT,32,BOGOR,3201,CIBINONG,320101,PONDOK RAJEG,3201011001
# TPS 002,33653005,3201011001002,5,JAWA BARAT,32,BOGOR,3201,CIBINONG,320101,PONDOK RAJEG,3201011001

# tps https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpd/32/3204/320444/3204442003/3204442003008.json
# {
#     "mode": "hhcw",
#     "chart": {
#         "null": null,
#         "695854": 2,
#         "695855": 9,
#         "695906": 3,
#         "695907": 0
#     },
#     "images": [
#         "https://sirekap-obj-formc.kpu.go.id/8233/pemilu/pdpd/32/04/44/20/07/3204442007006-20240216-114436--208734b7-c6f2-45d6-afd8-ec1a7d047898.jpg",
#     ],
#     "administrasi": {
#         "suara_sah": 170,
#         "suara_total": 181,
#         "pemilih_dpt_j": 208,
#         "pemilih_dpt_l": 103,
#         "pemilih_dpt_p": 105,
#         "pengguna_dpt_j": 178,
#         "pengguna_dpt_l": 82,
#         "pengguna_dpt_p": 96,
#         "pengguna_dptb_j": 0,
#         "pengguna_dptb_l": 0,
#         "pengguna_dptb_p": 0,
#         "suara_tidak_sah": 11,
#         "pengguna_total_j": 181,
#         "pengguna_total_l": 83,
#         "pengguna_total_p": 98,
#         "pengguna_non_dpt_j": 3,
#         "pengguna_non_dpt_l": 1,
#         "pengguna_non_dpt_p": 2
#     },
#     "psu": null,
#     "ts": "2024-02-16 21:59:27",
#     "status_suara": true,
#     "status_adm": true
# }

# null,695854,,695906,695907,kode_prov,kode_kab_kota,kode_kec,kode_desa,kode_tps,prov,kab_kota,kecamatan,desa,tps
# Versi: 17 Feb 2024 19:31:00 Progress: 73479 dari 140457 TPS (52.31%)
# Versi: 21 Feb 2024 19:01:07 Progress: 83864 dari 140457 TPS (59.71%)
# Versi: 24 Feb 2024 23:01:06 Progress: 89614 dari 140457 TPS (63.80%)


import pandas as pd
import glob
import os
import requests
from tqdm import tqdm
import time

DIR_TARGET = "perhitungan3"
all_files = glob.glob(os.path.join("master_tps", "*.csv"))
all_perhitungan = glob.glob(os.path.join(DIR_TARGET, "*.csv"))
all_perhitungan = [
    perhitungan.strip(".csv").strip(f"{DIR_TARGET}\\")
    for perhitungan in all_perhitungan
]

tps_df = pd.concat((pd.read_csv(f) for f in tqdm(all_files)), ignore_index=True)
tps_df_remaining = tps_df[~tps_df["kode"].astype(str).isin(all_perhitungan)]

tps_df_remaining_sample = tps_df_remaining.sample(frac=1).to_dict(orient="records")

for tps in tqdm(tps_df_remaining_sample):
    kode_prov = tps["kode_provinsi"]
    kode_kab_kota = tps["kode_kab_kota"]
    kode_kec = tps["kode_kecamatan"]
    kode_desa = tps["kode_desa"]
    kode_tps = tps["kode"]
    url = f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpd/{kode_prov}/{kode_kab_kota}/{kode_kec}/{kode_desa}/{kode_tps}.json"

    if os.path.isfile(f"{DIR_TARGET}/{kode_tps}.csv"):
        continue

    while True:
        try:
            perhitungan = requests.get(url, timeout=5).json()
            break
        except Exception as e:
            print(e)
            print("sleeping 10sec...")
            time.sleep(10)

    # chart
    chart = perhitungan["chart"]
    if not chart:
        chart = {}
    chart["kode_prov"] = kode_prov
    chart["kode_kab_kota"] = kode_kab_kota
    chart["kode_kec"] = kode_kec
    chart["kode_desa"] = kode_desa
    chart["kode_tps"] = kode_tps
    chart["prov"] = tps["provinsi"]
    chart["kab_kota"] = tps["kab_kota"]
    chart["kecamatan"] = tps["kecamatan"]
    chart["desa"] = tps["desa"]
    chart["tps"] = tps["nama"]

    # administrasi
    administrasi = perhitungan["administrasi"]
    if not administrasi:
        administrasi = {}

    perhitungan = {**chart, **administrasi}

    pd.DataFrame([perhitungan]).to_csv(f"{DIR_TARGET}/{kode_tps}.csv", index=False)
