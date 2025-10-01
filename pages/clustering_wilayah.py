import streamlit as st

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
        <p style='text-align: justify; padding-top:16px; padding-bottom:4px; font-size: 36px; font-weight: bold;'> 
        Upload Dataset
        </p>
        """,
        unsafe_allow_html=True
    )
    
    file_dataset = st.file_uploader(
        "Click or drag file to this area to upload",
        type=["xlsx"],
        help="Hanya berkas Excel (.xlsx) yang didukung."
    )
    
    st.write("Hanya berkas Excel (.xlsx) yang didukung.")

    st.write("Belum punya berkas? Unduh template dataset.")

    with open("assets/files/DummyExcel.xlsx", "rb") as template_dataset:
        st.download_button(
            label="Download Template Dataset",
            data=template_dataset,
            file_name="template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    
    #Pilih Metode
    st.markdown(
        """
        <p style='text-align: justify; padding-top:16px; padding-bottom:4px; font-size: 36px; font-weight: bold;'> 
        Pilih Metode
        </p>
        """,
        unsafe_allow_html=True
    )
    
    metode_clustering = st.selectbox(
        "Pilih Metode", 
        ["Intelligent K-Median", "K-Medoids"],
        help="Jumlah cluster untuk analisis.",
    )
    
    #Pilih Jumlah Cluster (K)
    st.markdown(
        """
        <p style='text-align: justify; padding-top:16px; padding-bottom:4px; font-size: 36px; font-weight: bold;'> 
        Pilih Jumlah Cluster (K)
        </p>
        """,
        unsafe_allow_html=True
    )
    
    jumlah_cluster = st.slider(
        "Pilih jumlah cluster (K)",
        min_value=2,
        max_value=11,
        value=3,
        step=1,
        help="Jumlah cluster untuk analisis."
    )
    