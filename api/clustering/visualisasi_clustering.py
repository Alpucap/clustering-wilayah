import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
from fuzzywuzzy import process

#Label scheme
label_schemes = {
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

label_desc = {
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

#Method untuk mengambil label scheme
def get_label_scheme(k: int):
    return label_schemes.get(k, [f"Cluster {i+1}" for i in range(k)])

#Method untuk analisis cluster
def analisis_cluster(df, fitur_dipakai, algo=""):
    #Bagi fitur ke positif & negatif
    fitur_pos = [c for c in ["AHH_L","AHH_P","RLS"] if c in fitur_dipakai]
    fitur_neg = [c for c in ["P0","P1","P2"] if c in fitur_dipakai]
    fitur_all = fitur_pos + fitur_neg

    if not fitur_all:
        raise ValueError("Tidak ada fitur yang valid untuk analisis cluster.")

    print(f"Analisis {algo} dengan fitur: {fitur_all}")

    #Jumlah anggota cluster
    jumlah = df["Cluster"].value_counts().sort_index()
    print("Jumlah anggota per cluster:")
    print(jumlah, "\n")

    #Rata-rata indikator per cluster (hanya fitur terpilih)
    mean_c = df.groupby("Cluster")[fitur_all].mean().round(3)
    print("Rata-rata indikator per cluster:")
    print(mean_c, "\n")

    #Skor gabungan  (rata-rata positif - rata-rata negatif)
    if fitur_pos and fitur_neg:
        score = (mean_c[fitur_pos].mean(axis=1) - mean_c[fitur_neg].mean(axis=1))
    elif fitur_pos:  # hanya fitur positif
        score = mean_c[fitur_pos].mean(axis=1)
    else:  # hanya fitur negatif
        score = -mean_c[fitur_neg].mean(axis=1)

    #Ranking cluster
    rank = score.sort_values(ascending=False)
    order = rank.index.tolist()
    K = len(rank)

    #Label cluster sesuai jumlah K
    scheme = get_label_scheme(K)
    labels = {order[i]: scheme[i] for i in range(K)}

    print("Label cluster:", labels, "\n")

    return mean_c, labels, score

#Method untuk visualisasi ringkasan cluster
def ringkasan_cluster(df, judul="Ringkasan Cluster"):
    s = df["Cluster"].astype("Int64")
    counts = s.value_counts().sort_index()
    K = int(counts.index.max()) + 1
    counts = counts.reindex(range(K), fill_value=0)
    total = counts.sum()

    summary = pd.DataFrame({
        "Cluster": counts.index,
        "Jumlah": counts.values,
        "Persen": (counts.values / total * 100).round(1)
    })

    fig, ax = plt.subplots(figsize=(4,3))
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, K))
    bars = ax.bar(summary["Cluster"].astype(str), summary["Jumlah"], color=colors)
    for bar, v, p in zip(bars, summary["Jumlah"], summary["Persen"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{v} ({p}%)", ha="center", va="bottom", fontsize=8)
    ax.set_title(f"{judul} (K={K})", fontsize=10)
    ax.set_xlabel("Cluster", fontsize=9)
    ax.set_ylabel("Jumlah Wilayah", fontsize=9)
    fig.tight_layout()

    return summary, fig


#Method untuk visualisasi evaluasi
def visualisasi_evaluasi(df_eval):
    fig, axes = plt.subplots(1, 3, figsize=(15,4))
    for algo, subset in df_eval.groupby("Algoritma"):
        axes[0].plot(subset["K"], subset["Silhouette"], marker="o", label=algo)
        axes[1].plot(subset["K"], subset["DBI"], marker="o", label=algo)
        axes[2].plot(subset["K"], subset["Waktu (detik)"], marker="o", label=algo)

    axes[0].set_title("Koefisien Silhouette vs K")
    axes[1].set_title("Indeks DBI vs K")
    axes[2].set_title("Waktu Eksekusi vs K")
    for ax in axes: ax.legend(); ax.set_xlabel("Jumlah Cluster (K)")
    plt.tight_layout()
    return fig

#Method untuk melakukan visualisasi silhouette secara keseluruhan
def visualisasi_silhouette_full(data_matriks, labels, algo=""):
    from sklearn.metrics import silhouette_samples, silhouette_score
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np

    sample_silhouette_values = silhouette_samples(data_matriks, labels)
    silhouette_avg = silhouette_score(data_matriks, labels)

    n_clusters = len(np.unique(labels))
    y_lower = 5
    
    fig, ax1 = plt.subplots(figsize=(6, 5))

    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i), fontsize=9)
        y_lower = y_upper + 5

    ax1.set_title(f"Plot Silhouette untuk berbagai Cluster ({algo})", fontsize=11, pad=10) 
    ax1.set_xlabel("Nilai Silhouette Coefficient", fontsize=10)
    ax1.set_ylabel("Label Cluster", fontsize=10)

    #Garis rata-rata
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--", linewidth=1.5)

    ax1.set_yticks([])
    ax1.set_xticks(np.linspace(-0.1, 1.0, 6))
    ax1.tick_params(axis="both", labelsize=9)

    plt.tight_layout(pad=1)
    return fig

#Method untuk visualisasi sebaran cluster
def visualisasi_sebaran_cluster_per_indikator(df, fitur_dipakai, algo=""):
    cols = [c for c in fitur_dipakai if c in df.columns]

    if not cols:
        raise ValueError("Tidak ada fitur valid untuk divisualisasikan.")

    g = sns.pairplot(
        df, vars=cols, hue="Cluster", diag_kind="kde",
        plot_kws={"alpha":0.7, "s":30}
    )
    g.fig.suptitle(f"Scatter Matrix per Cluster ({algo})", y=1.02)
    return g

#Method untuk visualisasi ringkasan cluster
def boxgrid_per_cluster(df, vars_, title_prefix):
    df = df.copy()
    df["Cluster"] = df["Cluster"].astype(int)

    n_vars = len(vars_)
    n_cols = 3
    n_rows = (n_vars + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    axes = axes.flatten()

    for i, var in enumerate(vars_):
        if var not in df.columns:
            continue
        sns.boxplot(
            data=df, x="Cluster", y=var, hue="Cluster",
            palette="Set2", legend=False, ax=axes[i]
        )
        axes[i].set_title(var)

    #hapus axes kosong kalau jumlah var < n_rows*n_cols
    for j in range(len(vars_), len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle(title_prefix, y=1.02, fontsize=12)
    plt.tight_layout()
    return fig

#Method untuk melihat korelasi antar variabel
def heatmap_correlation(df, vars_, title="Korelasi Antar Variabel"):
    corr = df[vars_].corr(method="pearson")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f",
                xticklabels=vars_, yticklabels=vars_, ax=ax, 
                annot_kws={"fontsize": 9}, cbar_kws={"shrink": 0.8})
    ax.set_title(title, fontsize=12, pad=10)
    ax.tick_params(axis='both', labelsize=9)
    plt.tight_layout()
    return fig

#Pemetaan
#Method untuk normalisasi nama
def normalize_name(name):
    if pd.isna(name):
        return name
    return name.upper().strip()

#Method untuk persiapan shapefile
def persiapkan_shapefile(path: str, df_hasil: pd.DataFrame, mapping_fix: dict = None):
    if path.endswith(".gdb"):
        gdf = gpd.read_file(path, layer="ADMINISTRASI_AR_KABKOTA")
    else:
        gdf = gpd.read_file(path)

    gdf = gdf.to_crs(4326)

    #Kolom nama wilayah
    nama_col = "NAMOBJ" if "NAMOBJ" in gdf.columns else gdf.columns[0]

    #Normalisasi
    gdf["key_join"] = gdf[nama_col].apply(normalize_name)
    df_hasil = df_hasil.copy()
    df_hasil["key_join"] = df_hasil["Nama Wilayah"].apply(normalize_name)

    #Mapping manual
    if mapping_fix is None:
        mapping_fix = {
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
    gdf["key_join"] = gdf["key_join"].replace(mapping_fix)
    df_hasil["key_join"] = df_hasil["key_join"].replace(mapping_fix)

    #Menggunakan Fuzzy Mapping
    nama_shp = gdf["key_join"].unique()
    nama_data = df_hasil["key_join"].unique()

    mapping_auto = {}
    for n in nama_data:
        if n not in mapping_fix.values():
            match, score = process.extractOne(n, nama_shp)[:2]
            if score >= 85:   # threshold cocok
                mapping_auto[n] = match

    gdf["key_join"] = gdf["key_join"].replace(mapping_auto)
    df_hasil["key_join"] = df_hasil["key_join"].replace(mapping_auto)

    #merge
    gdf_merged = gdf.merge(df_hasil, on="key_join", how="inner")
    gdf_merged["geometry"] = gdf_merged["geometry"].simplify(0.01, preserve_topology=True)
    
    return gdf_merged

#Method untuk tampilkan peta
def tampilkan_peta(gdf, score, labels, algo_name="iK-Median", fitur_dipakai=None):
    # Warna cluster
    norm = mcolors.Normalize(vmin=score.min(), vmax=score.max())
    cmap = cm.get_cmap("RdYlGn")
    cluster_colors = {
        cluster: mcolors.to_hex(cmap(norm(s)))
        for cluster, s in score.items()
    }
    
    if fitur_dipakai is None:
        fitur_dipakai = []

    tooltip_fields = ["NAMOBJ"] + [f for f in fitur_dipakai if f in gdf.columns] + ["Cluster"]
    tooltip_aliases = ["Wilayah"] + [f for f in fitur_dipakai if f in gdf.columns] + ["Cluster"]

    m = folium.Map(
        location=[-2.5, 118],
        zoom_start=4,
        tiles="OpenStreetMap",
        prefer_canvas=True
    )
    

    folium.GeoJson(
        gdf.to_json(),
        style_function=lambda feature: {
            "fillColor": cluster_colors.get(feature["properties"]["Cluster"], "#ffffff"),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.8,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True
        )
    ).add_to(m)

    #Legend
    legend_items = "".join([
        f'<i style="background:{cluster_colors[c]}; width:15px; height:15px; '
        f'float:left; margin-right:8px; opacity:0.8;"></i>'
        f'Cluster {c}: {labels.get(c, "Tidak Diketahui")}<br>'
        for c in sorted(cluster_colors.keys())
    ])

    legend_html = f"""
    <div style="
        position: absolute;
        top: 30px; right: 30px;
        width: 280px; height: auto;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:13px;
        padding: 10px;
        color: black;
    ">
    <b>Keterangan Cluster {algo_name}</b><br>
    {legend_items}
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    return m
