import streamlit as st
import pandas as pd
from api.clustering.visualisasi_clustering import analisis_cluster, ringkasan_cluster, visualisasi_evaluasi, visualisasi_silhouette_full, visualisasi_sebaran_cluster_per_indikator, boxgrid_per_cluster, heatmap_correlation, get_shapefile_from_drive, persiapkan_shapefile, tampilkan_peta
from streamlit_folium import st_folium
import io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
import zipfile
from PIL import Image as PILImage


#Helper method untuk sementara
def fig_to_png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()

def figs_to_pdf(figs):
    buf = io.BytesIO()
    page_w, page_h = landscape(A4)
    
    max_width = page_w - 100       
    max_height = page_h - 150

    doc = SimpleDocTemplate(
        buf, 
        pagesize=landscape(A4),
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    elements = []

    for i, (title, fig) in enumerate(figs, start=1):
        img_bytes_buf = io.BytesIO()
        fig.savefig(img_bytes_buf, format="png", bbox_inches="tight", dpi=80, pad_inches=0.1)
        img_bytes_buf.seek(0)

        pil_img = PILImage.open(img_bytes_buf)
        iw, ih = pil_img.size
        img_bytes_buf.seek(0)

        scale = min(max_width / iw, max_height / ih, 1.0) * 0.85  
        w, h = iw * scale, ih * scale

        elements.append(Paragraph(title, styles["Heading2"]))
        elements.append(Image(img_bytes_buf, width=w, height=h))

        if i < len(figs):
            elements.append(PageBreak())

    doc.build(elements)
    return buf.getvalue()

def buat_peta_statis(gdf_map, labels, cluster_col="Cluster"):
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    
    gdf_map.plot(column=cluster_col, categorical=True, ax=ax, cmap="tab20", edgecolor="black", linewidth=0.3)
    ax.set_title("Peta Sebaran Hasil Clustering", fontsize=14, fontweight="bold")
    ax.axis("off")

    cluster_ids = sorted(gdf_map[cluster_col].unique())
    handles = []
    cmap = plt.get_cmap("tab20")

    for cid in cluster_ids:
        cluster_label = labels.get(cid, f"Cluster {cid}")
        color = cmap(cid % 20)
        handles.append(mpatches.Patch(color=color, label=f"Cluster {cid}: {cluster_label}"))

    ax.legend(
        handles=handles,
        title=f"Keterangan Cluster {labels.get('algo','')}".strip(),
        loc="lower left",
        fontsize=8,
        title_fontsize=9
    )

    return fig

def loader(text: str):
    st.markdown(
        f"""
        <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4da6ff;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            animation: spin 1s linear infinite;
            margin: 0 auto 12px auto;
        }}
        </style>

        <div style="text-align:center; padding:60px;">
            <div class="spinner"></div>
            <div style="font-size:24px; font-weight:bold; color:#FAFAFA;">
                {text}
            </div>
            <div style="font-size:16px; color:gray; margin-top:4px;">
                Proses ini mungkin membutuhkan waktu beberapa detik
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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

    if "user_input" not in st.session_state:
        st.error("Belum ada input dari halaman sebelumnya. Silakan upload dataset dan jalankan clustering dulu.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "Mulai Clustering Wilayah", 
                use_container_width=True,
                help="Mulai proses clustering kabupaten/kota di Indonesia"
            ):
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
    
    # #Info tambahan (null & outlier)
    # if user_input.get("null_summary") is not None and not user_input["null_summary"].empty:
    #     st.warning(f"Ada missing value pada kolom:\n{user_input['null_summary'].to_dict(orient='records')}")
    # if user_input.get("jumlah_outlier", 0) > 0:
    #     st.warning(f"Ditemukan {user_input['jumlah_outlier']} outlier pada dataset.")
    
    #Ringkasan jumlah anggota per cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Ringkasan Jumlah Anggota per Cluster</p>", unsafe_allow_html=True)
    summary, fig = ringkasan_cluster(
        df_hasil, 
        f"Jumlah Anggota per Cluster ({user_input['metode_clustering']})"
    )

    col1, col2 = st.columns([1,2])

    with col1:
        st.pyplot(fig, use_container_width=False)

    with col2:
        st.dataframe(summary)
    
    #Analisis cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Analisis Hasil Cluster</p>", unsafe_allow_html=True)
    mean_c, labels, score = analisis_cluster(
        df_hasil,
        fitur_digunakan=st.session_state.user_input["fitur_digunakan"],
        algoritma=st.session_state.user_input["metode_clustering"]
    )
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Rata-rata indikator per cluster:**")
        st.dataframe(mean_c)
    with col2:
        st.markdown("**Skema label cluster:**")
        df_labels = pd.DataFrame(list(labels.items()), columns=["Cluster", "Label"])
        st.dataframe(df_labels)
        
    #Download Tabel Hasil Clustering
    st.markdown("<p style='text-align:center; font-size:28px; font-weight:bold; margin-top:86px;'>Download Hasil Clustering</p>", unsafe_allow_html=True)

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
            use_container_width=True
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
            use_container_width=True
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
        st.pyplot(fig_sil, use_container_width=False)

    with col2:
        st.markdown("**Evaluasi Cluster**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
                <div style="text-align:left; margin-bottom:20px;">
                    <div style="font-size:14px; font-weight:bold; color:#FAFAFA;">
                        Silhouette Score
                    </div>
                    <div style="font-size:28px; font-weight:bold; color:white; margin-top:2px;">
                        {user_input['silhouette']:.4f}
                    </div>
                    <div style="font-size:14px; color:gray; margin-top:-2px;">
                        Silhouette mendekati 1 lebih baik
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="text-align:left; margin-bottom:20px;">
                    <div style="font-size:14px; font-weight:bold; color:#FAFAFA;">
                        Davies-Bouldin Index
                    </div>
                    <div style="font-size:28px; font-weight:bold; color:white; margin-top:2px;">
                        {user_input['dbi']:.4f}
                    </div>
                    <div style="font-size:14px; color:gray; margin-top:-2px;">
                        DBI mendekati 0 lebih baik
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div style="text-align:left; margin-bottom:20px; margin-top:8px;">
                <div style="font-size:14px; font-weight:bold; color:#FAFAFA;">
                    Waktu Komputasi (detik)
                </div>
                <div style="font-size:28px; font-weight:bold; color:white; margin-top:2px;">
                    {st.session_state.user_input['waktu_komputasi']:.7f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig_heatmap, use_container_width=True)
        
    #Visualisasi Indikator per Cluster
    st.markdown("<p style='text-align:center; font-size:24px; font-weight:bold; margin-top:48px;'>Visualisasi Indikator per Cluster</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Sebaran Indikator per Cluster**")
        placeholder = st.empty()
        with placeholder.container():
            loader("Sedang membuat scatter indikator...")

        fig_scatter = visualisasi_sebaran_cluster_per_indikator(
            df_hasil,
            fitur_digunakan=user_input["fitur_digunakan"],
            algo=user_input["metode_clustering"]
        )
        placeholder.empty()
        st.pyplot(fig_scatter, use_container_width=True)


    with col2:
        st.markdown("**Distribusi Indikator per Cluster**")
        placeholder = st.empty()
        with placeholder.container():
            loader("Sedang membuat boxplot indikator...")

        fig_box = boxgrid_per_cluster(
            df_hasil,
            vars_,
            f"Distribusi Indikator ({user_input['metode_clustering']})"
        )
        placeholder.empty()
        st.pyplot(fig_box, use_container_width=True)

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
        st_folium(m, use_container_width=True, height=800, returned_objects=[])
        fig_map_static = buat_peta_statis(gdf_map, labels, cluster_col="Cluster")

    except Exception as e:
        st.error(f"Gagal menampilkan peta: {e}")


    #Download Visualisasi Clustering
    if "all_figs" not in st.session_state:
        st.session_state.all_figs = []

    if 'fig_sil' in locals() and not any(t == "Silhouette Plot" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Silhouette Plot", fig_sil))

    if 'fig_scatter' in locals() and not any(t == "Sebaran Indikator" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Sebaran Indikator", getattr(fig_scatter, "fig", fig_scatter)))

    if 'fig_box' in locals() and not any(t == "Boxplot Indikator" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Boxplot Indikator", fig_box))

    if 'fig_heatmap' in locals() and not any(t == "Heatmap Korelasi" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Heatmap Korelasi", fig_heatmap))

    if 'fig_map_static' in locals() and fig_map_static is not None and not any(t == "Peta Hasil Clustering" for t, _ in st.session_state.all_figs):
        st.session_state.all_figs.append(("Peta Hasil Clustering", fig_map_static))

    #Download Visualisasi Clustering
    st.markdown("<p style='text-align:center; font-size:28px; font-weight:bold; margin-top:86px;'>Download Visualisasi Hasil Clustering</p>", unsafe_allow_html=True)

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
                use_container_width=True
            )

        with col2:
            #PDF
            pdf_all = figs_to_pdf(st.session_state.all_figs)
            st.download_button(
                "Download PDF",
                data=pdf_all,
                file_name="visualisasi_clustering.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("Belum ada grafik yang bisa diunduh.")
