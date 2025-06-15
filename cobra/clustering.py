"""
Clustering functions for brain connectivity analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform


def prepare_clustering_data(connectivity_matrix, regions):
    """
    Prepare data for clustering analysis.
    
    Parameters
    ----------
    connectivity_matrix : array-like
        Correlation matrix between brain regions
    regions : list
        List of region names
        
    Returns
    -------
    distance_matrix : ndarray
        Distance matrix derived from correlations
    condensed_distances : ndarray
        Condensed distance matrix for hierarchical clustering
    linkage_matrix : ndarray
        Linkage matrix from hierarchical clustering
    """
    # Convert correlation to distance (1 - correlation for positive correlations)
    distance_matrix = 1 - connectivity_matrix

    # Ensure distance matrix is valid (non-negative, symmetric)
    distance_matrix = np.maximum(distance_matrix, 0)
    distance_matrix = (distance_matrix + distance_matrix.T) / 2
    np.fill_diagonal(distance_matrix, 0)

    # Convert to condensed form for hierarchical clustering
    condensed_distances = squareform(distance_matrix)

    # Perform hierarchical clustering
    linkage_matrix = linkage(condensed_distances, method='ward')

    return distance_matrix, condensed_distances, linkage_matrix


def create_clustered_correlation_matrix(connectivity_matrix, regions, n_clusters=None,
                                      figsize=(14, 12), region_colors=None,
                                      show_labels=True, label_interval=1):
    """
    Create and display the clustered correlation matrix with cluster boundaries.

    Parameters
    ----------
    connectivity_matrix : array-like
        Correlation matrix
    regions : list
        List of region names
    n_clusters : int, optional
        Number of clusters (auto-determined if None)
    figsize : tuple, default=(14, 12)
        Figure size (width, height)
    region_colors : list, optional
        List of colors for region labels (same length as regions)
    show_labels : bool, default=True
        Whether to show tick labels
    label_interval : int, default=1
        Show every nth label to reduce crowding

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    ax : matplotlib.axes.Axes
        Axes object
    cluster_labels : ndarray
        Cluster assignments for each region
    reordered_matrix : ndarray
        Reordered correlation matrix
    reordered_regions : list
        Reordered list of region names
    """
    # Prepare clustering data
    distance_matrix, condensed_distances, linkage_matrix = prepare_clustering_data(
        connectivity_matrix, regions)

    # Determine optimal number of clusters if not provided
    if n_clusters is None:
        n_clusters = min(8, max(3, len(regions) // 4))

    # Get cluster assignments
    cluster_labels = fcluster(linkage_matrix, n_clusters, criterion='maxclust')

    # Reorder matrix based on clustering
    cluster_order = np.argsort(cluster_labels)
    reordered_matrix = connectivity_matrix[cluster_order, :][:, cluster_order]
    reordered_regions = [regions[i] for i in cluster_order]
    reordered_clusters = cluster_labels[cluster_order]

    # Reorder colors if provided
    reordered_colors = None
    if region_colors is not None:
        reordered_colors = [region_colors[i] for i in cluster_order]

    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)

    im = ax.imshow(reordered_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    ax.set_title(f'Clustered Correlation Matrix ({n_clusters} clusters)',
                fontsize=16, fontweight='bold', pad=20)

    if show_labels:
        # Show labels at specified intervals
        tick_positions = range(0, len(reordered_regions), label_interval)
        tick_labels = [reordered_regions[i] for i in tick_positions]

        ax.set_xticks(tick_positions)
        ax.set_yticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=90, fontsize=6, ha='center')
        ax.set_yticklabels(tick_labels, fontsize=6, va='center')

        # Apply custom colors if provided
        if reordered_colors is not None:
            tick_colors = [reordered_colors[i] for i in tick_positions]
            for tick, color in zip(ax.get_xticklabels(), tick_colors):
                tick.set_color(color)
            for tick, color in zip(ax.get_yticklabels(), tick_colors):
                tick.set_color(color)
    else:
        ax.set_xticks([])
        ax.set_yticks([])

    # Add cluster boundaries
    cluster_boundaries = []
    current_cluster = reordered_clusters[0]
    for i, cluster in enumerate(reordered_clusters):
        if cluster != current_cluster:
            cluster_boundaries.append(i - 0.5)
            current_cluster = cluster

    for boundary in cluster_boundaries:
        ax.axhline(y=boundary, color='black', linewidth=2)
        ax.axvline(x=boundary, color='black', linewidth=2)

    plt.colorbar(im, ax=ax, label='Kendall Tau', shrink=0.8)
    plt.tight_layout()
    plt.show()

    return fig, ax, cluster_labels, reordered_matrix, reordered_regions


def analyze_clusters(connectivity_matrix, regions, cluster_labels):
    """
    Provide detailed cluster analysis with statistics.
    
    Parameters
    ----------
    connectivity_matrix : array-like
        Correlation matrix
    regions : list
        List of region names
    cluster_labels : array-like
        Cluster assignments for each region
    """
    print("=== CLUSTER ANALYSIS ===\n")

    n_clusters = len(np.unique(cluster_labels))

    for cluster_id in range(1, n_clusters + 1):
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        cluster_regions = [regions[i] for i in cluster_indices]

        print(f"CLUSTER {cluster_id} ({len(cluster_regions)} regions):")
        print("Regions:", ", ".join(cluster_regions))

        # Calculate within-cluster correlations
        if len(cluster_indices) > 1:
            cluster_matrix = connectivity_matrix[np.ix_(cluster_indices, cluster_indices)]
            # Get upper triangular part (excluding diagonal)
            upper_tri = np.triu(cluster_matrix, k=1)
            within_cluster_corrs = upper_tri[upper_tri != 0]

            print(f"Within-cluster correlations:")
            print(f"  Mean: {np.mean(within_cluster_corrs):.3f}")
            print(f"  Std:  {np.std(within_cluster_corrs):.3f}")
            print(f"  Range: [{np.min(within_cluster_corrs):.3f}, {np.max(within_cluster_corrs):.3f}]")
        else:
            print("Single region cluster - no within-cluster correlations")

        print("-" * 50)


def create_main_clustering_visualization(connectivity_matrix, regions, n_clusters=None,
                                       region_colors=None, show_labels=True, label_interval=5):
    """
    Main function that creates the clustered correlation matrix (primary visualization).

    Parameters
    ----------
    connectivity_matrix : array-like
        Correlation matrix
    regions : list
        List of region names
    n_clusters : int, optional
        Number of clusters
    region_colors : list, optional
        List of colors for region labels
    show_labels : bool, default=True
        Whether to show region labels
    label_interval : int, default=5
        Show every nth label (default 5 for 150 regions)
        
    Returns
    -------
    cluster_labels : ndarray
        Cluster assignments
    reordered_matrix : ndarray
        Reordered correlation matrix
    reordered_regions : list
        Reordered region names
    """
    print("Creating clustered correlation matrix visualization...")
    fig, ax, cluster_labels, reordered_matrix, reordered_regions = create_clustered_correlation_matrix(
        connectivity_matrix, regions, n_clusters, region_colors=region_colors,
        show_labels=show_labels, label_interval=label_interval
    )

    return cluster_labels, reordered_matrix, reordered_regions
