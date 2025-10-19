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
    with open("assets/files/DummyWord.docx", "rb") as file_manual:
        st.download_button(
            label="Download Buku Manual / Panduan Website",
            data=file_manual,
            file_name="Buku_Manual_Skripsi.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: justify; font-size: 16px;'>
        Berikut merupakan beberapa penjelasan dari indikator, metode, ataupun istilah 
        yang digunakan pada website ini.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    #QnA
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