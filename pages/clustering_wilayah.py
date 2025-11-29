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
        <p style='text-align: justify; padding-top:20px; padding-bottom:20px;'>
            Setiap kota dan kabupaten di Indonesia memiliki kondisi sosial dan tingkat kemiskinan yang berbeda-beda. Perbedaan ini sering kali menimbulkan kesenjangan antarwilayah, sehingga penting untuk melihat bagaimana pola tersebut terbentuk. 
            Melalui pendekatan berbasis data, gambaran mengenai kondisi wilayah dapat dieksplorasi secara lebih jelas.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    #Petunjuk Penggunaan
    with st.expander("Petunjuk Penggunaan Website", expanded=False):
        st.markdown("""
        ### Alur Penggunaan Sistem

        **1. Upload Dataset**
        - Unggah dataset sesuai template Excel yang disediakan
        - Pastikan seluruh kolom terisi dan tidak ada data kosong
        - Dataset akan divalidasi secara otomatis oleh sistem

        **2. Pilih Metode Clustering**
        - **Intelligent K-Median** → metode otomatis dengan jumlah cluster optimal
        - **K-Medoids** → memungkinkan pengguna menentukan jumlah cluster (K)

        **3. Tentukan Fitur Analisis**
        - Gunakan **preset fitur** untuk kombinasi indikator yang telah disarankan
        - Atau pilih fitur secara manual sesuai kebutuhan analisis
        - Minimal satu fitur wajib dipilih

        **4. Tentukan Rentang Tahun**
        - Pilih tahun awal dan akhir berdasarkan dataset
        - Data akan difilter dan digabung sesuai rentang tahun

        **5. Pengaturan Tambahan**
        - Untuk K-Medoids, pengguna dapat menyesuaikan jumlah cluster (K)
        - Pilih metrik jarak yang sesuai (Manhattan atau Euclidean)

        **6. Jalankan Clustering**
        - Klik tombol **Jalankan Clustering**
        - Sistem akan memproses data dan menampilkan hasil clustering

        ---
        💡 **Tips Penggunaan**
        - Gunakan pengaturan default untuk hasil yang optimal
        - Kombinasi indikator pendidikan dan kemiskinan memberikan pola cluster yang lebih stabil
        - Rentang tahun yang lebih panjang memberikan gambaran kondisi wilayah yang lebih representatif
        """)

        st.markdown(
            "<p style='text-align:center; font-size:16px; margin-top:24px;'>"
            "Butuh penjelasan lebih lengkap? Klik tombol di dibawah ini"
            "</p>",
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button("Petunjuk Penggunaan Website Lengkap", use_container_width=True):
                st.session_state.page = "petunjuk_penggunaan_website"
                st.rerun()

    #Upload File
    st.markdown(
        """
        <p style='padding-top:16px; font-size: 28px; font-weight: bold;'> 
            Upload Dataset
        </p>
        <p style='color:#6c757d; font-size:16px; padding-bottom:4px;'>
        Silakan unggah dataset sesuai format yang tersedia untuk mulai mengeksplorasi kota/kabupaten di Indonesia.
        </p>
        """,
        unsafe_allow_html=True
    )
    #Pilihan sumber dataset
    dataset_option = st.radio(
        "Pilih sumber dataset:",
        ["Upload Dataset Sendiri", "Gunakan Dataset yang Disediakan"],
        index=0,
        horizontal=True
    )

    df_clustering_wilayah = None
    
    if dataset_option == "Upload Dataset Sendiri":
        file_dataset = st.file_uploader(
            "Silakan unggah file dataset dalam format Excel (.xlsx)",
            type=["xlsx"],
            help="Pastikan format dataset sesuai template yang disediakan."
        )
        st.caption("Hanya berkas Excel (.xlsx) yang didukung, maksimal 50 MB.")
        
        if file_dataset is None:
            col1, col2, col3 = st.columns([2, 1, 2]) 
            with col1:
                with open("assets/files/Template_Dataset_Clustering_Wilayah.xlsx", "rb") as template_dataset:
                    st.download_button(
                        label="Belum Punya Dataset? Download Template Dataset",
                        data=template_dataset,
                        file_name="template_dataset_clustering_wilayah.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        width= 'stretch'
                    )

            st.markdown(
                """
                **Petunjuk Pengisian Template Dataset**

                Template dataset diberikan dalam format `Excel (.xlsx)` dengan kolom sebagai berikut:
                - **Nama Wilayah** - Nama kabupaten/kota di Indonesia (gunakan format *Pascal Case*, contoh: `Kota Jakarta Barat`).
                - **Tahun** - Tahun data (misalnya `2022, 2023, 2024`).
                - **AHH_L** - Angka Harapan Hidup Laki-laki (rata-rata usia harapan hidup penduduk laki-laki).
                - **AHH_P** - Angka Harapan Hidup Perempuan (rata-rata usia harapan hidup penduduk perempuan).
                - **P0** - Persentase Penduduk Miskin (proporsi penduduk di bawah garis kemiskinan).
                - **P1** - Indeks Kedalaman Kemiskinan (mengukur seberapa jauh rata-rata penduduk miskin dari garis kemiskinan).
                - **P2** - Indeks Keparahan Kemiskinan (menggambarkan ketimpangan di antara penduduk miskin).
                - **RLS** - Rata-rata Lama Sekolah (jumlah rata-rata tahun pendidikan formal penduduk usia 25 tahun ke atas).


                **Ketentuan pengisian:**
                1. Setiap kolom wajib diisi lengkap sesuai format, jangan menambah/mengurangi kolom.
                2. Tidak boleh ada sel kosong pada baris data.
                3. Nama Wilayah harus sesuai format Pascal Case.
                4. Seluruh nilai indikator `AHH_L, AHH_P, P0, P1, P2, RLS` diisi dengan angka desimal.
                5. Simpan dataset dalam format `Excel (.xlsx)` sebelum diunggah ke website.
                """,
                unsafe_allow_html=False
            )

        if file_dataset is not None:
                    try:
                        df_clustering_wilayah = load_dataset(file_dataset)
                        
                        missing_count = df_clustering_wilayah.isnull().sum().sum()
                        if missing_count > 0:
                            st.error(f"Dataset tidak valid: terdapat {missing_count} data kosong. Pastikan semua sel terisi lengkap.")
                            df_clustering_wilayah = None
                        else:
                            validate_dataset(df_clustering_wilayah)
                            st.success("Dataset berhasil dimuat!")
                            
                    except Exception as e:
                        st.error(f"Dataset tidak valid: {e}")
                        df_clustering_wilayah = None
    else:
        df_clustering_wilayah = pd.read_excel("assets/files/Dataset_Clustering_Wilayah.xlsx")

    if df_clustering_wilayah is not None:
        st.markdown(
            """
            <p style='padding-top:16px; padding-bottom:4px; font-size: 20px; font-weight: bold;'> 
                Dataset yang digunakan
            </p>
            <p style='margin-top:4px; margin-bottom:12px; color:#6c757d; font-size:16px;'>
                Berikut adalah dataset yang berhasil diunggah dan siap digunakan.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_clustering_wilayah)
        st.write(f"Dataset berisi **{df_clustering_wilayah.shape[0]} baris** dan **{df_clustering_wilayah.shape[1]} kolom**.")
        
    
    #Pilih Metode
    st.markdown(
        """
        <p style='padding-top:16px; font-size: 28px; font-weight: bold;'> 
            Pilih Metode
        </p>
        <p style='color:#6c757d; font-size:16px; padding-bottom:4px;'>
        Metode clustering menentukan cara sistem mengelompokkan wilayah berdasarkan kemiripan indikator.
        </p>
        """,
        unsafe_allow_html=True
    )

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
        ["Persentase Penduduk Miskin (P0)", "Indeks Kedalaman Kemiskinan (P1)", "Indeks Keparahan Kemiskinan (P2)"]
    ]
    
    st.markdown(
        """
        <p style='padding-top:16px; font-size: 28px; font-weight: bold;'> 
            Pilih Fitur
        </p>
        <p style='color:#6c757d; font-size:16px; padding-bottom:4px;'>
        Fitur membantu sistem membandingkan wilayah berdasarkan indikator yang dipilih.
        </p>
        """,
        unsafe_allow_html=True
    )
    
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

    if len(fitur_labels) == 0:
        st.error("Fitur wajib dipilih! Silakan pilih minimal satu fitur untuk clustering.")
        fitur_digunakan = []
    else:
        fitur_digunakan = [mapping_fitur[label] for label in fitur_labels]

    #Pilih Tahun
    st.markdown(
        """
        <p style='padding-top:16px; font-size: 28px; font-weight: bold;'> 
            Pilih Tahun
        </p>
        <p style='color:#6c757d; font-size:16px; padding-bottom:4px;'>
        Rentang tahun menentukan periode data yang dianalisis dalam proses clustering.
        </p>
        """,
        unsafe_allow_html=True
    )

    if df_clustering_wilayah is not None and "Tahun" in df_clustering_wilayah.columns:
        tahun_list = sorted(df_clustering_wilayah["Tahun"].dropna().astype(int).unique())

        col1, col2 = st.columns(2)
        with col1:
            tahun_awal = int(st.selectbox("Tahun Awal", tahun_list, index=0))
        with col2:
            tahun_akhir = int(st.selectbox("Tahun Akhir", tahun_list, index=len(tahun_list)-1))

        if tahun_awal > tahun_akhir:
            st.error("Tahun awal tidak boleh lebih besar dari tahun akhir.")
    else:
        st.warning("Silakan unggah dataset terlebih dahulu untuk memilih tahun.")
        tahun_awal, tahun_akhir = None, None

    #Pilih Jumlah Cluster
    jumlah_cluster_optimal = 2
    if metode_clustering == "K-Medoids":
        st.markdown(
            """
            <p style='padding-top:16px; font-size: 28px; font-weight: bold;'> 
                Pilih Jumlah Cluster (K)
            </p>
            <p style='color:#6c757d; font-size:16px; padding-bottom:4px;'>
            Jumlah cluster menentukan banyaknya kelompok wilayah yang akan dibentuk.
            </p>
            """,
            unsafe_allow_html=True
        )
        
        mode_k = st.radio(
            "Pilih mode penentuan jumlah cluster:",
            ["Gunakan Jumlah Optimal", "Pilih Jumlah Cluster Sendiri"],
            index=0,
            horizontal=True,
            help=f"Mode optimal menggunakan K = {jumlah_cluster_optimal}, nilai yang memberikan performa terbaik menurut hasil evaluasi metrik clustering."
        )
        
        if mode_k == "Gunakan Jumlah Optimal":
            jumlah_cluster = jumlah_cluster_optimal
            st.markdown(f"""
            <div style='padding: 12px; background-color: #0e1117; border-left: 4px solid #4da6ff; margin-top: 10px; border-radius: 4px;'>
                <strong>Pengaturan Optimal Diterapkan</strong><br/>
                Jumlah cluster otomatis diatur ke <strong>K={jumlah_cluster_optimal}</strong> untuk hasil clustering terbaik.
            </div>
            """, unsafe_allow_html=True)
        else:
            jumlah_cluster = st.slider(
                "Pilih jumlah cluster (K)",
                min_value=2,
                max_value=6,
                value=jumlah_cluster_optimal,
                step=1,
                help=f"Jumlah cluster untuk analisis. K={jumlah_cluster_optimal} memberikan hasil optimal."
            )
            if jumlah_cluster != jumlah_cluster_optimal:
                st.warning(f"Anda memilih K={jumlah_cluster}. Hasil clustering mungkin tidak seoptimal K={jumlah_cluster_optimal}.")
    else:
        jumlah_cluster = None

    #Pilih Metrik Jarak
    st.markdown(
        """
        <p style='padding-top:16px; font-size: 28px; font-weight: bold;'> 
            Pilih Metrik Jarak
        </p>
        <p style='color:#6c757d; font-size:16px; padding-bottom:4px;'>
        Metrik jarak digunakan untuk mengukur tingkat kemiripan antarwilayah berdasarkan fitur terpilih.
        </p>
        """,
        unsafe_allow_html=True
    )

    if metode_clustering == "Intelligent K-Median":
        default_index = 0 #manhattan
        key_metric = "metric_ikmedian"
    else:
        default_index = 1 #euclidean
        key_metric = "metric_kmedoids"

    metrik_jarak_label = st.selectbox(
        "Pilih Metrik Jarak",
        ["manhattan", "euclidean"],
        index=default_index,
        key=key_metric,
        help="Metode perhitungan jarak."
    )
        
    metrik_jarak = "cityblock" if metrik_jarak_label == "manhattan" else metrik_jarak_label


    #Filter dan Select Dataset
    df_clustering_filtered = None
    if df_clustering_wilayah is not None and len(fitur_digunakan) > 0:
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
    if df_clustering_filtered is not None and len(fitur_digunakan) > 0:
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
            <p style='margin-top:4px; margin-bottom:12px; color:#6c757d; font-size:16px;'>
                Berikut adalah dataset berdasarkan parameter analisis yang dipilih.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_clustering_filtered)
        st.write(f"Dataset berisi **{df_clustering_filtered.shape[0]} baris** dan **{df_clustering_filtered.shape[1]} kolom**.")
        st.success(
            "Jika semua parameter sudah sesuai, silakan lanjutkan dengan menjalankan proses clustering."
        )
    
        #Jalankan Clustering
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Jalankan Clustering", width= 'stretch'):
                
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
                return
