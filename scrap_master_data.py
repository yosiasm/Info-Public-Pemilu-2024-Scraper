# dpd https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json
# prov https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/32.json
# kab_kota https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/32/3204.json
# kec https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/32/3204/320444.json
# desa https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/32/3204/320444/3204442003.json
# tps https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpd/32/3204/320444/3204442003/3204442003008.json

import requests
import pandas as pd
import os
from tqdm import tqdm
import json

ROOT_URL = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp"
TARGET_PROVINSI = "JAWA BARAT"

# creat dir if not exists
MASTER_PROV_DIR = "master_prov"
MASTER_KAB_KOTA_DIR = "master_kab_kota"
MASTER_KEC_DIR = "master_kec"
MASTER_DESA_DIR = "master_desa"
MASTER_TPS_DIR = "master_tps"
os.makedirs(MASTER_PROV_DIR, exist_ok=True)
os.makedirs(MASTER_KAB_KOTA_DIR, exist_ok=True)
os.makedirs(MASTER_KEC_DIR, exist_ok=True)
os.makedirs(MASTER_DESA_DIR, exist_ok=True)
os.makedirs(MASTER_TPS_DIR, exist_ok=True)


# store dataframe as csv and json
def store_dataframe(df: pd.DataFrame, dir: str, kode: str):
    csv_filepath = f"{dir}/{kode}.csv"
    json_filepath = f"{dir}/{kode}.json"
    df.to_csv(csv_filepath, index=False)
    df.to_json(json_filepath, orient="records")


# check if data is exist
def check_data_exist(dir: str, kode: str) -> bool:
    return os.path.isfile(f"{dir}/{kode}.csv")


# load existing data
def load_data(dir: str, kode: str) -> pd.DataFrame:
    with open(f"{dir}/{kode}.json", "r") as r:
        return json.load(r)


# crawl data
def crawl(raw_url: str, dir: str, kode: str) -> dict:
    if not check_data_exist(dir, kode):
        url = f"{raw_url}/{kode}.json"
        return requests.get(url).json()
    else:
        return load_data(dir, kode)


# crawl daftar provinsi
kode_nasional = 0
daftar_prov = crawl(ROOT_URL, MASTER_PROV_DIR, kode_nasional)

# simpan data provinsi
df_prov = pd.DataFrame(daftar_prov)
store_dataframe(df_prov, MASTER_PROV_DIR, kode_nasional)

# iterasi tiap prov yang didapat
for _, prov in df_prov.iterrows():
    # skip yg bukan target provinsi
    if prov["nama"] != TARGET_PROVINSI:
        continue

    # crawl daftar kab kota
    nama_prov = prov["nama"]
    kode_prov = prov["kode"]
    prov_url = f"{ROOT_URL}"
    daftar_kabkota = crawl(prov_url, MASTER_KAB_KOTA_DIR, kode_prov)
    # simpan data kab kota
    df_kab_kota = pd.DataFrame(daftar_kabkota)
    df_kab_kota["provinsi"] = nama_prov
    df_kab_kota["kode_provinsi"] = kode_prov
    store_dataframe(df_kab_kota, MASTER_KAB_KOTA_DIR, kode_prov)

    # iterasi tiap kab kota yang didapat
    for _, kab_kota in tqdm(df_kab_kota.iterrows(), desc="Kota/Kabupaten"):
        # crawl daftar kec
        kode_kab_kota = kab_kota["kode"]
        nama_kab_kota = kab_kota["nama"]
        kab_kota_url = f"{prov_url}/{kode_prov}"  # root/32
        daftar_kec = crawl(kab_kota_url, MASTER_KEC_DIR, kode_kab_kota)  # root/32/3211
        # simpan data kecamatan
        df_kec = pd.DataFrame(daftar_kec)
        df_kec["provinsi"] = nama_prov
        df_kec["kode_provinsi"] = kode_prov
        df_kec["kab_kota"] = nama_kab_kota
        df_kec["kode_kab_kota"] = kode_kab_kota
        store_dataframe(df_kec, MASTER_KEC_DIR, kode_kab_kota)

        # iterasi tiap kec yang didapat
        for _, kec in df_kec.iterrows():
            # crawl daftar desa
            kode_kec = kec["kode"]
            nama_kec = kec["nama"]
            kec_url = f"{kab_kota_url}/{kode_kab_kota}"  # root/32/3211
            daftar_desa = crawl(kec_url, MASTER_DESA_DIR, kode_kec)
            # simpan data desa
            df_desa = pd.DataFrame(daftar_desa)
            df_desa["provinsi"] = nama_prov
            df_desa["kode_provinsi"] = kode_prov
            df_desa["kab_kota"] = nama_kab_kota
            df_desa["kode_kab_kota"] = kode_kab_kota
            df_desa["kecamatan"] = nama_kec
            df_desa["kode_kecamatan"] = kode_kec
            store_dataframe(df_desa, MASTER_DESA_DIR, kode_kec)

            # iterasi tiap desa yang didapat
            for _, desa in df_desa.iterrows():
                # crawl daftar tps
                kode_desa = desa["kode"]
                nama_desa = desa["nama"]
                desa_url = f"{kec_url}/{kode_kec}"
                daftar_tps = crawl(desa_url, MASTER_TPS_DIR, kode_desa)
                # simpan data tps
                df_tps = pd.DataFrame(daftar_tps)
                df_tps["provinsi"] = nama_prov
                df_tps["kode_provinsi"] = kode_prov
                df_tps["kab_kota"] = nama_kab_kota
                df_tps["kode_kab_kota"] = kode_kab_kota
                df_tps["kecamatan"] = nama_kec
                df_tps["kode_kecamatan"] = kode_kec
                df_tps["desa"] = nama_desa
                df_tps["kode_desa"] = kode_desa
                store_dataframe(df_tps, MASTER_TPS_DIR, kode_desa)
