import streamlit as st

def show():
    #Title
    st.markdown(
        """
        <h1 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:20px;'>
            TENTANG PENULIS
        </h1>
        """,
        unsafe_allow_html=True
    )

    #Description
    st.markdown(
        """
        <p style='text-align: justify; font-size:16px; padding-left:50px; padding-right:50px;'>
        Saya <b>Hans Christian Handoto</b>, seorang mahasiswa Fakultas Teknologi Informasi Universitas Tarumanagara 
        dengan fokus penelitian pada bidang <i>data mining</i> dan <i>machine learning</i>. 
        Skripsi ini disusun sebagai bagian dari studi sarjana, dengan tujuan untuk menganalisis dan 
        mengelompokkan kabupaten/kota di Indonesia berdasarkan indikator sosial-ekonomi menggunakan 
        metode <b>Intelligent K-Median</b> dan <b>K-Medoids</b>.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align: justify; font-size:16px; padding-left:50px; padding-right:50px;'>
        Sebagai penutup, penulis juga mengembangkan portofolio pribadi yang berisi berbagai proyek, 
        pengalaman, dan karya yang telah dikerjakan. Untuk informasi lebih lanjut mengenai hasil karya 
        dan perjalanan penulis, silakan kunjungi tautan berikut.
        </p>
        """,
        unsafe_allow_html=True
    )

    #Portfolio Website Link
    st.markdown(
        """
        <p style='text-align: center; font-size:18px;'>
            <a href='https://hans-portfolios.vercel.app/' target='_blank' 
            style='text-decoration: none; font-weight: bold; color: #4da6ff;'>
            Kunjungi Portofolio Saya
            </a>
        </p>
        """,
        unsafe_allow_html=True
    )
