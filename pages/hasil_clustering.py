import streamlit as st

def show():
    #Title
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            HASIL CLUSTERING
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    #Description
    st.markdown(
        """
        <p style='text-align: justify; padding-top:20px; padding-bottom:20px;'>
            Halaman ini menampilkan hasil pengelompokan wilayah berdasarkan indikator sosial-ekonomi.
            Visualisasi interaktif akan membantu pengguna memahami pola distribusi kesejahteraan 
            antar kabupaten/kota di Indonesia.
        </p>
        """,
        unsafe_allow_html=True
    )

    #Placeholder untuk grafik/hasil clustering
    st.info("📊 Hasil clustering akan muncul di sini setelah analisis dijalankan.")
