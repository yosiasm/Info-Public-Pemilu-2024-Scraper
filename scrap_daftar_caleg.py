"""
{
    "695854": {
        "nama": "AA ADE KADARISMAN, S.Sos., M.T.",
        "nomor_urut": 1,
        "jenis_kelamin": "L",
        "tempat_tinggal": "KAB. BANDUNG / JAWA BARAT"
    },
    "695855": {
        "nama": "AANYA RINA CASMAYANTI, S.E.",
        "nomor_urut": 2,
        "jenis_kelamin": "P",
        "tempat_tinggal": "KOTA BANDUNG / JAWA BARAT"
    },
"""

import requests
import pandas as pd

url = "https://sirekap-obj-data.kpu.go.id/pemilu/caleg/dpd/32.json"

data = requests.get(url).json()

data_reshape = []
for caleg_id in data:
    row = data[caleg_id]
    row["id"] = caleg_id
    data_reshape.append(row)

pd.DataFrame(data_reshape).to_csv("data_caleg.csv", index=False)
