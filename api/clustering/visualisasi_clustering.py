import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import streamlit as st
import folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from sklearn.metrics import silhouette_samples, silhouette_score
from fuzzywuzzy import process
import gdown, os, zipfile
import tempfile
import matplotlib.ticker as mticker
from itertools import combinations

#Deskripsi Indikator
indikator_deskripsi = {
    "AHH_L": "Angka Harapan Hidup Laki-laki (tahun)",
    "AHH_P": "Angka Harapan Hidup Perempuan (tahun)",
    "RLS":  "Rata-Rata Lama Sekolah (tahun)",
    "P0":   "Persentase Penduduk Miskin (persen)",
    "P1":   "Indeks Kedalaman Kemiskinan",
    "P2":   "Indeks Keparahan Kemiskinan"
}

#Method untuk melakukan analisis cluster
def analisis_cluster(df: pd.DataFrame, fitur_digunakan, algoritma: str = ""):
    fitur_positif = [c for c in ["AHH_L", "AHH_P", "RLS"] if c in fitur_digunakan]
    fitur_negatif = [c for c in ["P0", "P1", "P2"] if c in fitur_digunakan]
    fitur_semua = fitur_positif + fitur_negatif

    if not fitur_semua:
        raise ValueError("Tidak ada fitur yang valid untuk analisis cluster.")

    print(f"[Analisis] Algoritma: {algoritma} | Fitur: {fitur_semua}")

    #Jumlah anggota
    jumlah = df["Cluster"].value_counts().sort_index()
    print("Jumlah anggota per cluster:\n", jumlah, "\n")

    #Rata-rata indikator per cluster
    rata_c = df.groupby("Cluster")[fitur_semua].mean().round(3)
    print("Rata-rata indikator per cluster:\n", rata_c, "\n")

    #Skor gabungan
    if fitur_positif and fitur_negatif:
        skor = (rata_c[fitur_positif].mean(axis=1) - rata_c[fitur_negatif].mean(axis=1))
    elif fitur_positif:
        skor = rata_c[fitur_positif].mean(axis=1)
    else:
        skor = -rata_c[fitur_negatif].mean(axis=1)

    ranking = skor.sort_values(ascending=False)
    urutan = ranking.index.tolist()

    #Label cluster sederhana
    label_cluster = {c: f"Cluster {c}" for c in urutan}
    print("Label cluster:", label_cluster, "\n")

    return rata_c, label_cluster, skor


#Method untuk menampilkan ringkasan cluster
def ringkasan_cluster(df: pd.DataFrame, judul: str = "Ringkasan Cluster"):
    s = df["Cluster"].astype("Int64")
    hitung = s.value_counts().sort_index()
    k = int(hitung.index.max()) + 1
    hitung = hitung.reindex(range(k), fill_value=0)
    total = hitung.sum()

    ringkasan = pd.DataFrame({
        "Cluster": hitung.index,
        "Jumlah": hitung.values,
        "Persen": (hitung.values / total * 100).round(1)
    })

    fig, ax = plt.subplots(figsize=(4, 3))
    warna = plt.cm.Blues(np.linspace(0.4, 0.8, k))
    bars = ax.bar(ringkasan["Cluster"].astype(str), ringkasan["Jumlah"], color=warna)

    ax.margins(y=0.1)
    for bar, v, p in zip(bars, ringkasan["Jumlah"], ringkasan["Persen"]):
        ax.text(
            bar.get_x() + bar.get_width()/2, 
            bar.get_height() + (v * 0.02),
            f"{v} ({p}%)", 
            ha="center", va="bottom", fontsize=8
        )

    ax.set_title(f"{judul} (K={k})", fontsize=10, pad=15)
    ax.set_xlabel("Cluster", fontsize=9)
    ax.set_ylabel("Jumlah Wilayah", fontsize=9)

    fig.tight_layout()
    fig.subplots_adjust(top=0.85)

    return ringkasan, fig


#Method untuk menampilkan visualisasi evaluasi
def visualisasi_evaluasi(df_eval: pd.DataFrame):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for algo, subset in df_eval.groupby("Algoritma"):
        axes[0].plot(subset["K"], subset["Silhouette"], marker="o", label=algo)
        axes[1].plot(subset["K"], subset["DBI"], marker="o", label=algo)
        axes[2].plot(subset["K"], subset["Waktu (detik)"], marker="o", label=algo)

    axes[0].set_title("Koefisien Silhouette vs K")
    axes[1].set_title("Indeks DBI vs K")
    axes[2].set_title("Waktu Eksekusi vs K")
    for ax in axes:
        ax.legend()
        ax.set_xlabel("Jumlah Cluster (K)")
    plt.tight_layout()
    return fig

#Method untuk menampilkan kategori silhouette
def get_kategori_silhouette(score):
    if score >= 0.71:
        return "Struktur Kuat", "#28a745", "Cluster terpisah dengan sangat baik"
    elif score >= 0.51:
        return "Struktur Sedang", "#ffc107", "Cluster cukup terpisah"
    elif score >= 0.26:
        return "Struktur Lemah", "#fd7e14", "Cluster kurang terpisah"
    else:
        return "Tidak Ada Struktur", "#dc3545", "Cluster tidak membentuk struktur yang jelas"

#Method untuk menampilkan visualisasi silhouette full
def visualisasi_silhouette_full(data_matriks: np.ndarray, label_cluster: np.ndarray, algo: str = "", true_silhouette_score: float = None):
    nilai_sample = silhouette_samples(data_matriks, label_cluster)
    
    if true_silhouette_score is not None:
        nilai_rata = true_silhouette_score
    else:
        nilai_rata = silhouette_score(data_matriks, label_cluster)

    n_clusters = len(np.unique(label_cluster))
    y_bawah = 5
    
    fig, ax1 = plt.subplots(figsize=(5, 4))

    for i in range(n_clusters):
        nilai_i = nilai_sample[label_cluster == i]
        nilai_i.sort()

        ukuran_i = nilai_i.shape[0]
        y_atas = y_bawah + ukuran_i

        warna = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(
            np.arange(y_bawah, y_atas),
            0,
            nilai_i,
            facecolor=warna,
            edgecolor=warna,
            alpha=0.7
        )

        ax1.text(-0.05, y_bawah + 0.5 * ukuran_i, str(i), fontsize=9)
        y_bawah = y_atas + 5

    ax1.set_title(f"Plot Silhouette ({algo})", fontsize=11, pad=10) 
    ax1.set_xlabel("Nilai Silhouette Coefficient", fontsize=10)
    ax1.set_ylabel("Cluster", fontsize=10)

    #Garis rata-rata silhouette
    ax1.axvline(x=nilai_rata, color="red", linestyle="--", linewidth=1.5)
    
    ax1.text(
        nilai_rata, 
        -5,
        f"{nilai_rata:.4f}", 
        color="red", 
        fontsize=9, 
        ha="left", 
        va="bottom"
    )
    
    #Garis nol
    ax1.axvline(x=0, color="black", linestyle="--", linewidth=1)

    ax1.set_yticks([])
    ax1.set_xticks(np.linspace(-0.1, 1.0, 6))
    ax1.tick_params(axis="both", labelsize=9)

    plt.tight_layout(pad=1)
    
    return fig

#Method untuk analisis silhouette per cluster
def analisis_silhouette_per_cluster(X, labels):
    nilai_sample = silhouette_samples(X, labels)
    hasil = {}
    for c in np.unique(labels):
        hasil[c] = np.mean(nilai_sample[labels == c])
    return hasil


#Method untuk visualisasi boxplot
def visualisasi_boxplot_per_indikator_terpisah(df, fitur_digunakan, algo=""):
    kolom = [c for c in fitur_digunakan if c in df.columns]
    if not kolom:
        raise ValueError("Tidak ada fitur valid untuk divisualisasikan.")
    
    df_plot = df.copy()
    df_plot["Cluster"] = df_plot["Cluster"].astype(int)
    
    figures = []
    
    for fitur in kolom:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        deskripsi = indikator_deskripsi.get(fitur, fitur)
        
        sns.boxplot(
            data=df_plot, x="Cluster", y=fitur, hue="Cluster",
            palette="Set2", legend=False, ax=ax
        )
        
        ax.set_xlabel("Cluster", fontsize=10)
        ax.set_ylabel(deskripsi, fontsize=10)
        ax.set_title(f"Boxplot {deskripsi}", fontsize=11, pad=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        figures.append((f"Boxplot {deskripsi}", fig))
    
    return figures

#Method untuk visualisasi scatter plot
def visualisasi_scatter_per_pasangan_terpisah(df, fitur_digunakan, algo=""):
    kolom = [c for c in fitur_digunakan if c in df.columns]
    if len(kolom) < 2:
        raise ValueError("Minimal 2 fitur diperlukan untuk scatterplot.")
    
    pasangan = list(combinations(kolom, 2))
    figures = []
    
    for fitur_x, fitur_y in pasangan:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        deskripsi_x = indikator_deskripsi.get(fitur_x, fitur_x)
        deskripsi_y = indikator_deskripsi.get(fitur_y, fitur_y)
        
        for cluster in sorted(df["Cluster"].unique()):
            data_cluster = df[df["Cluster"] == cluster]
            ax.scatter(data_cluster[fitur_x], data_cluster[fitur_y], alpha=0.6, s=30, label=f"Cluster {cluster}")
        
        ax.set_xlabel(deskripsi_x, fontsize=10)
        ax.set_ylabel(deskripsi_y, fontsize=10)
        ax.set_title(f"{deskripsi_x} vs {deskripsi_y}", fontsize=11, pad=10)
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        figures.append((f"Scatter {deskripsi_x} vs {deskripsi_y}", fig))
    
    return figures

#Method untuk menampilkan figure dalam grid
def tampilkan_figures_dalam_grid(st, figures, n_cols=4):
    n_figs = len(figures)
    idx = 0
    
    while idx < n_figs:
        remaining = n_figs - idx
        cols_in_row = min(n_cols, remaining)
        cols = st.columns(n_cols)

        if cols_in_row < n_cols:
            empty_cols = n_cols - cols_in_row
            offset = empty_cols // 2
            
            for i in range(cols_in_row):
                with cols[offset + i]:
                    title, fig = figures[idx]
                    st.pyplot(fig, width='stretch')
                    idx += 1
        else:
            for i in range(n_cols):
                with cols[i]:
                    title, fig = figures[idx]
                    st.pyplot(fig, width='stretch')
                    idx += 1

#Method untuk menampilkan tren tahunan
def visualisasi_tren_tahunan(df, fitur, top_n=10, tahun_col="Tahun", wilayah_col="Nama Wilayah", judul=None, ascending=True):
    if tahun_col not in df.columns or wilayah_col not in df.columns:
        raise ValueError("Kolom 'Tahun' atau 'Nama Wilayah' tidak ditemukan.")

    deskripsi = indikator_deskripsi.get(fitur, fitur)
    df_plot = df.copy()

    nilai_rata = (
        df_plot
        .groupby(wilayah_col)[fitur]
        .mean()
    )

    urutan_wilayah = (
        nilai_rata
        .sort_values(ascending=ascending)
        .head(top_n)
        .index
        .tolist()
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    for wilayah in urutan_wilayah:
        data = (
            df_plot[df_plot[wilayah_col] == wilayah]
            .sort_values(tahun_col)
        )

        ax.plot(
            data[tahun_col],
            data[fitur],
            marker="o",
            linewidth=2,
            label=wilayah
        )

    arah = "terendah" if ascending else "tertinggi"

    ax.set_title(
        judul or f"{top_n} Kabupaten/Kota dengan {deskripsi} {arah} (rata-rata periode)",
        fontsize=13,
        pad=15
    )

    ax.set_xlabel("Tahun")
    ax.set_ylabel(deskripsi)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.grid(True, linestyle="--", alpha=0.6)

    ax.legend(
        fontsize=8,
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
        title="Wilayah",
        title_fontsize=9
    )

    plt.tight_layout()
    return fig

#Method untuk menampilkan korelasi variabel
def heatmap_correlation(df: pd.DataFrame, variabel, judul: str = "Korelasi Antar Variabel"):
    corr = df[variabel].corr(method="pearson")
    fig, ax = plt.subplots(figsize=(7, 5))

    sns.heatmap(
        corr, annot=True, cmap="coolwarm", center=0, fmt=".2f",
        xticklabels=[indikator_deskripsi.get(v, v) for v in variabel],
        yticklabels=[indikator_deskripsi.get(v, v) for v in variabel],
        ax=ax, annot_kws={"fontsize": 8}, cbar_kws={"shrink": 0.7}
    )

    ax.set_title(judul, fontsize=12, pad=20)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout(pad=2)
    
    return fig

#Method untuk normalisasi nama
def normalisasi_nama(nama):
    if pd.isna(nama):
        return nama
    return str(nama).upper().strip()

#Method untuk memberikan deskripsi perbandingan antar cluster
def deskripsi_perbandingan_cluster(mean_c, indikator_deskripsi):
    hasil = {}
    cluster_ids = list(mean_c.index)

    for c in cluster_ids:
        kalimat = []

        for fitur in mean_c.columns:
            nilai_c = mean_c.loc[c, fitur]

            lebih_tinggi = []
            lebih_rendah = []

            for c_lain in cluster_ids:
                if c_lain == c:
                    continue

                nilai_lain = mean_c.loc[c_lain, fitur]

                if nilai_c > nilai_lain:
                    lebih_tinggi.append(c_lain)
                elif nilai_c < nilai_lain:
                    lebih_rendah.append(c_lain)

            nama_fitur = indikator_deskripsi.get(fitur, fitur)

            bagian = []
            if lebih_tinggi:
                bagian.append(
                    f"lebih <b>tinggi</b> dibanding <b>Cluster {', '.join(map(str, lebih_tinggi))}</b>"
                )

            if lebih_rendah:
                bagian.append(
                    f"lebih <b>rendah</b> dibanding <b>Cluster {', '.join(map(str, lebih_rendah))}</b>"
                )

            if not bagian:
                teks = f"{nama_fitur} memiliki nilai yang relatif serupa antar cluster."
            else:
                teks = f"{nama_fitur} " + ", namun ".join(bagian) + "."

            kalimat.append(teks)

        hasil[c] = kalimat

    return hasil

#Method untuk menampilkan card cluster
def tampilkan_card_cluster(cluster_id, daftar_kalimat):
    st.markdown(f"""
    <div style="
        background-color:#0e1117;
        border:2px solid #262730;
        border-radius:12px;
        padding:20px;
        margin-bottom:20px;
        height:100%;
        display:flex;
        flex-direction:column;
    ">
        <p style="font-size:18px; font-weight:bold; color:#4a9eff; margin-bottom:14px;">
            Cluster {cluster_id}
        </p>
        <ul style="color:#e5e7eb; font-size:14px; padding-left:20px; margin:0; line-height:1.7; flex-grow:1;">
            {''.join([f"<li style='margin-bottom:10px'>{k}</li>" for k in daftar_kalimat])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

#Method untuk mengambil dan mengekstrak shapefile dari GDrive
def get_shapefile_from_drive(file_id: str):
    temp_dir = tempfile.mkdtemp(prefix="shapefile_")
    temp_zip = os.path.join(temp_dir, "shapefile.zip")

    gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_zip, quiet=False)

    with zipfile.ZipFile(temp_zip, "r") as zf:
        zf.extractall(temp_dir)

    for root, dirs, files in os.walk(temp_dir):
        for fn in files:
            if fn.endswith(".shp"):
                return os.path.join(root, fn)

    raise FileNotFoundError("File .shp tidak ditemukan setelah ekstraksi")

#Method untuk mempersiapkan shapefile
def persiapkan_shapefile(path: str, df_hasil: pd.DataFrame, mapping_manual: dict = None):
    if path.endswith(".gdb"):
        gdf = gpd.read_file(path, layer="ADMINISTRASI_AR_KABKOTA")
    else:
        gdf = gpd.read_file(path)

    gdf = gdf.to_crs(4326)

    kolom_nama = "NAMOBJ" if "NAMOBJ" in gdf.columns else gdf.columns[0]

    gdf["key_join"] = gdf[kolom_nama].apply(normalisasi_nama)
    df_h = df_hasil.copy()
    df_h["key_join"] = df_h["Nama Wilayah"].apply(normalisasi_nama)
    
    if "Tahun" in df_h.columns and df_h["Tahun"].nunique() > 1:
        numeric_cols = df_h.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c != "Cluster"] 
        
        agg_dict = {col: 'mean' for col in numeric_cols}
        agg_dict["Cluster"] = 'first'
        agg_dict["Nama Wilayah"] = 'first'
        
        df_h = df_h.groupby("key_join", as_index=False).agg(agg_dict)

    if mapping_manual is None:
        mapping_manual = {
            "KOTA ADM. JAKARTA SELATAN": "KOTA JAKARTA SELATAN",
            "KOTA ADM. JAKARTA TIMUR": "KOTA JAKARTA TIMUR",
            "KOTA ADM. JAKARTA PUSAT": "KOTA JAKARTA PUSAT",
            "KOTA ADM. JAKARTA BARAT": "KOTA JAKARTA BARAT",
            "KOTA ADM. JAKARTA UTARA": "KOTA JAKARTA UTARA",
            "ADM. KEP. SERIBU": "KEPULAUAN SERIBU",
            "MUKO MUKO": "MUKOMUKO",
            "FAK FAK": "FAKFAK",
            "TOJO UNA UNA": "TOJO UNA-UNA",
            "TOLI TOLI": "TOLITOLI",
            "PASANGKAYU": "MAMUJU UTARA",
            "KOTA PALANGKARAYA": "KOTA PALANGKA RAYA",
            "PONTIANAK": "MEMPAWAH",
            "KOTA BARU": "KOTABARU",
            "KOTA BAU BAU": "KOTA BAUBAU",
            "LAMPUNG SELATAN": "KABUPATEN LAMPUNG SELATAN",
            "SITARO": "KEPULAUAN SIAU TAGULANDANG BIARO",
            "KEPULAUAN TANIMBAR": "MALUKU TENGGARA BARAT",
            "TOBA": "TOBA SAMOSIR",
            "MINAHASA SELATAN/BOLAANG MONGONDOW TIMUR": "MINAHASA SELATAN"
        }

    gdf["key_join"] = gdf["key_join"].replace(mapping_manual)
    df_h["key_join"] = df_h["key_join"].replace(mapping_manual)

    nama_shp = gdf["key_join"].unique()
    nama_data = df_h["key_join"].unique()

    mapping_otomatis = {}
    for n in nama_data:
        if n not in mapping_manual.values():
            match, skor = process.extractOne(n, nama_shp)[:2]
            if skor >= 85:
                mapping_otomatis[n] = match

    gdf["key_join"] = gdf["key_join"].replace(mapping_otomatis)
    df_h["key_join"] = df_h["key_join"].replace(mapping_otomatis)

    gdf_gabung = gdf.merge(df_h, on="key_join", how="inner")
    gdf_gabung["geometry"] = gdf_gabung["geometry"].simplify(0.08, preserve_topology=True)

    return gdf_gabung

#Method untuk menampilkan peta
def tampilkan_peta(gdf: gpd.GeoDataFrame, skor: pd.Series, label_cluster: dict, nama_algo: str = "iK-Median", fitur_digunakan=None):
    if fitur_digunakan is None:
        fitur_digunakan = []

    norm = mcolors.Normalize(vmin=float(skor.min()), vmax=float(skor.max()))
    cmap = cm.get_cmap("RdYlGn")
    warna_cluster = {
        c: mcolors.to_hex(cmap(norm(float(s))))
        for c, s in skor.items()
    }

    nama_kolom_namobj = "NAMOBJ" if "NAMOBJ" in gdf.columns else gdf.columns[0]
    tooltip_fields = [nama_kolom_namobj] + [f for f in fitur_digunakan if f in gdf.columns] + ["Cluster"]
    tooltip_aliases = ["Wilayah"] + [indikator_deskripsi.get(f, f) for f in fitur_digunakan] + ["Cluster"]

    m = folium.Map(
        location=[-2.5, 118],
        zoom_start=5,
        tiles="OpenStreetMap",
        prefer_canvas=True
    )

    folium.GeoJson(
        gdf.to_json(),
        style_function=lambda feature: {
            "fillColor": warna_cluster.get(feature["properties"]["Cluster"], "#ffffff"),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.3,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True,
            sticky=True,
            direction="top" 
        )
    ).add_to(m)

    legenda_item = "".join([
        f'<div style="display:flex;align-items:center;margin-bottom:4px;">'
        f'<span style="display:inline-block;width:15px;height:15px;'
        f'background:{warna_cluster[c]};margin-right:8px;border:1px solid #777;"></span>'
        f'<span>Cluster {c}</span>'
        f'</div>'
        for c in sorted(warna_cluster.keys())
    ])

    legenda_html = f"""
    <div style="
        position: absolute;
        top: 30px; right: 30px;
        width: 300px; height: auto;
        background-color: white;
        border: 1px solid #999;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        z-index: 9999;
        font-size: 13px;
        padding: 10px 12px;
        color: #111;
        line-height: 1.3;
    ">
        <div style="font-weight: 600; margin-bottom: 6px;">
            Keterangan Cluster — {nama_algo}
        </div>
        {legenda_item}
    </div>
    """

    m.get_root().html.add_child(folium.Element(legenda_html))
    return m