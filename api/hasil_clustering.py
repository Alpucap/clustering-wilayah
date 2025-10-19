import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import io
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage

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
