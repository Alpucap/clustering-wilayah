import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import io
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage

analisis_teks = {
    "Silhouette Plot": "Plot ini menunjukkan kualitas pemisahan cluster. Nilai mendekati 1 artinya cluster lebih baik.",
    "Sebaran Indikator": "Scatter plot memperlihatkan distribusi indikator antar cluster, terlihat pola pemisahan antar wilayah.",
    "Boxplot Indikator": "Boxplot menampilkan variasi indikator dalam tiap cluster, sehingga bisa dibandingkan antar cluster.",
    "Heatmap Korelasi": "Heatmap menggambarkan hubungan antar variabel. Korelasi positif ditunjukkan warna merah, negatif warna biru.",
    "Peta Hasil Clustering": "Peta menunjukkan distribusi spasial cluster pada wilayah Indonesia, memudahkan analisis geografis."
}

def fig_to_png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()

def figs_to_pdf(figs, keterangan_analisis=None):
    buf = io.BytesIO()
    page_w, page_h = landscape(A4)

    max_width = page_w - 100
    max_height = page_h - 150

    doc = SimpleDocTemplate(
        buf, pagesize=landscape(A4),
        leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    elements = []

    for i, (title, fig) in enumerate(figs, start=1):
        img_bytes_buf = io.BytesIO()
        fig.savefig(img_bytes_buf, format="png", bbox_inches="tight", dpi=90, pad_inches=0.1)
        img_bytes_buf.seek(0)

        pil_img = PILImage.open(img_bytes_buf)
        iw, ih = pil_img.size
        scale = min(max_width / iw, max_height / ih, 1.0) * 0.9
        w, h = iw * scale, ih * scale

        elements.append(Paragraph(title, styles["Heading2"]))
        elements.append(Image(img_bytes_buf, width=w, height=h))

        if keterangan_analisis and title in keterangan_analisis:
            elements.append(Paragraph(keterangan_analisis[title], styles["Normal"]))

        if i < len(figs):
            elements.append(PageBreak())

    doc.build(elements)
    return buf.getvalue()

def buat_peta_statis(gdf_map, labels, cluster_col="Cluster"):
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))

    cluster_ids = sorted(gdf_map[cluster_col].unique())
    cmap = plt.get_cmap("tab20")
    warna_cluster = {cid: cmap(i % 20) for i, cid in enumerate(cluster_ids)}

    gdf_map.plot(
        column=cluster_col,
        categorical=True,
        ax=ax,
        color=gdf_map[cluster_col].map(warna_cluster),
        edgecolor="black",
        linewidth=0.3,
        legend=False
    )

    ax.set_title("Peta Sebaran Hasil Clustering", fontsize=16, fontweight="bold", pad=20)
    ax.axis("off")

    handles = []
    for cid in cluster_ids:
        cluster_label = labels.get(cid, f"Cluster {cid}")
        handles.append(mpatches.Patch(color=warna_cluster[cid], label=f"Cluster {cid}: {cluster_label}"))

    ax.legend(
        handles=handles,
        title="Keterangan Cluster",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=3,
        fontsize=9,
        title_fontsize=10,
        frameon=False
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
