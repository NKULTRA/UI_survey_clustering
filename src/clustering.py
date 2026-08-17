"""
Clustering functions for the OSMI Mental Health in Tech survey.
"""

import gower
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
from yellowbrick.cluster import KElbowVisualizer


def perform_kmeans_clustering(df, n_clusters=3, random_state=42):
    """
    Perform KMeans clustering on the given data.

    Parameters:
    - df: DataFrame, the input data for clustering.
    - n_clusters: int, the number of clusters to form.
    - random_state: int, random seed for reproducibility.

    Returns:
    - kmeans: Fitted KMeans model.
    - labels: Cluster labels for each point in the dataset.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    kmeans.fit(df)
    labels = kmeans.labels_
    return kmeans, labels


def plot_elbow_method(df, max_k=10, metric='distortion'):
    """
    Plot the elbow method (or silhouette score) to determine the optimal
    number of clusters.

    Parameters:
    - df: DataFrame, the input data for clustering.
    - max_k: int, the maximum number of clusters to test.
    - metric: str, 'distortion' (default, inertia -- classic elbow) or
      'silhouette'.

    Returns:
    - visualizer: fitted KElbowVisualizer (visualizer.elbow_value_ gives
      the detected optimal k).
    """
    model = KMeans(random_state=42, n_init=10)
    visualizer = KElbowVisualizer(model, k=(2, max_k), metric=metric)
    visualizer.fit(df)
    visualizer.show()
    return visualizer


def compute_gower_distance_matrix(df, numeric_cols):
    """
    Compute the Gower distance matrix for a mixed-type feature matrix.

    Parameters:
    - df: DataFrame, fully encoded feature matrix (no NaN, no non-numeric
      dtypes).
    - numeric_cols: list of column names to treat as numeric/ordinal
      (scaled absolute difference). Every other column is treated as
      categorical (exact match/mismatch). Typically ["age"] plus
      feature_config.ORDINAL_COLUMNS -- see DECISIONS.md for why ordinal
      columns are classified as numeric here (no dedicated ordinal mode
      in this package).

    Returns:
    - distance_matrix: n x n numpy array of pairwise Gower distances (0-1).
    """
    cat_features = [col not in numeric_cols for col in df.columns]
    return gower.gower_matrix(df, cat_features=cat_features)


def perform_hierarchical_clustering(distance_matrix, n_clusters, linkage_method='average'):
    """
    Perform agglomerative hierarchical clustering from a precomputed
    distance matrix (e.g. Gower distance -- NOT compatible with Ward
    linkage, which requires true Euclidean geometry; use 'average' or
    'complete' instead. 'complete' resists chaining better than
    'average' for weak-structure data -- see DECISIONS.md).

    Parameters:
    - distance_matrix: n x n precomputed distance matrix.
    - n_clusters: int, number of flat clusters to extract.
    - linkage_method: str, passed to scipy.cluster.hierarchy.linkage.

    Returns:
    - Z: the linkage matrix (for plotting a dendrogram).
    - labels: cluster assignment per row.
    """
    condensed_dist = squareform(distance_matrix, checks=False)
    Z = linkage(condensed_dist, method=linkage_method)
    labels = fcluster(Z, t=n_clusters, criterion='maxclust')
    return Z, labels


def plot_dendrogram(Z, truncate_mode='lastp', p=30):
    """
    Plot a dendrogram from a precomputed linkage matrix.
    """
    plt.figure(figsize=(12, 6))
    dendrogram(Z, truncate_mode=truncate_mode, p=p)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample index (or cluster size)")
    plt.ylabel("Distance")
    plt.show()


def perform_gmm_clustering(df, n_components=3, random_state=42):
    """
    Perform Gaussian Mixture Model clustering. Genuinely different
    mechanism from K-means/hierarchical: fits probability distributions
    (soft, density-based) rather than partitioning by geometric distance
    -- covered explicitly in the course book, unlike Gower distance.

    Still operates in Euclidean feature space (like K-means), not a
    precomputed distance matrix -- run on the scaled numeric matrix
    (X_scaled_df), not the Gower distance matrix.

    Parameters:
    - df: DataFrame or array, the scaled feature matrix.
    - n_components: int, number of mixture components (clusters).
    - random_state: int, for reproducibility.

    Returns:
    - gmm: fitted GaussianMixture model.
    - labels: hard cluster assignment per row (argmax of soft membership).
    """
    gmm = GaussianMixture(n_components=n_components, random_state=random_state)
    labels = gmm.fit_predict(df)
    return gmm, labels


def plot_gmm_bic_scan(df, max_k=10, random_state=42):
    """
    Scan a range of component counts and plot BIC (Bayesian Information
    Criterion) -- GMM's own model-selection metric, distinct from
    silhouette score. Lower BIC = better balance of fit quality vs.
    model complexity. Use alongside silhouette score, not instead of it:
    BIC picks the best-fitting probabilistic model; silhouette measures
    how well-separated the resulting hard cluster assignments are --
    they can disagree, and both are worth reporting if they do.

    Returns:
    - bic_scores: dict {k: bic_score}, so the chosen k can be justified
      explicitly rather than just eyeballing the plot.
    """
    bic_scores = {}
    for k in range(2, max_k + 1):
        gmm = GaussianMixture(n_components=k, random_state=random_state)
        gmm.fit(df)
        bic_scores[k] = gmm.bic(df)

    plt.plot(list(bic_scores.keys()), list(bic_scores.values()), marker='o')
    plt.xlabel('Number of components (k)')
    plt.ylabel('BIC')
    plt.title('GMM Model Selection (BIC)')
    plt.show()

    return bic_scores