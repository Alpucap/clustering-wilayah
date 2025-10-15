import numpy as np
from scipy.spatial.distance import cdist

#Method untuk menghitung Grand Median (Center of Mass (CoM))
def hitung_grand_median(data_matrix):
    return np.median(data_matrix, axis=0, keepdims=True)

#Method untuk cari centroid pertama
def cari_centroid_pertama(data_matrix, grand_median, metrik_jarak):
    jarak = cdist(data_matrix, grand_median, metric=metrik_jarak).ravel()
    return data_matrix[np.argmax(jarak)]

#Method untuk cari centroid kedua
def cari_centroid_kedua(data_matrix, centroid_pertama, metrik_jarak):
    jarak = cdist(data_matrix, centroid_pertama.reshape(1, -1), metric=metrik_jarak).ravel()
    return data_matrix[np.argmax(jarak)]

#Method untuk update centroid di iterasi k-median
def update_centroid_kmedian(data_matrix, labels, k):
    centroids = []
    for i in range(k):
        cluster_data = data_matrix[labels == i]
        if len(cluster_data) == 0:
            continue

        centroids.append(np.median(cluster_data, axis=0))
    return np.array(centroids)

#Method untuk melakukan iterasi K-Median
def iterasi_k_median(data_matrix, init_centroids, metrik_jarak, max_iter=100):
    centroids = np.array(init_centroids)
    labels = None

    for _ in range(max_iter):
        #Assign cluster
        jarak_matrix = cdist(data_matrix, centroids, metric=metrik_jarak)
        new_labels = np.argmin(jarak_matrix, axis=1)

        #Cek konvergen
        if labels is not None and np.array_equal(new_labels, labels):
            break
        labels = new_labels

        #Update centroid pakai median
        centroids = update_centroid_kmedian(data_matrix, labels, len(centroids))

    return labels, centroids

#Method untuk mencari kandidat centroid
def cari_kandidat_centroid(data_matrix, labels, centroids, metrik_jarak):
    kandidat_centroid = []
    
    for i, centroid in enumerate(centroids):
        cluster_data = data_matrix[labels == i]
        if len(cluster_data) == 0:
            continue
        
        #Titik terjauh dari centroid di cluster itu
        jarak_cluster = cdist(cluster_data, centroid.reshape(1, -1), metric=metrik_jarak).ravel()
        titik_terjauh = cluster_data[np.argmax(jarak_cluster)]
        kandidat_centroid.append(titik_terjauh)
        
    return kandidat_centroid

#Method untuk memilih centroid yang baru
def pilih_centroid_baru(kandidat, centroids, metrik_jarak):
    C = np.asarray(centroids)
    best, best_avg = None, -np.inf
    for calon in kandidat:
        d = cdist(np.array([calon]), C, metric=metrik_jarak).ravel()
        avg = d.mean()
        if avg > best_avg:
            best, best_avg = calon, avg
    return best

#Method untuk iterasi Intelligent K-Median
def iterasi_i_k_median(data_matrix, metrik_jarak="cityblock", max_iter=100):
    #Casting
    data_matrix = np.asarray(data_matrix, dtype=float)

    #Inisialisasi
    grand_median = hitung_grand_median(data_matrix)
    c1 = cari_centroid_pertama(data_matrix, grand_median, metrik_jarak)
    c2 = cari_centroid_kedua(data_matrix, c1, metrik_jarak)
    list_centroid = np.vstack([c1, c2])

    while True:
        #Jalankan K-Median untuk cluster saat ini
        labels, centroids = iterasi_k_median(data_matrix, list_centroid, metrik_jarak, max_iter)

        #Cari kandidat centroid baru
        kandidat_centroid = cari_kandidat_centroid(data_matrix, labels, centroids, metrik_jarak)
        if not kandidat_centroid:
            break

        #Pilih centroid baru dari kandidat
        centroid_baru = pilih_centroid_baru(kandidat_centroid, centroids, metrik_jarak)

        #Stop kalau centroid baru sudah ada di list_centroid (titik terpilih sebelumnya)
        if any(np.array_equal(centroid_baru, c) for c in list_centroid):
            break

        #Tambahkan centroid baru (dari data asli), bukan median
        list_centroid = np.vstack([list_centroid, centroid_baru])

    return labels, centroids