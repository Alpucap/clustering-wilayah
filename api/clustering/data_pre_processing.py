import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#Method untuk menghandle duplikat
def handle_duplicates(df, key_cols=["Nama Wilayah", "Tahun"]):
    df = df.copy()
    df["_non_na"] = df.notna().sum(axis=1)  
    df = df.sort_values(by="_non_na", ascending=False) 
    df = df.drop_duplicates(subset=key_cols, keep="first") 
    df = df.drop(columns=["_non_na"]) 
    return df.reset_index(drop=True)

#Method untuk standarisasi numerik
def standardize_numeric(df, kolom_numerik):
    for col in kolom_numerik:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(',', '.', regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

#Method untuk mengecek missing value
def check_null(df):
    null_counts = df.isnull().sum()
    null_summary = null_counts[null_counts > 0].reset_index()
    null_summary.columns = ["Kolom", "Jumlah Null"]
    return null_summary

#Method untuk mengecek outlier
def check_outlier(df, features):
    Q1 = df[features].quantile(0.25)
    Q3 = df[features].quantile(0.75)
    IQR = Q3 - Q1

    mask = ((df[features] < (Q1 - 1.5 * IQR)) |
            (df[features] > (Q3 + 1.5 * IQR))).any(axis=1)

    return mask.sum(), df[mask]

#Method untuk normalisasi data menggunakan Min-Max Normalization
def normalize_data(df, features):
    """
    Normalisasi data numerik menggunakan Min-Max Scaling (0–1).
    Return: DataFrame copy dengan fitur yang sudah ternormalisasi.
    """
    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[features] = scaler.fit_transform(df_normalized[features])
    return df_normalized