import streamlit as st
import base64

def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def show():
    #Hero
    img_base64 = get_base64_image("static/hero_background.jpg")
    st.markdown(
        f"""
        <style>

        .hero-section {{
            position: relative;
            width: 100%;  
            height: 100vh;   
            height: 70vh;
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover; /* gambar pas tanpa distorsi */
            background-position: center;
            background-repeat: no-repeat;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            overflow: hidden;
        }}

        .hero-overlay {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.65);
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            padding: 20px;
        }}

        .hero-content h1 {{
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
            margin-bottom: 20px;
        }}

        .hero-content p {{
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
            text-shadow: 1px 1px 6px rgba(0,0,0,0.7);
        }}
        </style>

        <div class="hero-section">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <h1>PENGELOMPOKAN WILAYAH DI INDONESIA</h1>
                <p>Clustering Wilayah di Indonesia Menggunakan <b>Intelligent K-Median</b> dan <b>K-Medoids</b></p>
            </div>
        </div>
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
            "Mulai Clustering Wilayah", 
            use_container_width=True,
            help="Mulai proses clustering kabupaten/kota di Indonesia"
        ):
            st.session_state.page = "clustering_wilayah"
            st.rerun()  


    st.markdown("<br>", unsafe_allow_html=True)
    
    #Indikator Clustering
    st.markdown(
        """
        <h2 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:30px;'>
            Indikator Clustering
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    indikator_clustering = [
        {
            "title": "Angka Harapan Hidup (AHH) Laki-laki",
            "description": "Rata-rata perkiraan usia yang dapat dicapai penduduk laki-laki, mencerminkan kualitas kesehatan dan kesejahteraan kelompok pria di suatu wilayah."
        },
        {
            "title": "Angka Harapan Hidup (AHH) Perempuan",
            "description": "Rata-rata perkiraan usia yang dapat dicapai penduduk perempuan, mencerminkan kualitas kesehatan dan kesejahteraan kelompok wanita di suatu wilayah."
        },
        {
            "title": "Persentase Penduduk Miskin (P0)",
            "description": "Proporsi penduduk yang berada di bawah garis kemiskinan. Indikator ini mengukur tingkat kemiskinan di suatu wilayah."
        },
        {
            "title": "Rata-rata Lama Sekolah (RLS)",
            "description": "Rata-rata jumlah tahun pendidikan formal yang ditempuh oleh penduduk usia 25 tahun ke atas, mencerminkan tingkat pendidikan."
        },
        {
            "title": "Indeks Kedalaman Kemiskinan (P1)",
            "description": "Mengukur seberapa jauh rata-rata pendapatan penduduk miskin dari garis kemiskinan. Semakin tinggi nilainya, semakin dalam kemiskinannya."
        },
        {
            "title": "Indeks Keparahan Kemiskinan (P2)",
            "description": "Mengukur ketimpangan pengeluaran di antara penduduk miskin. Nilai yang tinggi menunjukkan adanya kesenjangan yang besar."
        }
    ]
    
    st.markdown("""
    <style>
    .info-card {
        background-color: #0e1117;
        border: 2px solid #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        transition: all 0.3s ease-in-out;
    }
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(77, 166, 255, 0.2);
        border-color: #4da6ff;
    }
    .info-card h3 {
        color: #4da6ff;
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.2em;
    }
    .info-card p {
        text-align: justify;
        margin-bottom: 0;
        color: #fafafa;
        font-size: 0.95em;
    }
    </style>
    """, unsafe_allow_html=True)

    for i in range(0, len(indikator_clustering), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(indikator_clustering):
                with cols[j]:
                    indicator = indikator_clustering[i+j]
                    st.markdown(
                        f"""
                        <div class="info-card">
                            <h3>{indicator['title']}</h3>
                            <p>{indicator['description']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

    
    st.markdown("<br>", unsafe_allow_html=True)
    
    #Metode Clustering
    st.markdown(
        """
        <h2 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:30px;'>
            Metode Clustering
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    metode_clustering = [
        {
            "title": "Intelligent K-Median",
            "description": "Sebuah pengembangan dari algoritma K-Median yang memilih medoid (titik pusat) awal secara cerdas, bukan acak. Tujuannya adalah untuk menghasilkan cluster yang lebih stabil, akurat, dan mempercepat proses konvergensi."
        },
        {
            "title": "K-Medoids",
            "description": "Algoritma ini mengelompokkan data dengan memilih titik data aktual sebagai pusat cluster (medoid). Metode ini lebih tangguh terhadap noise dan outlier dibandingkan K-Means yang menggunakan rata-rata sebagai pusat cluster."
        }
    ]
    
    cols = st.columns(2)
    for i in range(len(metode_clustering)):
        with cols[i]:
            metode = metode_clustering[i]
            st.markdown(
                f"""
                <div class="info-card">
                    <h3>{metode['title']}</h3>
                    <p>{metode['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
