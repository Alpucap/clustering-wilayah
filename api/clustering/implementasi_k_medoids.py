import numpy as np
from scipy.spatial.distance import cdist

#Method untuk assign cluster k-medoids
def assign_cluster_medoids(distance_matrix, medoids):
    labels = np.argmin(distance_matrix[:, medoids], axis=1)
    return labels

#Method untuk hitung total cost
def hitung_total_cost(distance_matrix, medoids, labels):
    n = distance_matrix.shape[0]
    return distance_matrix[np.arange(n), medoids[labels]].sum()

#Method untuk iterasi K-Medoids
def iterasi_k_medoids(data_matriks, jumlah_cluster, metrik_jarak="euclidean", max_iterasi=100):
    n = len(data_matriks)

    distance_matrix = cdist(data_matriks, data_matriks, metric=metrik_jarak)

    #Init medoid acak
    rng = np.random.default_rng()
    medoids = rng.choice(n, jumlah_cluster, replace=False)

    #Assign awal & cost awal
    labels = assign_cluster_medoids(distance_matrix, medoids)
    best_cost = hitung_total_cost(distance_matrix, medoids, labels)

    for it in range(max_iterasi):
        improved = False

        is_medoid = np.zeros(n, dtype=bool)
        is_medoid[medoids] = True
        candidates = np.flatnonzero(~is_medoid)

        for m_idx in range(jumlah_cluster):
            for kandidat in candidates:

                #coba swap
                medoids_coba = medoids.copy()
                medoids_coba[m_idx] = kandidat

                labels_coba = assign_cluster_medoids(distance_matrix, medoids_coba)
                cost_baru = hitung_total_cost(distance_matrix, medoids_coba, labels_coba)

                if cost_baru < best_cost:
                    best_cost = cost_baru
                    medoids = medoids_coba
                    labels = labels_coba
                    improved = True

        if not improved:
            print(f"Konvergen di iterasi ke-{it+1}, cost = {best_cost:.4f}")
            break

    return labels, data_matriks[medoids]