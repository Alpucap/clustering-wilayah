import streamlit as st

def show():
    #Title
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            TENTANG WEBSITE
        </h1>
        """,
        unsafe_allow_html=True
    )

    #Description
    st.markdown(
        """
        <div style='text-align: justify; font-size:16px; padding-left:50px; padding-right:50px; white-space: normal; word-wrap: break-word;'>
            Kesenjangan kesejahteraan antarwilayah di Indonesia masih menjadi permasalahan yang tercermin dari variasi indikator kesehatan, pendidikan, dan kemiskinan. 
            Perbedaan ini tercermin dari variasi Angka Harapan Hidup (AHH) laki-laki dan perempuan, tingkat kemiskinan yang diukur melalui Persentase Penduduk Miskin (P0), 
            Indeks Kedalaman Kemiskinan (P1), Indeks Keparahan Kemiskinan (P2), serta capaian pendidikan melalui Rata-rata Lama Sekolah (RLS). 
            Kondisi ini erat kaitannya dengan pencapaian Sustainable Development Goals (SDGs), khususnya SDG 1 (No Poverty), SDG 3 (Good Health and Well-being), 
            dan SDG 4 (Quality Education). Untuk itu, diperlukan analisis pola dan karakteristik wilayah untuk memberikan pemahaman yang lebih mendalam mengenai disparitas antarwilayah. 
            Perancangan ini bertujuan untuk mengelompokkan kabupaten/kota di Indonesia berdasarkan lima variabel tersebut menggunakan algoritma Intelligent K-Median dan K-Medoids. 
            Intelligent K-Median digunakan karena mampu mengatasi kelemahan inisialisasi acak pada K-Median standar sekaligus lebih tahan terhadap outlier, 
            sedangkan K-Medoids dipilih sebagai pembanding yang juga menggunakan titik data aktual sebagai pusat cluster. 
            Dataset yang digunakan merupakan data sekunder dari Badan Pusat Statistik (BPS) untuk periode 2022–2024. 
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        s
        """,
        unsafe_allow_html=True
    )




