import pandas as pd

#Method untuk load dataset
def load_dataset(file):
    return pd.read_excel(file)

#Method untuk memvalidasi dataset
def validate_dataset(df):
    required_cols = ["Nama Wilayah", "Tahun", "AHH_L", "AHH_P", "RLS", "P0", "P1", "P2"]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Kolom wajib hilang: {missing_cols}")
    
    return True

#Method untuk memfilter dan memilih fitur
def filter_and_select_data(df, fitur, tahun_awal, tahun_akhir):
    df = df[(df["Tahun"] >= tahun_awal) & (df["Tahun"] <= tahun_akhir)]
    return df[["Nama Wilayah", "Tahun"] + fitur].copy()

