import numpy as np
from sklearn.metrics import davies_bouldin_score, silhouette_score, pairwise_distances

#Method untuk evaluasi cluster
def evaluasi_cluster(data_matriks, label_cluster, metrik_jarak="euclidean"):
    n_clusters = len(np.unique(label_cluster))
    
    #Validasi jika jumlah cluster lebih dari 2
    if n_clusters < 2:
        return None, None

    #Silhouette Score
    sil = silhouette_score(data_matriks, label_cluster, metric=metrik_jarak)

    #DBI
    if metrik_jarak == "euclidean":
        dbi = davies_bouldin_score(data_matriks, label_cluster)

    elif metrik_jarak == "cityblock":
        clusters = np.unique(label_cluster)
        k = len(clusters)

        centroids = [np.median(data_matriks[label_cluster == c], axis=0) for c in clusters]

        sigmas = []
        for idx, c in enumerate(clusters):
            members = data_matriks[label_cluster == c]
            if len(members) > 0:
                dists = pairwise_distances(members, [centroids[idx]], metric="cityblock")
                sigmas.append(np.mean(dists))
            else:
                sigmas.append(0)

        ratios = []
        for i in range(k):
            max_ratio = -np.inf
            for j in range(k):
                if i != j:
                    d_c = np.sum(np.abs(centroids[i] - centroids[j]))  # Manhattan distance antar centroid
                    ratio = (sigmas[i] + sigmas[j]) / d_c if d_c != 0 else np.inf
                    max_ratio = max(max_ratio, ratio)
            ratios.append(max_ratio)

        dbi = np.mean(ratios)

    else:
        raise ValueError(f"Metrik '{metrik_jarak}' belum didukung untuk evaluasi.")

    return dbi, sil
