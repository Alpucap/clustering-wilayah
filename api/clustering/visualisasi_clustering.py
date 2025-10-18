# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from sklearn.metrics import silhouette_samples, silhouette_score
from fuzzywuzzy import process
import gdown, os, zipfile
import tempfile

#Deskripsi Indikator
indikator_deskripsi = {
    "AHH_L": "Angka Harapan Hidup Laki-laki",
    "AHH_P": "Angka Harapan Hidup Perempuan",
    "RLS":  "Rata-Rata Lama Sekolah (tahun)",
    "P0":   "Persentase Penduduk Miskin",
    "P1":   "Indeks Kedalaman Kemiskinan",
    "P2":   "Indeks Keparahan Kemiskinan"
}

#Skema Label Cluster & Deskripsi
skema_label = {
    2:  ["Sejahtera", "Tertinggal"],
    3:  ["Sejahtera", "Menengah", "Tertinggal"],
    4:  ["Sejahtera", "Menengah Atas", "Menengah Bawah", "Tertinggal"],
    5:  ["Sejahtera", "Menengah Atas", "Menengah", "Menengah Bawah", "Tertinggal"],
    6:  ["Sejahtera", "Cukup Sejahtera", "Menengah Atas", "Menengah Bawah", "Rentan", "Tertinggal"],
    7:  ["Sejahtera", "Cukup Sejahtera", "Menengah Atas", "Menengah", "Menengah Bawah", "Rentan", "Tertinggal"],
    8:  ["Sejahtera", "Cukup Sejahtera", "Menengah Atas", "Menengah", "Menengah Bawah", "Cukup Rentan", "Rentan", "Tertinggal"],
    9:  ["Sejahtera", "Cukup Sejahtera", "Menengah Atas", "Menengah", "Menengah Bawah", "Cukup Rentan", "Rentan", "Sangat Rentan", "Tertinggal"],
    10: ["Sejahtera", "Cukup Sejahtera", "Menengah Atas", "Menengah", "Menengah Bawah", "Cukup Rentan", "Rentan", "Sangat Rentan", "Tertinggal", "Tertinggal Berat"],
    11: ["Sejahtera Tinggi", "Sejahtera", "Cukup Sejahtera", "Menengah Atas", "Menengah", "Menengah Bawah", "Cukup Rentan", "Rentan", "Sangat Rentan", "Tertinggal", "Tertinggal Berat"],
}

deskripsi_label = {
    "Sejahtera": "AHH & RLS tinggi; P0/P1/P2 rendah.",
    "Sejahtera Tinggi": "Indikator positif sangat tinggi; kemiskinan sangat rendah.",
    "Cukup Sejahtera": "Mendekati sejahtera; kemiskinan rendah–sedang.",
    "Menengah Atas": "Di atas rata-rata; kemiskinan terkendali.",
    "Menengah": "Sekitar rata-rata pada semua indikator.",
    "Menengah Bawah": "Sedikit di bawah rata-rata; kemiskinan menengah.",
    "Cukup Rentan": "Mulai menunjukkan kerentanan; kemiskinan sedang–tinggi.",
    "Rentan": "Indikator positif rendah; kemiskinan tinggi.",
    "Sangat Rentan": "Positif sangat rendah; kemiskinan sangat tinggi.",
    "Tertinggal": "AHH & RLS rendah; P0/P1/P2 tinggi.",
    "Tertinggal Berat": "Kondisi sosial-ekonomi paling rendah di rentang cluster."
}

def ambil_skema_label(jumlah_k: int):
    """Ambil daftar label cluster berdasarkan jumlah K."""
    return skema_label.get(jumlah_k, [f"Cluster {i+1}" for i in range(jumlah_k)])


#Analisis Cluster
def analisis_cluster(df: pd.DataFrame, fitur_digunakan, algoritma: str = ""):
    """
    df: DataFrame yang minimal punya kolom:
        - 'Cluster' (int)
        - indikator sesuai fitur_digunakan (mis: AHH_L, AHH_P, RLS, P0, P1, P2)
    fitur_digunakan: list nama kolom indikator dipakai
    algoritma: nama algoritma (untuk logging saja)
    """
    fitur_positif = [c for c in ["AHH_L", "AHH_P", "RLS"] if c in fitur_digunakan]
    fitur_negatif = [c for c in ["P0", "P1", "P2"] if c in fitur_digunakan]
    fitur_semua  = fitur_positif + fitur_negatif

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
    urutan  = ranking.index.tolist()
    k       = len(ranking)

    skema          = ambil_skema_label(k)
    label_cluster  = {urutan[i]: skema[i] for i in range(k)}
    print("Label cluster:", label_cluster, "\n")

    return rata_c, label_cluster, skor


#Ringkasan Cluster
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


#Visualisasi Evaluasi
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


#Visualisasi Silhouette
def visualisasi_silhouette_full(data_matriks: np.ndarray, label_cluster: np.ndarray, algo: str = ""):
    nilai_sample = silhouette_samples(data_matriks, label_cluster)
    nilai_rata   = silhouette_score(data_matriks, label_cluster)

    n_clusters = len(np.unique(label_cluster))
    y_bawah = 5
    
    fig, ax1 = plt.subplots(figsize=(6, 5))

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
    ax1.axvline(x=nilai_rata, color="red", linestyle="--", linewidth=1.5)

    ax1.text(
        nilai_rata, 
        -5,
        f"{nilai_rata:.2f}", 
        color="red", 
        fontsize=9, 
        ha="left", 
        va="bottom"
    )

    ax1.set_yticks([])
    ax1.set_xticks(np.linspace(-0.1, 1.0, 6))
    ax1.tick_params(axis="both", labelsize=9)

    plt.tight_layout(pad=1)
    return fig


#Visualisasi Sebaran (pairplot)
def visualisasi_sebaran_cluster_per_indikator(df: pd.DataFrame, fitur_digunakan, algo: str = ""):
    kolom = [c for c in fitur_digunakan if c in df.columns]
    if not kolom:
        raise ValueError("Tidak ada fitur valid untuk divisualisasikan.")

    df_plot = df.rename(columns={k: indikator_deskripsi.get(k, k) for k in kolom})
    kolom_jelas = [indikator_deskripsi.get(k, k) for k in kolom]

    g = sns.pairplot(
        df_plot, vars=kolom_jelas, hue="Cluster", diag_kind="kde",
        plot_kws={"alpha": 0.7, "s": 30}
    )
    g.figure.suptitle(f"Scatter Matrix per Cluster ({algo})", y=1.02)
    return g



#Boxplot distribusi indikator per cluster
def boxgrid_per_cluster(df: pd.DataFrame, variabel, judul: str):
    df = df.copy()
    df["Cluster"] = df["Cluster"].astype(int)

    mapping = {k: indikator_deskripsi.get(k, k) for k in variabel}
    df_plot = df.rename(columns=mapping)
    variabel_jelas = [mapping.get(v, v) for v in variabel]

    n_vars = len(variabel_jelas)
    n_cols = 3
    n_rows = (n_vars + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    axes = axes.flatten()

    for i, var in enumerate(variabel_jelas):
        if var not in df_plot.columns:
            continue
        sns.boxplot(
            data=df_plot, x="Cluster", y=var, hue="Cluster",
            palette="Set2", legend=False, ax=axes[i]
        )
        axes[i].set_title(var)

    for j in range(len(variabel_jelas), len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle(judul, y=1.02, fontsize=12)
    plt.tight_layout()
    return fig



#Heatmap korelasi indikator
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


#Normalisasi Nama Wilayah
def normalisasi_nama(nama):
    if pd.isna(nama):
        return nama
    return str(nama).upper().strip()

#Read shapefile
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

#Persiapan Shapefile
def persiapkan_shapefile(path: str, df_hasil: pd.DataFrame, mapping_manual: dict = None):
    if path.endswith(".gdb"):
        gdf = gpd.read_file(path, layer="ADMINISTRASI_AR_KABKOTA")
    else:
        gdf = gpd.read_file(path)

    gdf = gdf.to_crs(4326)

    #Tentukan kolom nama wilayah di shapefile
    kolom_nama = "NAMOBJ" if "NAMOBJ" in gdf.columns else gdf.columns[0]

    #Buat key join (upper & strip)
    gdf["key_join"] = gdf[kolom_nama].apply(normalisasi_nama)
    df_h = df_hasil.copy()
    df_h["key_join"] = df_h["Nama Wilayah"].apply(normalisasi_nama)

    #Mapping manual default (bisa diperluas)
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

    #Terapkan mapping manual ke kedua sisi
    gdf["key_join"] = gdf["key_join"].replace(mapping_manual)
    df_h["key_join"] = df_h["key_join"].replace(mapping_manual)

    #Fuzzy mapping (opsional, threshold 85)
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

    gdf_gabung["geometry"] = gdf_gabung["geometry"].simplify(0.05, preserve_topology=True)

    return gdf_gabung


#Peta Folium
def tampilkan_peta(gdf: gpd.GeoDataFrame, skor: pd.Series, label_cluster: dict, nama_algo: str = "iK-Median", fitur_digunakan=None):
    if fitur_digunakan is None:
        fitur_digunakan = []

    # Normalisasi skor → warna (hijau = lebih baik, merah = lebih rentan)
    norm = mcolors.Normalize(vmin=float(skor.min()), vmax=float(skor.max()))
    cmap = cm.get_cmap("RdYlGn")
    warna_cluster = {
        c: mcolors.to_hex(cmap(norm(float(s))))
        for c, s in skor.items()
    }

    # Field tooltip: Wilayah + indikator yang ada + Cluster
    nama_kolom_namobj = "NAMOBJ" if "NAMOBJ" in gdf.columns else gdf.columns[0]
    tooltip_fields  = [nama_kolom_namobj] + [f for f in fitur_digunakan if f in gdf.columns] + ["Cluster"]
    tooltip_aliases = ["Wilayah"] + [indikator_deskripsi.get(f, f) for f in fitur_digunakan] + ["Cluster"]

    #Peta dasar
    m = folium.Map(
        location=[-2.5, 118],
        zoom_start=4,
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
            localize=True
        )
    ).add_to(m)

    #Legend
    legenda_item = "".join([
        f'<div style="display:flex;align-items:center;margin-bottom:4px;">'
        f'<span style="display:inline-block;width:15px;height:15px;'
        f'background:{warna_cluster[c]};margin-right:8px;border:1px solid #777;"></span>'
        f'<span>Cluster {c}: {label_cluster.get(c, "Tidak Diketahui")}</span>'
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

