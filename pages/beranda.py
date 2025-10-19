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
        .hero-clustering-section {{
            position: relative;
            width: 100%;  
            height: 70vh;
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            margin: 0 0 -150px 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            overflow: hidden;
        }}

        .hero-clustering-overlay {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.65);
        }}

        .hero-clustering-content {{
            position: relative;
            z-index: 1;
            padding: 20px;
        }}

        .hero-clustering-content h1 {{
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
            margin-bottom: 20px;
        }}

        .hero-clustering-content p {{
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto 30px auto;
            text-shadow: 1px 1px 6px rgba(0,0,0,0.7);
        }}
        
        div[data-testid="column"]:has(.cta-clustering-button) {{
            position: relative;
            z-index: 1000;
            margin-top: -150px;
        }}
        </style>

        <div class="hero-clustering-section">
            <div class="hero-clustering-overlay"></div>
            <div class="hero-clustering-content">
                <h1>PENGELOMPOKAN WILAYAH DI INDONESIA</h1>
                <p>Clustering Wilayah di Indonesia Menggunakan <b>Intelligent K-Median</b> dan <b>K-Medoids</b></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    #CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(
            "Mulai Eksplorasi Kota & Kabupaten di Indonesia", 
            use_container_width=True,
            help="Mulai proses clustering kabupaten/kota di Indonesia",
            key="btn_start_clustering"
        ):
            st.session_state.page = "clustering_wilayah"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    #Description
    st.markdown(
        """
        <div>
            <p style='text-align: justify; font-size: 16px; padding-top:50px;'>
            Website ini dirancang untuk <b style="color:#4da6ff;">mengelompokkan kabupaten/kota di Indonesia</b> 
            dengan menggunakan metode <b style="color:#4da6ff;">Intelligent K-Median</b> dan <b style="color:#4da6ff;">K-Medoids</b>. 
            Hasil analisis ditampilkan dalam bentuk <b style="color:#4da6ff;">tabel, grafik, dan peta interaktif</b>, 
            serta dievaluasi menggunakan <b style="color:#4da6ff;">Silhouette Coefficient</b> dan <b style="color:#4da6ff;">Davies-Bouldin Index (DBI)</b>. 
            Melalui pendekatan ini, pengguna tidak hanya melihat hasil pengelompokan wilayah, 
            tetapi juga dapat memperoleh berbagai <b style="color:#4da6ff;">manfaat</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    #Method untuk membuat section dengan cards
    def create_card_section(title, items, columns=3, show_title_in_card=True, show_section_title=True):
        if show_section_title:
            st.markdown(
                f"""
                <h2 style='text-align: center; font-weight: bold; padding-top:30px; padding-bottom:30px;'>
                    {title}
                </h2>
                """,
                unsafe_allow_html=True
            )
        
        #Untuk Manfaat Website
        if items and isinstance(items[0], str):
            cols = st.columns(columns, gap="medium")
            for idx, item in enumerate(items):
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div class="info-card" style="height: 100%; display: flex; align-items: center; justify-content: center;">
                            <p style="margin: 0; line-height: 1.6; text-align: center;">{item}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        #Untuk Indikator dan Metode
        else:
            for i in range(0, len(items), columns):
                cols = st.columns(columns, gap="medium")
                for j in range(columns):
                    if i + j < len(items):
                        with cols[j]:
                            item = items[i + j]
                            if show_title_in_card:
                                st.markdown(
                                    f"""
                                    <div class="info-card">
                                        <h3>{item['title']}</h3>
                                        <p>{item['description']}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
        
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)


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
        margin-bottom: 20px;
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
    
    /* Responsive button container */
    .button-container-responsive {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    @media (max-width: 768px) {
        .button-container-responsive {
            max-width: 100%;
            padding: 0 30px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    manfaat_data = [
        "Menyediakan penerapan algoritma clustering dalam bentuk sistem interaktif.",
        "Menampilkan hasil pengelompokan wilayah dalam bentuk tabel, grafik, dan peta interaktif.",
        "Memberikan informasi yang mudah diakses dan dipahami mengenai kondisi antarwilayah di Indonesia.",
        "Membantu mengidentifikasi pola kesamaan dan perbedaan antarwilayah dalam bentuk visualisasi dan pemetaan."
    ]

    indikator_data = [
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

    metode_data = [
        {
            "title": "Intelligent K-Median",
            "description": "Sebuah pengembangan dari algoritma K-Median yang memilih medoid (titik pusat) awal secara cerdas, bukan acak. Tujuannya adalah untuk menghasilkan cluster yang lebih stabil, akurat, dan mempercepat proses konvergensi."
        },
        {
            "title": "K-Medoids",
            "description": "Algoritma ini mengelompokkan data dengan memilih titik data aktual sebagai pusat cluster (medoid). Metode ini lebih tangguh terhadap noise dan outlier dibandingkan K-Means yang menggunakan rata-rata sebagai pusat cluster."
        }
    ]

    create_card_section(None, manfaat_data, columns=4, show_section_title=False)
    st.markdown("<br><br>", unsafe_allow_html=True)

    create_card_section("Indikator Clustering", indikator_data, columns=3)
    st.markdown("<br><br>", unsafe_allow_html=True)

    create_card_section("Metode Clustering", metode_data, columns=2)
    
    #Clustering Wilayah Button
    st.markdown("<div style='margin-top: 96px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(
            "Jalankan Pengelompokan Sekarang", 
            use_container_width=True,
            help="Mulai proses clustering kabupaten/kota di Indonesia",
            key="btn_start_clustering_bottom"
        ):
            st.session_state.page = "clustering_wilayah"
            st.rerun()