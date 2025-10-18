import streamlit as st
import pandas as pd
from database import SessionLocal
from models import ActivityLog
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def show(cookies=None):
    st.markdown("<h2 style='text-align: center;'>Riwayat Aktivitas</h2>", unsafe_allow_html=True)

    if "user_id" not in st.session_state:
        st.warning("Silakan login untuk melihat riwayat aktivitas.")
        return

    with SessionLocal() as db:
        logs = (
            db.query(ActivityLog)
            .filter_by(user_id=st.session_state["user_id"])
            .order_by(ActivityLog.created_at.desc())
            .all()
        )

    if not logs:
        st.info("Belum ada riwayat aktivitas.")
        return

    # Konversi ke DataFrame
    data = []
    for log in logs:
        fitur = log.fitur_digunakan
        if isinstance(fitur, str):
            fitur = json.loads(fitur)

        # Helper function untuk format angka
        def format_number(value):
            if value is None:
                return "-"
            try:
                return f"{float(value):.4f}"
            except (ValueError, TypeError):
                return str(value)

        data.append({
            "Tanggal": log.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "Metode": log.metode_clustering,
            "Fitur": ", ".join(fitur),
            "Tahun": f"{log.tahun_awal} – {log.tahun_akhir}",
            "Cluster": str(log.jumlah_cluster) if log.jumlah_cluster else "-",
            "Metode Jarak": log.metrik_jarak if log.metrik_jarak else "-",
            "Silhouette": format_number(log.silhouette),
            "DBI": format_number(log.dbi),
            "Waktu Komputasi (s)": format_number(log.waktu_komputasi),
        })

    df = pd.DataFrame(data)

    # Tampilkan tabel di UI
    st.dataframe(df, use_container_width=True)

    # Tombol download di bawah tabel
    st.markdown("#### Download Riwayat")
    col1, col2 = st.columns(2)

    with col1:
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="riwayat_aktivitas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:

        pdf_buffer = BytesIO()
        # Tambahkan margin yang lebih besar
        doc = SimpleDocTemplate(
            pdf_buffer, 
            pagesize=landscape(A4),
            leftMargin=1*cm,
            rightMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )

        styles = getSampleStyleSheet()
        
        # Style untuk fitur (wrap text)
        fitur_style = ParagraphStyle(
            'FiturStyle',
            parent=styles['Normal'],
            fontSize=7,
            leading=9,
            wordWrap='LTR'
        )
        
        # Style untuk cell biasa
        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontSize=7,
            leading=9
        )

        # Header
        table_data = [list(df.columns)]
        
        # Rows - wrap semua cell dalam Paragraph untuk kontrol lebih baik
        for row in df.values.tolist():
            new_row = []
            for i, val in enumerate(row):
                val_str = str(val) if val is not None else "-"
                if df.columns[i] == "Fitur":
                    new_row.append(Paragraph(val_str, fitur_style))
                else:
                    new_row.append(Paragraph(val_str, normal_style))
            table_data.append(new_row)

        # Set lebar kolom yang lebih proporsional
        # Total width landscape A4 = ~27cm - margins (2cm) = ~25cm = ~710 points
        col_widths = [85, 65, 180, 65, 40, 70, 60, 50, 95]

        table = Table(table_data, repeatRows=1, colWidths=col_widths)
        style = TableStyle([
            # Header styling
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4472C4")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,0), 8),
            
            # Cell padding
            ("LEFTPADDING", (0,0), (-1,-1), 4),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            
            # Grid
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("LINEBELOW", (0,0), (-1,0), 1.5, colors.HexColor("#4472C4")),
            
            # Alternating row colors
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F2F2")]),
        ])
        table.setStyle(style)

        doc.build([table])

        st.download_button(
            label="Download PDF (Landscape)",
            data=pdf_buffer.getvalue(),
            file_name="riwayat_aktivitas.pdf",
            mime="application/pdf",
            use_container_width=True
        )