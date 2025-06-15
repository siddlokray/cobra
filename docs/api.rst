# API Reference

This document provides a comprehensive reference for all functions and classes in the CoBRA.

## Clustering Module

### Core Functions

#### `prepare_clustering_data(connectivity_matrix, regions)`

Prepare data for clustering analysis by converting correlation matrices to distance matrices and performing hierarchical clustering.

**Parameters:**
- `connectivity_matrix` (array): Correlation matrix between brain regions
- `regions` (list): List of region names

**Returns:**
- `distance_matrix` (array): Distance matrix (1 - correlation)
- `condensed_distances` (array): Condensed distance matrix for hierarchical clustering
- `linkage_matrix` (array): Linkage matrix from hierarchical clustering

**Description:**
This function converts a correlation matrix to a distance matrix suitable for clustering analysis. It ensures the distance matrix is valid (non-negative, symmetric) and performs Ward linkage hierarchical clustering.

---

#### `plot_original_correlation_matrix(connectivity_matrix, regions, figsize=(12, 10), region_colors=None, show_labels=True, label_interval=1)`

Plot the original correlation matrix as a heatmap with customizable labeling and coloring options.

**Parameters:**
- `connectivity_matrix` (array): Correlation matrix
- `regions` (list): List of region names
- `figsize` (tuple, optional): Figure size (width, height). Default: (12, 10)
- `region_colors` (list, optional): List of colors for region labels (same length as regions)
- `show_labels` (bool, optional): Whether to show tick labels. Default: True
- `label_interval` (int, optional): Show every nth label to reduce crowding. Default: 1

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object
- `ax` (matplotlib.axes.Axes): Axes object

**Description:**
Creates a heatmap visualization of the original correlation matrix with customizable labeling to handle large numbers of brain regions effectively.

---

#### `create_clustered_correlation_matrix(connectivity_matrix, regions, n_clusters=None, figsize=(14, 12), region_colors=None, show_labels=True, label_interval=1)`

Create and display a clustered correlation matrix with cluster boundaries and improved labeling.

**Parameters:**
- `connectivity_matrix` (array): Correlation matrix
- `regions` (list): List of region names
- `n_clusters` (int, optional): Number of clusters (auto-determined if None)
- `figsize` (tuple, optional): Figure size (width, height). Default: (14, 12)
- `region_colors` (list, optional): List of colors for region labels
- `show_labels` (bool, optional): Whether to show tick labels. Default: True
- `label_interval` (int, optional): Show every nth label to reduce crowding. Default: 1

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object
- `ax` (matplotlib.axes.Axes): Axes object
- `cluster_labels` (array): Cluster assignments for each region
- `reordered_matrix` (array): Correlation matrix reordered by clusters
- `reordered_regions` (list): Region names reordered by clusters

**Description:**
Creates a clustered visualization of the correlation matrix with clear cluster boundaries. Automatically determines optimal number of clusters if not specified.

---

#### `plot_cluster_summary(regions, cluster_labels, figsize=(10, 12))`

Create a text-based cluster summary visualization with formatted cluster assignments.

**Parameters:**
- `regions` (list): List of region names
- `cluster_labels` (array): Cluster assignments for each region
- `figsize` (tuple, optional): Figure size (width, height). Default: (10, 12)

**Returns:**
- `fig` (matplotlib.figure.Figure): Figure object
- `ax` (matplotlib.axes.Axes): Axes object

**Description:**
Generates a readable text summary of cluster assignments, automatically formatting large clusters into multiple columns for better readability.

---

#### `analyze_clusters(connectivity_matrix, regions, cluster_labels)`

Provide detailed cluster analysis with statistical summaries.

**Parameters:**
- `connectivity_matrix` (array): Correlation matrix
- `regions` (list): List of region names
- `cluster_labels` (array): Cluster assignments for each region

**Description:**
Prints comprehensive statistics for each cluster including within-cluster correlation statistics (mean, standard deviation, range).

---

#### `create_main_clustering_visualization(connectivity_matrix, regions, n_clusters=None, region_colors=None, show_labels=True, label_interval=5)`

Main function that creates the primary clustered correlation matrix visualization.

**Parameters:**
- `connectivity_matrix` (array): Correlation matrix
- `regions` (list): List of region names
- `n_clusters` (int, optional): Number of clusters
- `region_colors` (list, optional): List of colors for region labels
- `show_labels` (bool, optional): Whether to show region labels. Default: True
- `label_interval` (int, optional): Show every nth label. Default: 5

**Returns:**
- `cluster_labels` (array): Cluster assignments
- `reordered_matrix` (array): Reordered correlation matrix
- `reordered_regions` (list): Reordered region names

**Description:**
Primary visualization function that creates a clean, publication-ready clustered correlation matrix.

### Utility Functions

#### `generate_example_colors(regions, color_scheme='network')`

Generate color schemes for brain regions based on various strategies.

**Parameters:**
- `regions` (list): List of region names
- `color_scheme` (str, optional): Color scheme type. Options: 'network', 'random', 'gradient', 'categorical'. Default: 'network'

**Returns:**
- `list`: Colors for each region

**Color Schemes:**
- `'network'`: Colors based on brain network anatomy (frontal=red, parietal=blue, etc.)
- `'random'`: Random colors with fixed seed for reproducibility
- `'gradient'`: Gradient colors using viridis colormap
- `'categorical'`: Cycling through distinct categorical colors

## Network Module

### Main Function

#### `make_network_graph(connectivity_matrix, regions, cluster_labels, threshold=0.5, figsize=(14, 10), save_path=None, layout_type='spring', show_labels='selective', node_colors=None, color_by='cluster', cleanliness=None, orientation='horizontal')`

Create a publication-ready network graph with extensive customization options.

**Parameters:**
- `connectivity_matrix` (array): Correlation matrix between brain regions
- `regions` (list): List of region names
- `cluster_labels` (array): Cluster assignments for each region
- `threshold` (float, optional): Minimum correlation strength to display. Default: 0.5
- `figsize` (tuple, optional): Figure size (width, height). Default: (14, 10)
- `save_path` (str, optional): Path to save the figure
- `layout_type` (str, optional): Layout algorithm. Options: 'spring', 'circular', 'force_atlas', 'kamada_kawai'. Default: 'spring'
- `show_labels` (str, optional): Label display mode. Options: 'all', 'selective', 'hubs', 'none'. Default: 'selective'
- `node_colors` (dict, list, or None, optional): Custom node colors
- `color_by` (str, optional): Node coloring scheme. Options: 'cluster', 'custom', 'degree', 'betweenness'. Default: 'cluster'
- `cleanliness` (str, optional): Preset configurations. Options: 'light', 'medium', 'heavy', 'minimal', 'labeled'
- `orientation` (str, optional): Graph orientation. Options: 'horizontal', 'vertical'. Default: 'horizontal'

**Returns:**
- `G` (networkx.Graph): The network graph object
- `pos` (dict): Node positions for the layout

**Layout Types:**
- `'spring'`: Force-directed layout with spring model
- `'circular'`: Nodes arranged in a circle
- `'kamada_kawai'`: Force-directed layout using Kamada-Kawai algorithm
- `'force_atlas'`: Force-directed layout with edge weights

**Label Display Options:**
- `'all'`: Show all region labels with intelligent abbreviation
- `'selective'`: Show labels for high-degree nodes (top 20%)
- `'hubs'`: Show labels for top 10 hub nodes only
- `'none'`: No labels displayed

**Node Coloring Schemes:**
- `'cluster'`: Color nodes by cluster assignment
- `'custom'`: Use provided custom colors
- `'degree'`: Color by node connectivity degree
- `'betweenness'`: Color by betweenness centrality

**Cleanliness Presets:**
- `'light'`: threshold=0.4, selective labels (less filtered)
- `'medium'`: threshold=0.5, hub labels only (balanced)
- `'heavy'`: threshold=0.6, no labels (highly filtered)
- `'minimal'`: threshold=0.7, no labels, smaller figure (very clean)
- `'labeled'`: threshold=0.5, all labels, larger figure (detailed)

**Custom Node Colors:**
The `node_colors` parameter accepts:
- `dict`: `{region_name: color}` for specific regions
- `list`: Colors in same order as regions
- `None`: Use default coloring scheme

**Description:**
Creates a comprehensive network visualization of brain connectivity with extensive customization options. Automatically handles hemisphere labeling, provides network statistics, and includes a detailed legend.

## Usage Examples

### Basic Clustering Analysis

```python
import numpy as np
from clustering_module import create_main_clustering_visualization, analyze_clusters

# Load your connectivity matrix and region names
connectivity_matrix = np.load('connectivity_data.npy')
regions = ['region1', 'region2', ...]  # Your region names

# Create clustered visualization
cluster_labels, reordered_matrix, reordered_regions = create_main_clustering_visualization(
    connectivity_matrix, regions, n_clusters=8
)

# Analyze clusters
analyze_clusters(connectivity_matrix, regions, cluster_labels)
```

### Network Graph Creation

```python
from network_module import make_network_graph

# Create a clean network graph
G, pos = make_network_graph(
    connectivity_matrix, 
    regions, 
    cluster_labels,
    threshold=0.5,
    cleanliness='medium',
    show_labels='selective'
)
```

### Advanced Customization

```python
# Custom colors for specific regions
custom_colors = {
    'lh_prefrontal_cortex': 'red',
    'rh_prefrontal_cortex': 'red',
    'lh_visual_cortex': 'blue',
    'rh_visual_cortex': 'blue'
}

# Create network with custom styling
G, pos = make_network_graph(
    connectivity_matrix,
    regions,
    cluster_labels,
    threshold=0.6,
    layout_type='spring',
    show_labels='all',
    node_colors=custom_colors,
    color_by='custom',
    figsize=(16, 12),
    save_path='brain_network.png'
)
```

## Dependencies

### Required Packages
- `numpy`: Numerical computing
- `pandas`: Data manipulation
- `matplotlib`: Plotting and visualization
- `seaborn`: Statistical visualization
- `scipy`: Scientific computing (clustering, statistics)
- `scikit-learn`: Machine learning (clustering algorithms)
- `networkx`: Network analysis and visualization

### Optional Packages
- `PIL/Pillow`: Image processing (if saving high-resolution figures)

## Notes

### Performance Considerations
- For large correlation matrices (>200 regions), consider using `label_interval` > 1 to reduce label crowding
- Network graphs with many connections may benefit from higher threshold values for cleaner visualization
- Spring layout algorithms may take longer for large networks; consider using 'circular' for faster rendering

### Memory Usage
- Large correlation matrices require significant memory for hierarchical clustering
- Network graphs store all edge information; high thresholds reduce memory usage

### Visualization Tips
- Use `cleanliness` presets for quick, publication-ready figures
- Combine clustering and network analysis for comprehensive connectivity insights
- Save high-resolution figures using `dpi=300` for publications
