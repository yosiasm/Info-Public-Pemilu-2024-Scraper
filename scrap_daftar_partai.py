import requests
import pandas as pd

# Versi: 24 Feb 2024 23:07:05 Progress: 82324 dari 140457 TPS (58.61%) (jawa barat)
"""
 "1": 1091085,
 "2": 1512192,
"""
url = "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpr/32.json"
suara = requests.get(url).json()["chart"]

# detail partai
"""
"1": {
        "ts": "2024-02-17 16:00:02",
        "id_partai": 100001,
        "id_pilihan": 1,
        "is_aceh": false,
        "nama": "Partai Kebangkitan Bangsa",
        "nama_lengkap": "Partai Kebangkitan Bangsa",
        "nomor_urut": 1,
        "warna": "#00764A"
    }
"""
url = "https://sirekap-obj-data.kpu.go.id/pemilu/partai.json"
detail_partai = requests.get(url).json()

detail_suara_partai = []
for no_urut in suara:
    detail_partai[no_urut]["jumlah_suara"] = suara[no_urut]
    detail_suara_partai.append(detail_partai[no_urut])

pd.DataFrame(detail_suara_partai).to_csv("detail_suara_partai.csv", index=False)
