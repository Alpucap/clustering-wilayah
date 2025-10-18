import streamlit as st
import pandas as pd
from database import SessionLocal
from models import ActivityLog
from api.clustering.load_data import load_dataset, validate_dataset, filter_and_select_data
from api.clustering.run_clustering import run_clustering

def show():
    #Title
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            PENGELOMPOKAN WILAYAH DI INDONESIA
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    #Description
    st.markdown(
        """
        <p style='text-align: justify; padding-top:30px; padding-bottom:20px;'>
            Setelah memahami indikator yang digunakan dalam pengelompokan wilayah—yaitu 
            <b>Angka Harapan Hidup (AHH)</b> laki-laki & perempuan, 
            <b>Persentase Penduduk Miskin (P0)</b>, 
            <b>Rata-rata Lama Sekolah (RLS)</b>, 
            <b>Indeks Kedalaman Kemiskinan (P1)</b>, serta 
            <b>Indeks Keparahan Kemiskinan (P2)</b>—proses clustering dapat langsung dilakukan 
            menggunakan data yang tersedia.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    #Upload File
    st.markdown(
        """
        <p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'> 
        Upload Dataset
        </p>
        """,
        unsafe_allow_html=True
    )
    
    file_dataset = st.file_uploader(
        "Unggah file dataset dalam format Excel (.xlsx)",
        type=["xlsx"],
        help="Pastikan format dataset sesuai template yang disediakan."
    )
    st.caption("Hanya berkas Excel (.xlsx) yang didukung.")
    
    if file_dataset is None:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            with open("assets/files/Template_Dataset_Clustering_Wilayah.xlsx", "rb") as template_dataset:
                st.download_button(
                    label="Belum Punya Dataset? Download Template Dataset",
                    data=template_dataset,
                    file_name="template_dataset_clustering_wilayah.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        with col2:
            with open("assets/files/DummyWord.docx", "rb") as file_petunjuk_penggunaan:
                st.download_button(
                    label="Panduan Pengisian Template Dataset",
                    data=file_petunjuk_penggunaan,
                    file_name="Panduan_Pengisian_Dataset.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

    
    #Load & Validate dataset
    df_clustering_wilayah = None
    if file_dataset is not None:
        try:
            df_clustering_wilayah = load_dataset(file_dataset)   
            validate_dataset(df_clustering_wilayah)                
            st.success("Dataset berhasil dimuat!")
        except Exception as e:
            st.error(f"Dataset tidak valid: {e}")
            return 

    if df_clustering_wilayah is not None:
        st.markdown(
            """
            <p style='padding-top:16px; padding-bottom:4px; font-size: 20px; font-weight: bold;'> 
            Dataset yang di upload
            </p>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_clustering_wilayah)
        st.write(f"Dataset berisi **{df_clustering_wilayah.shape[0]} baris** dan **{df_clustering_wilayah.shape[1]} kolom**.")
        
    
    #Pilih Metode
    st.markdown("<p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'>Pilih Metode</p>", unsafe_allow_html=True)
    metode_clustering = st.selectbox(
        "Pilih Metode Clustering", 
        ["Intelligent K-Median", "K-Medoids"],
        help="Pilih metode clustering yang digunakan."
    )

    #Pilih Fitur
    mapping_fitur = {
        "Angka Harapan Hidup Laki-Laki (AHH_L)": "AHH_L",
        "Angka Harapan Hidup Perempuan (AHH_P)": "AHH_P",
        "Rata-rata Lama Sekolah (RLS)": "RLS",
        "Persentase Penduduk Miskin (P0)": "P0",
        "Indeks Kedalaman Kemiskinan (P1)": "P1",
        "Indeks Keparahan Kemiskinan (P2)": "P2",
    }

    label_fitur = [
        ["Angka Harapan Hidup Laki-Laki (AHH_L)", "Angka Harapan Hidup Perempuan (AHH_P)", "Rata-rata Lama Sekolah (RLS)", "Persentase Penduduk Miskin (P0)", "Indeks Kedalaman Kemiskinan (P1)", "Indeks Keparahan Kemiskinan (P2)"],
        ["Angka Harapan Hidup Laki-Laki (AHH_L)", "Angka Harapan Hidup Perempuan (AHH_P)", "Rata-rata Lama Sekolah (RLS)"],
        ["Angka Harapan Hidup Laki-Laki (AHH_L)", "Angka Harapan Hidup Perempuan (AHH_P)", "Persentase Penduduk Miskin (P0)", "Indeks Kedalaman Kemiskinan (P1)", "Indeks Keparahan Kemiskinan (P2)"],
        ["Rata-rata Lama Sekolah (RLS)", "Persentase Penduduk Miskin (P0)", "Indeks Kedalaman Kemiskinan (P1)", "Indeks Keparahan Kemiskinan (P2)"],
        ["Angka Harapan Hidup Laki-Laki (AHH_L)", "Angka Harapan Hidup Perempuan (AHH_P)"],
        ["Persentase Penduduk Miskin (P0)", "Indeks Kedalaman Kemiskinan (P1)", "Indeks Keparahan Kemiskinan (P2)"],
        ["Rata-rata Lama Sekolah (RLS)"],
        ["Angka Harapan Hidup Laki-Laki (AHH_L)"],
        ["Angka Harapan Hidup Perempuan (AHH_P)"],
        ["Persentase Penduduk Miskin (P0)"],
        ["Indeks Kedalaman Kemiskinan (P1)"],
        ["Indeks Keparahan Kemiskinan (P2)"],
    ]
    
    st.markdown("<p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'>Pilih Fitur</p>", unsafe_allow_html=True)
    mode_fitur = st.radio("Opsi pemilihan fitur:", ["Gunakan Preset", "Pilih Sendiri (Custom)"], horizontal=True)

    if mode_fitur == "Gunakan Preset":
        preset_options = [", ".join(fitur_group) for fitur_group in label_fitur]
        fitur_preset_str = st.selectbox(
            "Pilih kombinasi fitur untuk clustering",
            preset_options,
            help="Pilih indikator yang akan digunakan dalam clustering."
        )
        fitur_labels = [label.strip() for label in fitur_preset_str.split(",")]

    else:
        fitur_labels = st.multiselect(
            "Pilih fitur yang ingin digunakan",
            list(mapping_fitur.keys()),
            default=["Angka Harapan Hidup Laki-Laki (AHH_L)", "Angka Harapan Hidup Perempuan (AHH_P)"]
        )

    fitur_digunakan = [mapping_fitur[label] for label in fitur_labels]

    #Pilih Tahun
    st.markdown("<p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'>Pilih Tahun</p>", unsafe_allow_html=True)

    tahun_list = []

    if df_clustering_wilayah is not None and "Tahun" in df_clustering_wilayah.columns:
        tahun_list = sorted(df_clustering_wilayah["Tahun"].dropna().astype(int).unique())
    else:
        tahun_list = ["Silakan unggah dataset terlebih dahulu"]

    col1, col2 = st.columns(2)
    with col1:
        tahun_awal = st.selectbox("Tahun Awal", tahun_list, index=0)
    with col2:
        tahun_akhir = st.selectbox("Tahun Akhir", tahun_list, index=len(tahun_list)-1)

    if isinstance(tahun_awal, int) and isinstance(tahun_akhir, int):
        if tahun_awal > tahun_akhir:
            st.error("Tahun awal tidak boleh lebih besar dari tahun akhir.")


    #Pilih Jumlah Cluster
    if metode_clustering == "K-Medoids":
        st.markdown("<p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'>Pilih Jumlah Cluster (K)</p>", unsafe_allow_html=True)
        jumlah_cluster = st.slider(
            "Pilih jumlah cluster (K)",
            min_value=2,
            max_value=11,
            value=3,
            step=1,
            help="Jumlah cluster untuk analisis."
        )
    else:
        jumlah_cluster = None

    #Pilih Metrik Jarak
    st.markdown("<p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'>Pilih Metrik Jarak</p>", unsafe_allow_html=True)
    metrik_jarak_label = st.selectbox(
        "Pilih Metrik Jarak",
        ["manhattan", "euclidean"],
        help="Metode perhitungan jarak."
    )

    metrik_jarak = "cityblock" if metrik_jarak_label == "manhattan" else metrik_jarak_label


    #Filter dan Select Dataset
    df_clustering_filtered = None
    if df_clustering_wilayah is not None:
        try:
            df_clustering_filtered = filter_and_select_data(
                df_clustering_wilayah,
                fitur_digunakan,
                tahun_awal,
                tahun_akhir
            )
        except Exception as e:
            st.error(f"Gagal memfilter dataset: {e}")
    
    #Ringkasan Pilihan User
    if df_clustering_filtered is not None:
        st.markdown("---")
        st.markdown("<p style='padding-top:16px; padding-bottom:4px; font-size: 28px; font-weight: bold;'>Ringkasan Pilihan Analisis</p>", unsafe_allow_html=True)
        fitur_display_html = "".join([f"<li>{label}</li>" for label in fitur_labels])

        if metode_clustering == "K-Medoids":
            cluster_html = f"<li>Jumlah Cluster (K): {jumlah_cluster}</li>"
        else:
            cluster_html = "" 

        st.markdown(f"""
        <ul>
        <li>Metode: {metode_clustering}</li>
        <li>Fitur:
            <ul>
            {fitur_display_html}
            </ul>
        </li>
        <li>Tahun: {tahun_awal} – {tahun_akhir}</li>
        {cluster_html}
        <li>Metrik Jarak: {metrik_jarak}</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown(
            """
            <p style='padding-top:16px; padding-bottom:4px; font-size: 20px; font-weight: bold;'> 
            Dataset yang dipilih
            </p>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_clustering_filtered)
        st.write(f"Dataset berisi **{df_clustering_filtered.shape[0]} baris** dan **{df_clustering_filtered.shape[1]} kolom**.")
        st.info(
            "Jika pilihan sudah sesuai, silakan klik tombol **Jalankan Clustering** di bawah "
            "untuk memproses dataset dan menampilkan hasil analisis."
        )
    
        #Jalankan Clustering
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Jalankan Clustering", use_container_width=True):
                if df_clustering_filtered is None:
                    st.error("Dataset belum siap. Pastikan file valid dan tahun/fitur sudah dipilih.")
                else:
                    result = run_clustering(df_clustering_filtered, fitur_digunakan, metode_clustering, jumlah_cluster, metrik_jarak)
                    
                    df_with_cluster = df_clustering_filtered.copy()
                    df_with_cluster["Cluster"] = result["df_hasil"]["Cluster"].values
                    
                    if "user_id" in st.session_state:
                        with SessionLocal() as db:
                            log = ActivityLog(
                                user_id=int(st.session_state["user_id"]),
                                metode_clustering=metode_clustering,
                                fitur_digunakan=fitur_labels,
                                tahun_awal=int(tahun_awal),
                                tahun_akhir=int(tahun_akhir),
                                jumlah_cluster=int(jumlah_cluster) if jumlah_cluster is not None else None,
                                metrik_jarak=metrik_jarak,
                                silhouette=str(result["silhouette"]),
                                dbi=str(result["dbi"]),
                                waktu_komputasi=str(result["waktu_komputasi"])
                            )
                            db.add(log)
                            db.commit()
                    
                    st.session_state.page = "hasil_clustering"
                    st.session_state.user_input = {
                        "dataset": result["df_processed"],    
                        "df_hasil": df_with_cluster,
                        "labels": result["labels"],         
                        "centroids": result["centroids"],    
                        "fitur_digunakan": fitur_digunakan,
                        "metode_clustering": metode_clustering,
                        "tahun_awal": tahun_awal,
                        "tahun_akhir": tahun_akhir,
                        "jumlah_k": jumlah_cluster,
                        "metrik_jarak": metrik_jarak,
                        "null_summary": result["null_summary"],
                        "jumlah_outlier": result["jumlah_outlier"],
                        "df_outliers": result["df_outliers"],
                        "dbi": result["dbi"],        
                        "silhouette": result["silhouette"],
                        "waktu_komputasi": result["waktu_komputasi"]
                    }
                    st.session_state["loading"] = True
                    st.rerun()

