# CoBRA: Connectivity Brain Regional Analysis

A comprehensive Python library for analyzing cortical brain region connectivity using correlation matrices, hierarchical clustering, and network visualization.

## Features

- **Connectivity Matrix Analysis**: Process and analyze correlation matrices between brain regions
- **Hierarchical Clustering**: Identify clusters of functionally related brain regions
- **Network Visualization**: Create publication-ready network graphs with flexible customization
- **Statistical Analysis**: Comprehensive cluster statistics and connectivity metrics

## Installation

```bash
pip install cobra-brain
```

## Quick Start

```python
import numpy as np
from cobra import clustering, visualization, network

# Load your connectivity matrix and region names
connectivity_matrix = np.load('your_connectivity_matrix.npy')
regions = ['region1', 'region2', ...]  # List of region names

# Perform clustering analysis
cluster_labels, reordered_matrix, reordered_regions = clustering.create_main_clustering_visualization(
    connectivity_matrix, regions, n_clusters=8
)

# Create network visualization
G, pos = network.make_network_graph(
    connectivity_matrix, regions, cluster_labels,
    threshold=0.5, layout_type='spring'
)

# Generate cluster summary
clustering.plot_cluster_summary(regions, cluster_labels)
```

## Core Components

### Clustering (`cobra.clustering`)
- `prepare_clustering_data()`: Prepare correlation matrices for hierarchical clustering
- `create_clustered_correlation_matrix()`: Generate clustered heatmaps
- `analyze_clusters()`: Statistical analysis of identified clusters
- `plot_cluster_summary()`: Visual cluster assignments

### Network Analysis (`cobra.network`)
- `make_network_graph()`: Create network graphs with customizable layouts
- Multiple layout algorithms: spring, circular, force-atlas, kamada-kawai
- Flexible node coloring: by cluster, degree, betweenness centrality
- Adjustable edge filtering and styling

## Advanced Usage

### Custom Clustering
```python
# Custom number of clusters with color coding
region_colors = clustering.generate_example_colors(regions, 'network')
cluster_labels = clustering.create_main_clustering_visualization(
    connectivity_matrix, regions, 
    n_clusters=6, 
    region_colors=region_colors,
    label_interval=10
)
```

### Network Graph Customization
```python
# Create a clean, minimal network
G, pos = network.make_network_graph(
    connectivity_matrix, regions, cluster_labels,
    threshold=0.6,
    cleanliness='minimal',
    color_by='degree',
    layout_type='spring'
)

# Publication-ready labeled version
G, pos = network.make_network_graph(
    connectivity_matrix, regions, cluster_labels,
    cleanliness='labeled',
    save_path='brain_network.png'
)
```

### Statistical Analysis
```python
# Detailed cluster analysis
clustering.analyze_clusters(connectivity_matrix, regions, cluster_labels)

# Original vs clustered matrix comparison
visualization.plot_original_correlation_matrix(
    connectivity_matrix, regions, 
    region_colors=region_colors
)
```

## Requirements

- Python >= 3.7
- NumPy >= 1.19.0
- SciPy >= 1.5.0
- Matplotlib >= 3.3.0
- NetworkX >= 2.5
- scikit-learn >= 0.23.0

## Data Format

CoBRA expects:
- **Connectivity Matrix**: Square correlation matrix (n_regions × n_regions)
- **Region Names**: List of strings identifying each brain region
- **Values**: Correlation coefficients typically range from -1 to 1

## Examples

The `examples/` directory contains:
- `basic_usage.py`: Simple workflow demonstration
- `sample_data.py`: Generate synthetic brain connectivity data for testing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use CoBRA in your research, please cite:

```bibtex
@software{cobra,
  title={CoBRA: Cortical Brain Region Analysis},
  author={Sidd Lokray},
  year={2025},
  url={https://github.com/siddlokray/cobra}
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions and issues, please open an issue on GitHub or contact [siddharthlokray@dgmail.com].
