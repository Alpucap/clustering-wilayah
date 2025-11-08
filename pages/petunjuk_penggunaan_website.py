import streamlit as st

def show():
    #Title
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            PETUNJUK PENGGUNAAN WEBSITE
        </h1>
        """,
        unsafe_allow_html=True
    )

    #Description
    st.markdown(
        """
        <p style='text-align: justify; font-size: 16px;'>
        Untuk memahami cara menggunakan fitur <b>pengelompokan wilayah</b>, tidak perlu khawatir. 
        Website ini sudah dilengkapi dengan <b>Buku Manual</b> yang berisi penjelasan mengenai alur penggunaan, 
        mulai dari cara mengunggah dataset, memilih metode clustering, menentukan jumlah cluster, 
        hingga melihat hasil analisis dalam bentuk tabel, grafik, dan peta interaktif.  
        <br><br>
        Silakan unduh <b>Buku Manual</b> dengan klik tombol di bawah ini.
        </p>
        """,
        unsafe_allow_html=True
    )

    #Manual Book
    with open("assets/files/Manual_Book.pdf", "rb") as file_manual:
        st.download_button(
            label="Download Buku Manual / Panduan Website",
            data=file_manual,
            file_name="Manual_Book.pdf",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width= 'stretch'
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p>Selain melalui Buku Manual, panduan singkat penggunaan clustering wilayah juga tersedia langsung di bawah ini.</p>", unsafe_allow_html=True)
    
    #Cara Penggunaan
    with st.expander("Bagaimana cara menggunakan clustering wilayah?"):
        st.write(
            """
            1. Buka halaman **Clustering Wilayah** lalu unduh template dataset.  
            2. Lengkapi dataset sesuai format (Nama Wilayah, Tahun, AHH_L, AHH_P, P0, P1, P2, RLS) lalu unggah kembali ke website.  
            3. Setelah dataset berhasil diunggah, tentukan parameter clustering:  
                - Metode (Intelligent K-Median atau K-Medoids)  
                - Fitur yang digunakan (preset/manual)  
                - Rentang tahun analisis  
                - Jumlah cluster (khusus untuk K-Medoids)  
                - Metrik jarak  
            4. Klik tombol **Jalankan Clustering** untuk memproses data.  
            5. Lihat hasil pada halaman **Hasil Clustering** berupa tabel, ringkasan cluster, serta analisis.  
            6. Akses visualisasi tambahan (silhouette score, DBI, korelasi variabel, distribusi indikator, dan peta interaktif).  
            7. Unduh hasil clustering maupun visualisasi dalam format Excel, PDF, atau PNG sesuai kebutuhan.  
            """
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Mulai Clustering"):
                st.session_state.page = "clustering"
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
        
    
    #Pertanyaan Umum
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: justify; font-size: 16px;'>
        Berikut merupakan beberapa penjelasan dari indikator, metode, ataupun istilah 
        yang digunakan pada website ini.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    with st.expander("Apa itu Clustering?"):
        st.write(
            "Clustering adalah metode analisis data untuk mengelompokkan objek yang memiliki kemiripan karakteristik "
            "ke dalam satu kelompok (cluster), sehingga objek dalam satu cluster lebih mirip satu sama lain dibandingkan "
            "dengan objek di cluster lain. "
            "Dalam konteks website ini, clustering digunakan untuk mengelompokkan kabupaten/kota di Indonesia "
            "berdasarkan indikator kesehatan, pendidikan, dan kemiskinan."
        )

    with st.expander("Apa itu Angka Harapan Hidup (AHH)?"):
        st.write(
            "AHH adalah rata-rata perkiraan jumlah tahun yang dapat dijalani seseorang sejak lahir. "
            "Semakin tinggi AHH menunjukkan semakin baik kualitas kesehatan masyarakat suatu wilayah."
        )

    with st.expander("Apa itu Persentase Penduduk Miskin (P0)?"):
        st.write(
            "P0 adalah persentase penduduk yang hidup di bawah garis kemiskinan dibandingkan dengan total penduduk. "
            "Indikator ini menggambarkan tingkat kemiskinan di suatu wilayah."
        )

    with st.expander("Apa itu Indeks Kedalaman Kemiskinan (P1)?"):
        st.write(
            "P1 atau poverty gap index mengukur rata-rata jarak pengeluaran penduduk miskin terhadap garis kemiskinan. "
            "Semakin tinggi P1 berarti rata-rata penduduk miskin semakin jauh dari garis kemiskinan."
        )

    with st.expander("Apa itu Indeks Keparahan Kemiskinan (P2)?"):
        st.write(
            "P2 menunjukkan tingkat ketimpangan di antara penduduk miskin. "
            "Semakin tinggi P2 berarti semakin besar perbedaan tingkat kemiskinan antar rumah tangga miskin."
        )

    with st.expander("Apa itu Rata-rata Lama Sekolah (RLS)?"):
        st.write(
            "RLS adalah rata-rata jumlah tahun pendidikan formal yang ditempuh oleh penduduk usia 15 tahun ke atas. "
            "Semakin tinggi RLS menunjukkan semakin baik kualitas sumber daya manusia dari aspek pendidikan."
        )

    with st.expander("Apa itu Intelligent K-Median?"):
        st.write(
            "Intelligent K-Median adalah pengembangan dari metode K-Median dengan inisialisasi centroid yang lebih optimal, "
            "sehingga hasil clustering lebih stabil."
        )

    with st.expander("Apa itu K-Medoids?"):
        st.write(
            "K-Medoids adalah algoritma clustering mirip dengan K-Means, tetapi menggunakan objek aktual sebagai pusat cluster. "
            "Metode ini lebih tahan terhadap outlier dibandingkan K-Means."
        )
    
    with st.expander("Apa itu Silhouette Score?"):
        st.write(
            "Silhouette Score adalah metrik untuk mengukur kualitas clustering dengan menilai seberapa baik "
            "suatu objek dikelompokkan dalam cluster-nya dibandingkan dengan cluster lain. "
            "Nilai berkisar antara -1 hingga 1."
        )
        st.markdown(
            """
            **Interpretasi Silhouette Score:**
            - **0.71 - 1.00**: Struktur Kuat (cluster sangat terpisah dengan baik)
            - **0.51 - 0.70**: Struktur Sedang (cluster cukup terpisah)
            - **0.26 - 0.50**: Struktur Lemah (cluster kurang terpisah, coba metode lain)
            - **≤ 0.25**: Tidak Ada Struktur (cluster sangat overlap)
            
            Semakin mendekati 1, semakin baik kualitas clustering yang dihasilkan.
            """
        )
    
    with st.expander("Apa itu Davies-Bouldin Index (DBI)?"):
        st.write(
            "Davies-Bouldin Index (DBI) adalah metrik evaluasi clustering yang mengukur rasio rata-rata jarak "
            "dalam cluster terhadap jarak antar cluster. DBI membantu menilai seberapa kompak dan terpisah cluster-cluster yang terbentuk."
            "Semakin mendekati 0, semakin baik kualitas clustering yang dihasilkan."
        )
    
    with st.expander("Apa itu Metrik Jarak (Distance Metric)?"):
        st.write(
            "Metrik jarak adalah ukuran untuk menentukan tingkat kemiripan atau perbedaan antara dua titik data. "
            "Dalam algoritma clustering seperti K-Medoids dan K-Median, metrik jarak digunakan untuk menghitung seberapa dekat "
            "atau jauh suatu data dari pusat cluster (medoid/median). "
            "Pemilihan metrik jarak yang tepat sangat penting karena dapat memengaruhi hasil pengelompokan."
        )
        st.markdown(
            """
            **Beberapa metrik jarak umum yang digunakan antara lain:**
            - **Euclidean Distance**: Mengukur jarak lurus antar titik (jarak geometris).
            - **Manhattan Distance**: Mengukur jarak berdasarkan selisih absolut pada setiap dimensi.
            - **Minkowski Distance**: Generalisasi dari Euclidean dan Manhattan.
            """
        )

    with st.expander("Apa itu Euclidean Distance?"):
        st.write(
            "Euclidean Distance adalah metrik jarak paling umum digunakan dalam analisis clustering. "
            "Metrik ini menghitung jarak garis lurus antara dua titik dalam ruang berdimensi-n. "
            "Cocok digunakan jika skala data sudah seragam (tidak memiliki perbedaan satuan antar variabel)."
        )
        st.latex(r"d(i, j) = \sqrt{\sum_{k=1}^{n} (x_{ik} - x_{jk})^2}")
        st.markdown("**Keterangan:**")
        st.latex(r"d(i, j): \text{ jarak Euclidean antara objek } i \text{ dan } j")
        st.latex(r"x_{ik}, x_{jk}: \text{ nilai variabel ke-}k \text{ untuk objek } i \text{ dan } j")
        st.latex(r"n: \text{ jumlah variabel atau dimensi data}")

    with st.expander("Apa itu Manhattan Distance?"):
        st.write(
            "Manhattan Distance (sering disebut City Block Distance atau L1-norm) "
            "mengukur jarak antar titik dengan menjumlahkan selisih absolut tiap dimensi. "
            "Ibarat menghitung jarak di kota berbentuk kotak (seperti jalan Manhattan), bukan garis lurus. "
            "Metode ini lebih tahan terhadap outlier dibandingkan Euclidean Distance."
        )
        st.latex(r"d(i, j) = \sum_{k=1}^{n} |x_{ik} - x_{jk}|")
        st.markdown("**Keterangan:**")
        st.latex(r"d(i, j): \text{ jarak Manhattan antara objek } i \text{ dan } j")
        st.latex(r"x_{ik}, x_{jk}: \text{ nilai variabel ke-}k \text{ untuk objek } i \text{ dan } j")
        st.latex(r"n: \text{ jumlah variabel atau dimensi data}")
