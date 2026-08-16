from sklearn.cluster import KMeans
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
    - metric: str, scoring metric passed to KElbowVisualizer -- 'distortion'
      (default, within-cluster sum of squares / inertia -- the classic
      "elbow method") or 'silhouette' (mean silhouette score across
      samples). Running both and comparing where they agree is more
      robust than relying on either metric alone.

    Returns:
    - visualizer: fitted KElbowVisualizer, so the detected optimal k can
      be read via visualizer.elbow_value_ without re-running.
    """
    model = KMeans(random_state=42, n_init=10)
    visualizer = KElbowVisualizer(model, k=(2, max_k), metric=metric, force_model=True)
    visualizer.fit(df)
    visualizer.show()
    return visualizer