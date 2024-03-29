import pandas as pd
import glob
import os
from tqdm import tqdm

file_target = "all_perhitungan.csv"
perhitungan_file = glob.glob(os.path.join("perhitungan3", "*.csv"))

perhitungan_df = pd.concat(
    (pd.read_csv(f) for f in tqdm(perhitungan_file)), axis=0, ignore_index=True
)

perhitungan_df.to_csv(file_target, index=False)


print(
    len(perhitungan_df),
    "rows saved to",
    file_target,
    "from",
    len(perhitungan_file),
    "csv files",
)

correct_columns = [
    "kode_prov",
    "kode_kab_kota",
    "kode_kec",
    "kode_desa",
    "kode_tps",
    "prov",
    "kab_kota",
    "kecamatan",
    "desa",
    "tps",
    "null",
    "695854",
    "695855",
    "695856",
    "695857",
    "695858",
    "695859",
    "695860",
    "695861",
    "695862",
    "695863",
    "695864",
    "695865",
    "695866",
    "695867",
    "695868",
    "695869",
    "695870",
    "695871",
    "695872",
    "695873",
    "695874",
    "695875",
    "695876",
    "695877",
    "695878",
    "695879",
    "695880",
    "695881",
    "695882",
    "695883",
    "695884",
    "695885",
    "695886",
    "695887",
    "695888",
    "695889",
    "695890",
    "695891",
    "695892",
    "695893",
    "695894",
    "695895",
    "695896",
    "695897",
    "695898",
    "695899",
    "695900",
    "695901",
    "695902",
    "695903",
    "695904",
    "695905",
    "695906",
    "695907",
    "suara_sah",
    "suara_total",
    "pemilih_dpt_j",
    "pemilih_dpt_l",
    "pemilih_dpt_p",
    "pengguna_dpt_j",
    "pengguna_dpt_l",
    "pengguna_dpt_p",
    "pengguna_dptb_j",
    "pengguna_dptb_l",
    "pengguna_dptb_p",
    "suara_tidak_sah",
    "pengguna_total_j",
    "pengguna_total_l",
    "pengguna_total_p",
    "pengguna_non_dpt_j",
    "pengguna_non_dpt_l",
    "pengguna_non_dpt_p",
]
