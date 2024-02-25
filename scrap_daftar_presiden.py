import requests
import pandas as pd

# Versi: 24 Feb 2024 23:00:15 Progress: 630132 dari 823236 TPS (76.54%)
# Versi: 24 Feb 2024 23:00:15 Progress: 103790 dari 140457 TPS (73.89%) (jawa barat)

# detail presiden
"""
    "100025": {
        "ts": "2024-02-17 16:00:02",
        "nama": "H. ANIES RASYID BASWEDAN, Ph.D. - Dr. (H.C.) H. A. MUHAIMIN ISKANDAR",
        "warna": "#8CB9BD",
        "nomor_urut": 1
    },
"""
url = "https://sirekap-obj-data.kpu.go.id/pemilu/ppwp.json"
detail_presiden = requests.get(url).json()

# hasil perhitungan
"""
"chart": {
        "100025": 5747720,
        "100026": 10541920,
        "100027": 1782544,
        "persen": 70.74
    },
"""
url = "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/32.json"
hasil_perhitungan = requests.get(url).json()["chart"]

hasil_perhitungan_presiden = []
for id_pres in detail_presiden:
    detail = detail_presiden[id_pres]
    detail["id"] = id_pres

    detail["jumlah_suara"] = hasil_perhitungan[id_pres]
    hasil_perhitungan_presiden.append(detail)

pd.DataFrame(hasil_perhitungan_presiden).to_csv(
    "detail_suara_presiden.csv", index=False
)
