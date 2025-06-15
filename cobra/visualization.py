"""
Visualization functions for brain connectivity analysis.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_original_correlation_matrix(connectivity_matrix, regions, figsize=(12, 10),
                                   region_colors=None, show_labels=True, label_interval=1):
    """
    Plot the original correlation matrix heatmap with improved label handling.

    Parameters
    ----------
    connectivity_matrix : array-like
        Correlation matrix
    regions : list
        List of region names
    figsize : tuple, default=(12, 10)
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
    """
    fig, ax = plt.subplots(figsize=figsize)

    im = ax.imshow(connectivity_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    ax.set_title('Original Correlation Matrix', fontsize=16, fontweight='bold', pad=20)

    if show_labels:
        # Show labels at specified intervals
        tick_positions = range(0, len(regions), label_interval)
        tick_labels = [regions[i] for i in tick_positions]

        ax.set_xticks(tick_positions)
        ax.set_yticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=90, fontsize=6, ha='center')
        ax.set_yticklabels(tick_labels, fontsize=6, va='center')

        # Apply custom colors if provided
        if region_colors is not None:
            tick_colors = [region_colors[i] for i in tick_positions]
            for tick, color in zip(ax.get_xticklabels(), tick_colors):
                tick.set_color(color)
            for tick, color in zip(ax.get_yticklabels(), tick_colors):
                tick.set_color(color)
    else:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.colorbar(im, ax=ax, label='Kendall Tau', shrink=0.8)
    plt.tight_layout()
    plt.show()

    return fig, ax


def plot_cluster_summary(regions, cluster_labels, figsize=(10, 12)):
    """
    Create a text-based cluster summary visualization with better formatting.
    
    Parameters
    ----------
    regions : list
        List of region names
    cluster_labels : array-like
        Cluster assignments for each region
    figsize : tuple, default=(10, 12)
        Figure size (width, height)
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    ax : matplotlib.axes.Axes
        Axes object
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')

    n_clusters = len(np.unique(cluster_labels))

    # Create cluster summary text
    cluster_summary = "Cluster Assignments:\n\n"
    for cluster_id in range(1, n_clusters + 1):
        cluster_regions = [regions[i] for i in range(len(regions)) if cluster_labels[i] == cluster_id]
        cluster_summary += f"Cluster {cluster_id} ({len(cluster_regions)} regions):\n"

        # Format regions in columns if there are many
        if len(cluster_regions) > 10:
            # Split into multiple columns
            cols = 3
            col_size = len(cluster_regions) // cols + (1 if len(cluster_regions) % cols else 0)
            for row in range(col_size):
                line = "  "
                for col in range(cols):
                    idx = row + col * col_size
                    if idx < len(cluster_regions):
                        line += f"• {cluster_regions[idx]:<25}"
                cluster_summary += line.rstrip() + "\n"
        else:
            for region in cluster_regions:
                cluster_summary += f"  • {region}\n"
        cluster_summary += "\n"

    ax.text(0.05, 0.95, cluster_summary, transform=ax.transAxes, fontsize=8,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.7))

    plt.tight_layout()
    plt.show()

    return fig, ax


def generate_example_colors(regions, color_scheme='network'):
    """
    Generate example color schemes for regions.

    Parameters
    ----------
    regions : list
        List of region names
    color_scheme : str, default='network'
        Color scheme: 'network', 'random', 'gradient', or 'categorical'

    Returns
    -------
    list
        Colors for each region
    """
    n_regions = len(regions)

    if color_scheme == 'network':
        # Example: different colors for different brain networks
        colors = []
        for i, region in enumerate(regions):
            if 'frontal' in region.lower() or 'front' in region.lower():
                colors.append('red')
            elif 'parietal' in region.lower():
                colors.append('blue')
            elif 'temporal' in region.lower():
                colors.append('green')
            elif 'occipital' in region.lower():
                colors.append('orange')
            elif 'cingulate' in region.lower():
                colors.append('purple')
            else:
                colors.append('black')
        return colors

    elif color_scheme == 'random':
        np.random.seed(42)  # For reproducibility
        colors = plt.cm.tab20(np.random.rand(n_regions))
        return colors

    elif color_scheme == 'gradient':
        colors = plt.cm.viridis(np.linspace(0, 1, n_regions))
        return colors

    elif color_scheme == 'categorical':
        # Cycle through a set of distinct colors
        base_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        colors = [base_colors[i % len(base_colors)] for i in range(n_regions)]
        return colors

    else:
        return ['black'] * n_regions