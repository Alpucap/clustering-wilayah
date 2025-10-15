import streamlit as st

def show():
    #Hero
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            PENGELOMPOKAN WILAYAH DI INDONESIA BERDASARKAN<br>
            ANGKA HARAPAN HIDUP, TINGKAT KEMISKINAN, DAN RATA-RATA LAMA SEKOLAH
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <p style='text-align: center; font-size: 18px; color: gray; padding-bottom:50px; margin-bottom:40px;'>
            Clustering Wilayah di Indonesia Menggunakan <b>Intelligent K-Median</b> dan <b>K-Medoids</b>
        </p>
        """,
        unsafe_allow_html=True
    )
    
    #Description
    st.markdown(
        """
        <p style='text-align: justify; font-size: 16px; padding-top:30px;'>
        Website ini bertujuan untuk mengelompokkan kabupaten/kota di Indonesia berdasarkan 
        <b style="color:#4da6ff;">Angka Harapan Hidup (AHH)</b>, 
        <b style="color:#4da6ff;">Persentase Penduduk Miskin (P0)</b>, 
        <b style="color:#4da6ff;">Rata-rata Lama Sekolah (RLS)</b>, 
        <b style="color:#4da6ff;">Indeks Kedalaman Kemiskinan (P1)</b>, dan 
        <b style="color:#4da6ff;">Indeks Keparahan Kemiskinan (P2)</b>. Dengan menggunakan metode <b style="color:#4da6ff;">Intelligent K-Median</b> dan 
        <b style="color:#4da6ff;">K-Medoids</b>, hasil pengelompokan kabupaten/kota disajikan melalui 
        visualisasi interaktif agar pengguna dapat lebih mudah memahami pola distribusi kesejahteraan 
        dan kondisi sosial-ekonomi antarwilayah di Indonesia.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    
    #CTA Button untuk ke Halaman Clustering Wilayah
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Mulai Clustering", 
            use_container_width=True,
            help="Mulai proses clustering kabupaten/kota di Indonesia"
        ):
            st.session_state.page = "clustering_wilayah"
            st.rerun()  


    st.markdown("<br>", unsafe_allow_html=True)
