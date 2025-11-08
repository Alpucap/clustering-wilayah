import streamlit as st
import pandas as pd
from api.clustering.visualisasi_clustering import analisis_cluster, ringkasan_cluster, visualisasi_silhouette_full, visualisasi_tren_tahunan, analisis_silhouette_per_cluster, get_kategori_silhouette, visualisasi_scatter_per_pasangan_terpisah, tampilkan_figures_dalam_grid, visualisasi_boxplot_per_indikator_terpisah, heatmap_correlation, get_shapefile_from_drive, persiapkan_shapefile, tampilkan_peta, indikator_deskripsi
from api.hasil_clustering import fig_to_png_bytes, df_to_fig_table, figs_to_pdf, buat_peta_statis, loader
from streamlit_folium import st_folium
import io
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
import zipfile
import matplotlib.pyplot as plt

def show():
    #Inisialisasi
    
    #Download Visualisasi Clustering
    if "all_figs" not in st.session_state:
        st.session_state.all_figs = []
        
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
            Berikut merupakan hasil pengelompokan kota/kabupaten di Indonesia yang disajikan dalam bentuk tabel, berbagai visualisasi, 
            serta pemetaan yang interaktif untuk membantu memahami pola distribusi antarwilayah.
        </p>
        """,
        unsafe_allow_html=True
    )

    if "user_input" not in st.session_state:
            st.warning(
                "Belum ada hasil clustering. "
                "Silakan lakukan proses clustering di halaman **Clustering Wilayah** dengan menekan tombol di bawah."
            )
            if st.button("Mulai Clustering Wilayah"):
                st.session_state.page = "clustering_wilayah"
                st.rerun()
            return
        
    user_input = st.session_state.user_input
    df_hasil = user_input.get("df_hasil")
    vars_ = user_input["fitur_digunakan"]
            
    #Tabel Hasil clustering
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Tabel Hasil Clustering</p>", unsafe_allow_html=True)
    if df_hasil is not None and not df_hasil.empty:
        st.dataframe(df_hasil)
        st.caption("Kolom **Cluster** menunjukkan hasil pengelompokan wilayah.")
    else:
        st.warning("Belum ada hasil clustering. Silakan ulangi proses.")
        st.stop()
    
    #Ringkasan jumlah anggota per cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Ringkasan Jumlah Anggota per Cluster</p>", unsafe_allow_html=True)
    summary, fig = ringkasan_cluster(
        df_hasil, 
        f"Jumlah Anggota per Cluster ({user_input['metode_clustering']})"
    )

    col1, col2 = st.columns([2,3])

    with col1:
        st.pyplot(fig, width= 'content')

    with col2:
        st.dataframe(summary, hide_index=True)
    
    #Analisis cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Analisis Hasil Cluster</p>", unsafe_allow_html=True)
    mean_c, labels, score = analisis_cluster(
        df_hasil,
        fitur_digunakan=st.session_state.user_input["fitur_digunakan"],
        algoritma=st.session_state.user_input["metode_clustering"]
    )
    st.markdown("**Rata-rata indikator per cluster:**")
    st.dataframe(mean_c)
        
    #Download Tabel Hasil Clustering
    st.markdown("<p style='text-align:center; font-size:28px; font-weight:bold; margin-top:86px;'>Download Hasil Clustering</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; margin-bottom:24px;'>Tabel hasil clustering yang telah ditampilkan dapat diunduh menggunakan format Xlsx maupun PDF.</p>", unsafe_allow_html = True)
    col1, col2 = st.columns(2)

    with col1:
        #Excel
        xlsx_buf = io.BytesIO()
        with pd.ExcelWriter(xlsx_buf, engine="openpyxl") as writer:
            df_hasil.to_excel(writer, sheet_name="Hasil_Clustering", index=False)
            summary.to_excel(writer, sheet_name="Ringkasan_Cluster", index=False)
            mean_c.to_excel(writer, sheet_name="Rata-rata Indikator", index=True)
            pd.DataFrame(list(labels.items()), columns=["Cluster", "Label"]).to_excel(
                writer, sheet_name="Label_Cluster", index=False
            )
        st.download_button(
            label=" Download Excel (.xlsx)",
            data=xlsx_buf.getvalue(),
            file_name="hasil_clustering.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width= 'stretch'
        )

    with col2:
        #PDF
        pdf_buf = io.BytesIO()
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(
            pdf_buf,
            pagesize=landscape(A4),
            leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18
        )

        elements = []
        elements.append(Paragraph("Hasil Clustering", styles["Heading1"]))

        data1 = [df_hasil.columns.tolist()] + df_hasil.astype(str).values.tolist()
        t1 = Table(data1, repeatRows=1)
        t1.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#374151")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.Color(0.97,0.97,0.97)])
        ]))
        elements.append(t1)

        elements.append(PageBreak())

        elements.append(Paragraph("Ringkasan Cluster", styles["Heading2"]))
        data2 = [summary.columns.tolist()] + summary.astype(str).values.tolist()
        t2 = Table(data2, repeatRows=1)
        t2.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4B5563")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ]))
        elements.append(t2)
        
        elements.append(PageBreak())
        elements.append(Paragraph("Analisis Cluster", styles["Heading2"]))

        #Rata-rata indikator per cluster
        elements.append(Paragraph("Rata-rata indikator per cluster", styles["Heading3"]))
        data3 = [mean_c.reset_index().columns.tolist()] + mean_c.reset_index().astype(str).values.tolist()
        t3 = Table(data3, repeatRows=1)
        t3.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#6B7280")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ]))
        elements.append(t3)

        #Skema label cluster
        elements.append(Paragraph("Skema Label Cluster", styles["Heading3"]))
        data4 = [["Cluster", "Label"]] + [[str(k), str(v)] for k, v in labels.items()]
        t4 = Table(data4, repeatRows=1)
        t4.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#9CA3AF")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ]))
        elements.append(t4)

        doc.build(elements)

        st.download_button(
            label="Download PDF",
            data=pdf_buf.getvalue(),
            file_name="hasil_clustering.pdf",
            mime="application/pdf",
            width= 'stretch'
        )

    st.markdown("---")
        
    #Evaluasi cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Evaluasi Hasil Clustering</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        placeholder = st.empty()
        with placeholder.container():
            loader("Sedang membuat silhouette plot...")

        fig_sil = visualisasi_silhouette_full(
            df_hasil[user_input["fitur_digunakan"]].values,
            df_hasil["Cluster"].values,
            algo=user_input["metode_clustering"]
        )
        placeholder.empty()
        st.pyplot(fig_sil, width= 'content')

    with col2:
        st.markdown("""
        <div style='background-color: #0e1117; 
                    border: 2px solid #262730; 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin-bottom: 15px;'>
            <p style='color: white; font-size: 16px; font-weight: bold; margin: 0;'>Evaluasi Cluster</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            kategori, warna, deskripsi = get_kategori_silhouette(user_input['silhouette'])
            
            st.markdown(
                f"""
                <div style='background-color: #0e1117; 
                            border: 2px solid #262730; 
                            border-radius: 10px; 
                            padding: 20px;
                            height: 180px;'>
                    <div style="font-size:14px; font-weight:bold; color:white; margin-bottom:10px;">
                        Silhouette Score
                    </div>
                    <div style="font-size:32px; font-weight:bold; color:white; margin-bottom:10px;">
                        {user_input['silhouette']:.4f}
                    </div>
                    <div style="font-size:13px; color:{warna}; margin-bottom:8px; font-weight:600;">
                        {kategori}
                    </div>
                    <div style="font-size:13px; color:#9ca3af; line-height:1.4;">
                        {deskripsi}, Silhouette mendekati 1 lebih baik
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style='background-color: #0e1117; 
                            border: 2px solid #262730; 
                            border-radius: 10px; 
                            padding: 20px;
                            height: 180px;'>
                    <div style="font-size:14px; font-weight:bold; color:white; margin-bottom:10px;">
                        Davies-Bouldin Index
                    </div>
                    <div style="font-size:32px; font-weight:bold; color:white; margin-bottom:10px;">
                        {user_input['dbi']:.4f}
                    </div>
                    <div style="font-size:13px; color:#9ca3af; line-height:1.4; margin-top:25px;">
                        DBI mendekati 0 lebih baik
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div style='background-color: #0e1117; 
                        border: 2px solid #262730; 
                        border-radius: 10px; 
                        padding: 20px;
                        margin-top: 10px;'>
                <div style="font-size:14px; font-weight:bold; color:white; margin-bottom:10px;">
                    Waktu Komputasi (detik)
                </div>
                <div style="font-size:32px; font-weight:bold; color:white;">
                    {st.session_state.user_input['waktu_komputasi']:.7f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("""
        <div style='background-color: #0e1117; 
                    border: 2px solid #262730; 
                    border-radius: 10px; 
                    padding: 20px;
                    margin-top: 10px;'>
            <div style="font-size:14px; font-weight:bold; color:white; margin-bottom:15px;">
                Interpretasi Silhouette Score
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 12px; height: 12px; background-color: #28a745; border-radius: 3px; margin-right: 10px;"></div>
                <span style="color: white; font-size: 13px;"><b>0.71 - 1.00:</b> <span style="color: #28a745;">Struktur Kuat</span></span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 12px; height: 12px; background-color: #ffc107; border-radius: 3px; margin-right: 10px;"></div>
                <span style="color: white; font-size: 13px;"><b>0.51 - 0.70:</b> <span style="color: #ffc107;">Struktur Sedang</span></span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 12px; height: 12px; background-color: #fd7e14; border-radius: 3px; margin-right: 10px;"></div>
                <span style="color: white; font-size: 13px;"><b>0.26 - 0.50:</b> <span style="color: #fd7e14;">Struktur Lemah</span></span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 12px; height: 12px; background-color: #dc3545; border-radius: 3px; margin-right: 10px;"></div>
                <span style="color: white; font-size: 13px;"><b>< 0.26:</b> <span style="color: #dc3545;">Tidak Ada Struktur</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    #Simpan Silhouette Plot
    if 'fig_sil' in locals() and not any(t == "Silhouette Plot" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Silhouette Plot", fig_sil))
        plt.close(fig_sil)


    #Heatmap Korelasi
    st.markdown(
        "<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Korelasi Antar Variabel</p>", 
        unsafe_allow_html=True
    )

    placeholder = st.empty()
    with placeholder.container():
        loader("Membuat heatmap korelasi variabel...")

    fig_heatmap = heatmap_correlation(df_hasil, vars_, "Heatmap Korelasi Variabel")
    placeholder.empty()

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig_heatmap, use_container_width=True)
    with col2:
        st.markdown("""
        <div style='background-color: #0e1117; 
                    border: 2px solid #262730; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-bottom: 15px;'>
            <p style='color: white; font-size: 16px; font-weight: bold; margin: 0; text-align: left;'> 
            Korelasi menggambarkan seberapa erat hubungan antara dua indikator.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.markdown("""
            <div style='background-color: #0e1117; 
                        border: 2px solid #262730; 
                        border-radius: 10px; 
                        padding: 20px; 
                        margin-bottom: 10px;
                        height: 160px;
                        display: flex;
                        flex-direction: column;'>
                <p style='color: #4a9eff; font-size: 18px; font-weight: bold; margin: 0 0 10px 0;'>Nilai Positif (+)</p>
                <p style='color: white; font-size: 13px; margin: 0; line-height: 1.5;'>
                Kedua indikator bergerak searah. Ketika satu indikator meningkat, indikator lainnya juga cenderung meningkat.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with row1_col2:
            st.markdown("""
            <div style='background-color: #0e1117; 
                        border: 2px solid #262730; 
                        border-radius: 10px; 
                        padding: 20px; 
                        margin-bottom: 10px;
                        height: 160px;
                        display: flex;
                        flex-direction: column;'>
                <p style='color: #4a9eff; font-size: 18px; font-weight: bold; margin: 0 0 10px 0;'>Nilai Negatif (−)</p>
                <p style='color: white; font-size: 13px; margin: 0; line-height: 1.5;'>
                Kedua indikator bergerak berlawanan arah. Ketika satu indikator meningkat, indikator lainnya cenderung menurun.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            st.markdown("""
            <div style='background-color: #0e1117; 
                        border: 2px solid #262730; 
                        border-radius: 10px; 
                        padding: 20px;
                        height: 160px;
                        display: flex;
                        flex-direction: column;'>
                <p style='color: #4a9eff; font-size: 18px; font-weight: bold; margin: 0 0 10px 0;'>Mendekati Nol</p>
                <p style='color: white; font-size: 13px; margin: 0; line-height: 1.5;'>
                Mengindikasikan hubungan yang lemah atau tidak konsisten antara dua indikator.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with row2_col2:
            st.markdown("""
            <div style='background-color: #0e1117; 
                        border: 2px solid #262730; 
                        border-radius: 10px; 
                        padding: 20px;
                        height: 160px;
                        display: flex;
                        flex-direction: column;'>
                <p style='color: #4a9eff; font-size: 18px; font-weight: bold; margin: 0 0 10px 0;'>Mendekati ±1</p>
                <p style='color: white; font-size: 13px; margin: 0; line-height: 1.5;'>
                Menunjukkan hubungan yang sangat kuat, baik searah maupun berlawanan arah.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    #Simpan Heatmap
    if 'fig_heatmap' in locals() and not any(t == "Heatmap Korelasi" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Heatmap Korelasi", fig_heatmap))
        plt.close(fig_heatmap)
    
    #Tren fitur tahunan
    indikator_rendah_bagus = ["P0", "P1", "P2"]
    tahun_tersedia = df_hasil["Tahun"].nunique()
    tahun_terbaru = df_hasil["Tahun"].max()
    top_n = 10  

    if tahun_tersedia > 1:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Tren Indikator Per Tahun</p>", unsafe_allow_html=True)

            col1, col2 = st.columns([2, 1])
            with col1:
                fitur_dipilih = st.selectbox(
                    "Pilih indikator yang ingin ditampilkan:",
                    options=user_input["fitur_digunakan"],
                    format_func=lambda x: indikator_deskripsi.get(x, x)
                )
            with col2:
                top_n_input = st.number_input(
                    "Tampilkan berapa wilayah teratas?",
                    min_value=1,
                    max_value=df_hasil["Nama Wilayah"].nunique(),
                    value=10,
                    step=1
                )
                st.session_state.top_n_for_pdf = top_n_input

            ascending = True if fitur_dipilih in indikator_rendah_bagus else False
            df_tahun_terbaru = df_hasil[df_hasil["Tahun"] == tahun_terbaru]

            ranking = (
                df_tahun_terbaru[["Nama Wilayah", fitur_dipilih]]
                .sort_values(by=fitur_dipilih, ascending=ascending)
                .head(top_n_input) 
            )
            wilayah_top = ranking["Nama Wilayah"]

            deskripsi = indikator_deskripsi.get(fitur_dipilih, fitur_dipilih)
            judul_tren = f"{top_n_input} Kabupaten/Kota dengan {deskripsi} {'terendah' if fitur_dipilih in indikator_rendah_bagus else 'tertinggi'}"

            fig_tren_web = visualisasi_tren_tahunan(
                df_hasil[df_hasil["Nama Wilayah"].isin(wilayah_top)],
                fitur_dipilih,
                top_n=top_n_input,  
                judul=judul_tren
            )
            st.pyplot(fig_tren_web, width= 'stretch')

            tabel_multi_tahun = (
                df_hasil[df_hasil["Nama Wilayah"].isin(wilayah_top)]
                .pivot_table(index="Nama Wilayah", columns="Tahun", values=fitur_dipilih)
            )
            
            tahun_terbaru = tabel_multi_tahun.columns.max()
            tabel_multi_tahun = tabel_multi_tahun.sort_values(by=tahun_terbaru, ascending=ascending)

            st.markdown(f"<p style='text-align:center; font-size:18px; font-weight:bold; margin-top:24px;'>Nilai {deskripsi} per Tahun untuk {top_n_input} Kabupaten/Kota</p>", unsafe_allow_html=True)
            st.dataframe(tabel_multi_tahun, width= 'stretch')
    
    
    top_n_pdf = st.session_state.get('top_n_for_pdf', 10)

    if tahun_tersedia > 1:
        fitur_tersedia = [f for f in user_input["fitur_digunakan"] if f in df_hasil.columns]
        
        for fitur in fitur_tersedia:
            deskripsi = indikator_deskripsi.get(fitur, fitur)
            ascending = True if fitur in indikator_rendah_bagus else False

            wilayah_top = (
                df_hasil[df_hasil["Tahun"] == tahun_terbaru]
                [["Nama Wilayah", fitur]]
                .sort_values(by=fitur, ascending=ascending)
                .head(top_n_pdf)["Nama Wilayah"] 
            )

            df_tren_top = df_hasil[df_hasil["Nama Wilayah"].isin(wilayah_top)]

            judul_tren = f"{top_n_pdf} Kabupaten/Kota dengan {deskripsi} {'terendah' if fitur in indikator_rendah_bagus else 'tertinggi'}"
            fig_tren_full = visualisasi_tren_tahunan(df_tren_top, fitur, top_n=top_n_pdf, judul=judul_tren)

            if not any(t == f"Tren {deskripsi}" for t, _ in st.session_state.all_figs):
                st.session_state.all_figs.append((f"Tren {deskripsi}", fig_tren_full))
                plt.close(fig_tren_full)

            tahun_tersedia_list = sorted(df_hasil["Tahun"].unique())

            tabel_multi_tahun = (
                df_tren_top
                .pivot_table(index="Nama Wilayah", columns="Tahun", values=fitur)
                .reset_index()
            )

            available_years = [y for y in tahun_tersedia_list if y in tabel_multi_tahun.columns]
            tabel_multi_tahun = tabel_multi_tahun[["Nama Wilayah"] + available_years]

            tahun_terbaru_col = available_years[-1] 
            tabel_multi_tahun = tabel_multi_tahun.sort_values(by=tahun_terbaru_col, ascending=ascending)

            tabel_fig = df_to_fig_table(
                tabel_multi_tahun,
                title=f"Tabel {top_n_pdf} Kabupaten/Kota dengan {deskripsi} {'terendah' if fitur in indikator_rendah_bagus else 'tertinggi'}"
            )
            if not any(t == f"Tabel Tren {deskripsi}" for t, _ in st.session_state.all_figs):
                st.session_state.all_figs.append((f"Tabel Tren {deskripsi}", tabel_fig))
                plt.close(tabel_fig)


    #Visualisasi Indikator per Cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Visualisasi Indikator per Cluster</p>", unsafe_allow_html=True)

    #Scatterplot Pasangan Indikator
    st.markdown("<p style='text-align:center; font-size:18px; font-weight:bold; margin-top:32px;'>Scatterplot Pasangan Indikator per Cluster</p>", unsafe_allow_html=True)
    placeholder = st.empty()
    with placeholder.container():
        loader("Sedang membuat scatterplot...")

    figures_scatter = visualisasi_scatter_per_pasangan_terpisah(
        df_hasil,
        fitur_digunakan=user_input["fitur_digunakan"],
        algo=user_input["metode_clustering"]
    )
    placeholder.empty()

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        tampilkan_figures_dalam_grid(st, figures_scatter, n_cols=3)
    
    #Simpan semua figures scatterplot
    if 'figures_scatter' in locals():
        for title, fig in figures_scatter:
            if not any(t == title for t, _ in st.session_state.all_figs):
                st.session_state.all_figs.append((title, fig))
                plt.close(fig)

    #Distribusi indikator per cluster
    st.markdown("<p style='text-align:center; font-size:18px; font-weight:bold; margin-top:32px;'>Boxplot Distribusi Indikator per Cluster</p>", unsafe_allow_html=True)
    placeholder = st.empty()
    with placeholder.container():
        loader("Sedang membuat boxplot indikator...")

    figures_boxplot = visualisasi_boxplot_per_indikator_terpisah(
        df_hasil,
        fitur_digunakan=user_input["fitur_digunakan"],
        algo=user_input["metode_clustering"]
    )
    placeholder.empty()

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        tampilkan_figures_dalam_grid(st, figures_boxplot, n_cols=3)
    
    #Simpan Boxplot
    if 'figures_boxplot' in locals():
        for title, fig in figures_boxplot:
            if not any(t == title for t, _ in st.session_state.all_figs):
                st.session_state.all_figs.append((title, fig))
                plt.close(fig)

    #Peta Hasil Clustering
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Pemetaan Hasil Clustering</p>", unsafe_allow_html=True)
    shp_path = get_shapefile_from_drive("1V8K5N0hd917R78UbxNNj224upoxEcoKr")
    fig_map_static = None
    try:
        placeholder = st.empty()
        with placeholder.container():
            loader("Sedang memuat peta hasil clustering...")

        gdf_map = persiapkan_shapefile(shp_path, df_hasil)
        m = tampilkan_peta(
            gdf_map,
            skor=score,
            label_cluster=labels,
            nama_algo=user_input["metode_clustering"],
            fitur_digunakan=user_input["fitur_digunakan"]
        )

        placeholder.empty()
        st_folium(m, width= 'stretch', height=800, returned_objects=[])
        fig_map_static = buat_peta_statis(gdf_map, labels, cluster_col="Cluster")

    except Exception as e:
        st.error(f"Gagal menampilkan peta: {e}")
            
    if 'fig_map_static' in locals() and fig_map_static is not None and not any(t == "Peta Hasil Clustering" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Peta Hasil Clustering", fig_map_static))
        plt.close(fig_map_static)
        
    #Download Visualisasi Clustering
    st.markdown("<p style='text-align:center; font-size:28px; font-weight:bold; margin-top:86px;'>Download Visualisasi Hasil Clustering</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; margin-bottom:24px;'>Hasil visualisasi yang telah ditampilkan dapat diunduh menggunakan format PNG (Zip) maupun PDF.</p>", unsafe_allow_html = True)
    if st.session_state.all_figs:
        col1, col2 = st.columns(2)

        with col1:
            #PNG dalam ZIP
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w") as zf:
                for title, fig in st.session_state.all_figs:
                    filename = title.lower().replace(" ", "_") + ".png"
                    zf.writestr(filename, fig_to_png_bytes(fig))
            st.download_button(
                "Download PNG (Zip)",
                data=zip_buf.getvalue(),
                file_name="visualisasi_clustering.zip",
                mime="application/zip",
                width= 'stretch'
            )

        with col2:
            #PDF
            sil_per_cluster = analisis_silhouette_per_cluster(
                df_hasil[user_input["fitur_digunakan"]].values,
                df_hasil["Cluster"].values
            )

            keterangan_analisis = {
                "Silhouette Plot": "Rata-rata nilai silhouette per cluster:<br/>" + "<br/>".join(
                    [f"Cluster {c}: {v:.3f}" for c, v in sil_per_cluster.items()]
                )
            }

            pdf_all = figs_to_pdf(st.session_state.all_figs, keterangan_analisis=keterangan_analisis)
            st.download_button(
                "Download PDF",
                data=pdf_all,
                file_name="visualisasi_clustering.pdf",
                mime="application/pdf",
                width= 'stretch'
            )
    else:
        st.info("Belum ada grafik yang bisa diunduh.")