import pandas as pd
from api.clustering.data_pre_processing import handle_duplicates, check_null, standardize_numeric, check_outlier, normalize_data
from api.clustering.implementasi_i_k_median import iterasi_i_k_median
from api.clustering.implementasi_k_medoids import iterasi_k_medoids
from api.clustering.evaluasi_clustering import evaluasi_cluster

#Method untuk menjalankan clustering
def run_clustering(df, fitur_digunakan, metode_clustering, jumlah_cluster, metrik_jarak):
    #Handle duplikat (pakai kombinasi Wilayah & Tahun biar aman)
    df_proc = handle_duplicates(df, key_cols=["Nama Wilayah", "Tahun"])
    if "Tahun" in df.columns:
        df_proc = df_proc.drop_duplicates(subset=["Nama Wilayah", "Tahun"], keep="first")

    #Standardisasi kolom numerik
    df_proc = standardize_numeric(df_proc, fitur_digunakan)

    #Cek missing values
    null_summary = check_null(df_proc)

    #Cek outlier
    jumlah_outlier, df_outliers = check_outlier(df_proc, fitur_digunakan)

    #Normalisasi
    df_proc = normalize_data(df_proc, fitur_digunakan)
    
    
    #Implementasi clustering
    data_matrix = df_proc[fitur_digunakan].values
    
    labels, centroids = None, None

    if metode_clustering == "Intelligent K-Median":
        labels, centroids = iterasi_i_k_median(data_matrix, metrik_jarak=metrik_jarak)

    elif metode_clustering == "K-Medoids":
        if jumlah_cluster is None:
            raise ValueError("jumlah cluster harus diisi untuk metode K-Medoids")
        labels, centroids = iterasi_k_medoids(data_matrix, jumlah_cluster, metrik_jarak=metrik_jarak)

    else:
        raise ValueError(f"Metode clustering '{metode_clustering}' belum diimplementasikan")
        
    
    df_hasil = df_proc.copy()
    df_hasil["Cluster"] = labels
    
    #Evaluasi Cluster
    dbi, sil = evaluasi_cluster(data_matrix, labels, metrik_jarak=metrik_jarak)
    
    #Return
    return {
        "df_processed": df_proc,
        "df_hasil": df_hasil,
        "labels": labels,
        "centroids": centroids,
        "null_summary": null_summary,
        "jumlah_outlier": jumlah_outlier,
        "df_outliers": df_outliers,
        "dbi": dbi,
        "silhouette": sil
    }
