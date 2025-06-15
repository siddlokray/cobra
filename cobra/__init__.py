"""
CoBrA: Cortical Brain Region Analysis

A comprehensive Python library for analyzing cortical brain connectivity 
through correlation matrices, hierarchical clustering, and network visualization.
"""

__version__ = "0.1.0"
__author__ = "Sidd Lokray"
__email__ = "siddharthlokray@gmail.com"
__description__ = "Cortical Brain Region Analysis toolkit"

# Import main modules
from . import clustering
from . import visualization
from . import network

# Import key functions for direct access
from .clustering import (
    prepare_clustering_data,
    create_clustered_correlation_matrix,
    create_main_clustering_visualization,
    plot_cluster_summary,
    analyze_clusters,
    generate_example_colors
)

from .visualization import (
    plot_original_correlation_matrix
)

from .network import (
    make_network_graph
)

# Define what's available when using "from cobra import *"
__all__ = [
    # Modules
    'clustering',
    'visualization', 
    'network',
    
    # Key functions
    'prepare_clustering_data',
    'create_clustered_correlation_matrix',
    'create_main_clustering_visualization',
    'plot_cluster_summary',
    'analyze_clusters',
    'generate_example_colors',
    'plot_original_correlation_matrix',
    'make_network_graph'
]

# Package metadata
__package_info__ = {
    'name': 'cobra',
    'version': __version__,
    'description': __description__,
    'author': __author__,
    'author_email': __email__,
    'url': 'https://github.com/slokray/cobra',
    'license': 'MIT',
    'python_requires': '>=3.7',
}