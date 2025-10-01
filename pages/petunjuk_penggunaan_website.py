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
        Halaman ini memandu pengguna memahami indikator yang digunakan — 
        <b>Angka Harapan Hidup (AHH)</b>, <b>Persentase Penduduk Miskin (P0)</b>, 
        <b>Indeks Kedalaman Kemiskinan (P1)</b>, <b>Indeks Keparahan Kemiskinan (P2)</b>, 
        serta <b>Rata-rata Lama Sekolah (RLS)</b> — serta cara menjalankan proses clustering. 
        Dengan mengikuti petunjuk ini, pengguna dapat langsung mencoba analisis dan melihat hasil 
        pengelompokan kabupaten/kota di Indonesia berdasarkan kondisi sosial-ekonomi.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    #Buku Manual (Petunjuk Penggunaan Website)
    with open("assets/files/DummyWord.docx", "rb") as file_petunjuk_penggunaan:
        st.download_button(
            label="Petunjuk Penggunaan Website",
            data=file_petunjuk_penggunaan,
            file_name="Buku Manual.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    #QnA
    with st.expander("Apa itu Angka Harapan Hidup (AHH)?"):
        st.write(
            "AHH adalah rata-rata perkiraan banyak tahun yang dapat ditempuh oleh seseorang sejak lahir, "
            "dengan asumsi pola mortalitas saat ini tetap berlaku. Indikator ini merepresentasikan tingkat kesehatan masyarakat."
        )

    with st.expander("Apa itu Persentase Penduduk Miskin (P0)?"):
        st.write(
            "P0 adalah persentase penduduk yang hidup di bawah garis kemiskinan pada suatu wilayah. "
            "Indikator ini mencerminkan tingkat kemiskinan absolut."
        )

    with st.expander("Apa itu Indeks Kedalaman Kemiskinan (P1)?"):
        st.write(
            "P1 mengukur rata-rata kesenjangan pengeluaran penduduk miskin terhadap garis kemiskinan. "
            "Semakin tinggi nilainya, semakin jauh rata-rata pengeluaran penduduk miskin dari garis kemiskinan."
        )

    with st.expander("Apa itu Indeks Keparahan Kemiskinan (P2)?"):
        st.write(
            "P2 mengukur tingkat ketimpangan pengeluaran di antara penduduk miskin. "
            "Semakin tinggi nilainya, semakin besar kesenjangan antarpenduduk miskin di bawah garis kemiskinan."
        )

    with st.expander("Apa itu Rata-rata Lama Sekolah (RLS)?"):
        st.write(
            "RLS adalah rata-rata jumlah tahun penduduk berusia 25 tahun ke atas telah menempuh pendidikan formal. "
            "Indikator ini merepresentasikan kondisi pendidikan suatu wilayah."
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

    with st.expander("Bagaimana cara menggunakan clustering wilayah?"):
        st.write(
            """
            1. Upload dataset (.xlsx).  
            2. Pilih metode clustering.  
            3. Tentukan jumlah cluster dan periode data.  
            4. Jalankan analisis.  
            5. Lihat hasil pada halaman Hasil Clustering.  
            6. Unduh hasil analisis jika diperlukan.  
            """
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Mulai Clustering"):  
                st.session_state.page = "clustering"
                st.rerun()