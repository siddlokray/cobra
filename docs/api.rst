API Reference
=============

This package provides tools for clustering and visualizing brain connectivity data.

cluster module
--------------

Data Preparation
~~~~~~~~~~~~~~~~

.. autofunction:: cluster.prepare_clustering_data

   Prepare connectivity data for hierarchical clustering analysis.

   :param connectivity_matrix: Correlation matrix between brain regions
   :type connectivity_matrix: numpy.ndarray
   :param regions: List of region names
   :type regions: list
   :returns: Distance matrix, condensed distances, and linkage matrix
   :rtype: tuple

Matrix Visualization
~~~~~~~~~~~~~~~~~~~

.. autofunction:: cluster.plot_original_correlation_matrix

   Plot the original correlation matrix as a heatmap with customizable labeling.

   :param connectivity_matrix: Correlation matrix
   :type connectivity_matrix: numpy.ndarray
   :param regions: List of region names
   :type regions: list
   :param figsize: Figure size (width, height)
   :type figsize: tuple, optional
   :param region_colors: List of colors for region labels
   :type region_colors: list, optional
   :param show_labels: Whether to show tick labels
   :type show_labels: bool, optional
   :param label_interval: Show every nth label to reduce crowding
   :type label_interval: int, optional
   :returns: Figure and axes objects
   :rtype: tuple

.. autofunction:: cluster.create_clustered_correlation_matrix

   Create and display clustered correlation matrix with cluster boundaries.

   :param connectivity_matrix: Correlation matrix
   :type connectivity_matrix: numpy.ndarray
   :param regions: List of region names
   :type regions: list
   :param n_clusters: Number of clusters (auto-determined if None)
   :type n_clusters: int, optional
   :param figsize: Figure size (width, height)
   :type figsize: tuple, optional
   :param region_colors: List of colors for region labels
   :type region_colors: list, optional
   :param show_labels: Whether to show tick labels
   :type show_labels: bool, optional
   :param label_interval: Show every nth label to reduce crowding
   :type label_interval: int, optional
   :returns: Figure, axes, cluster labels, reordered matrix, and reordered regions
   :rtype: tuple

Cluster Analysis
~~~~~~~~~~~~~~~

.. autofunction:: cluster.plot_cluster_summary

   Create a text-based cluster summary visualization.

   :param regions: List of region names
   :type regions: list
   :param cluster_labels: Cluster assignments for each region
   :type cluster_labels: numpy.ndarray
   :param figsize: Figure size (width, height)
   :type figsize: tuple, optional
   :returns: Figure and axes objects
   :rtype: tuple

.. autofunction:: cluster.analyze_clusters

   Provide detailed cluster analysis with statistics.

   :param connectivity_matrix: Correlation matrix
   :type connectivity_matrix: numpy.ndarray
   :param regions: List of region names
   :type regions: list
   :param cluster_labels: Cluster assignments for each region
   :type cluster_labels: numpy.ndarray

Main Functions
~~~~~~~~~~~~~

.. autofunction:: cluster.create_main_clustering_visualization

   Main function that creates the clustered correlation matrix visualization.

   :param connectivity_matrix: Correlation matrix
   :type connectivity_matrix: numpy.ndarray
   :param regions: List of region names
   :type regions: list
   :param n_clusters: Number of clusters
   :type n_clusters: int, optional
   :param region_colors: List of colors for region labels
   :type region_colors: list, optional
   :param show_labels: Whether to show region labels
   :type show_labels: bool, optional
   :param label_interval: Show every nth label (default 5 for 150 regions)
   :type label_interval: int, optional
   :returns: Cluster labels, reordered matrix, and reordered regions
   :rtype: tuple

Utilities
~~~~~~~~~

.. autofunction:: cluster.generate_example_colors

   Generate example color schemes for regions.

   :param regions: List of region names
   :type regions: list
   :param color_scheme: Color scheme type ('network', 'random', 'gradient', 'categorical')
   :type color_scheme: str, optional
   :returns: List of colors for each region
   :rtype: list

visualize module
----------------

Network Graphs
~~~~~~~~~~~~~~

.. autofunction:: visualize.make_network_graph

   Create a clean, publication-ready network graph with flexible customization options.

   :param connectivity_matrix: Correlation matrix between brain regions
   :type connectivity_matrix: numpy.ndarray
   :param regions: List of region names
   :type regions: list
   :param cluster_labels: Cluster assignments for each region
   :type cluster_labels: numpy.ndarray
   :param threshold: Minimum correlation strength to show (higher = less crowded)
   :type threshold: float, optional
   :param figsize: Figure size (width, height)
   :type figsize: tuple, optional
   :param save_path: Path to save the figure
   :type save_path: str, optional
   :param layout_type: Layout algorithm ('spring', 'circular', 'force_atlas', 'kamada_kawai')
   :type layout_type: str, optional
   :param show_labels: Label display ('all', 'selective', 'hubs', 'none')
   :type show_labels: str, optional
   :param node_colors: Custom colors for nodes
   :type node_colors: dict, list, or None, optional
   :param color_by: Node coloring scheme ('cluster', 'custom', 'degree', 'betweenness')
   :type color_by: str, optional
   :param cleanliness: Preset configurations ('light', 'medium', 'heavy', 'minimal', 'labeled')
   :type cleanliness: str, optional
   :param orientation: Graph orientation ('horizontal', 'vertical')
   :type orientation: str, optional
   :returns: NetworkX graph object and node positions
   :rtype: tuple

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from your_package import cluster, visualize

   # Load your connectivity data
   connectivity_matrix = np.random.rand(100, 100)  # Your correlation matrix
   regions = [f"region_{i}" for i in range(100)]   # Your region names

   # Create clustered visualization
   cluster_labels, reordered_matrix, reordered_regions = cluster.create_main_clustering_visualization(
       connectivity_matrix, regions, n_clusters=5
   )

   # Analyze clusters
   cluster.analyze_clusters(connectivity_matrix, regions, cluster_labels)

   # Create network graph
   G, pos = visualize.make_network_graph(
       connectivity_matrix, regions, cluster_labels,
       threshold=0.5, layout_type='spring', show_labels='selective'
   )

Advanced Customization
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Generate custom colors
   region_colors = cluster.generate_example_colors(regions, color_scheme='network')

   # Create detailed clustered matrix with custom colors
   fig, ax, cluster_labels, reordered_matrix, reordered_regions = cluster.create_clustered_correlation_matrix(
       connectivity_matrix, regions, n_clusters=8,
       region_colors=region_colors, show_labels=True, label_interval=3
   )

   # Create clean network graph with custom settings
   G, pos = visualize.make_network_graph(
       connectivity_matrix, regions, cluster_labels,
       threshold=0.6, figsize=(16, 12), layout_type='spring',
       show_labels='hubs', color_by='degree', cleanliness='medium',
       save_path='brain_network.png'
   )

   # Plot cluster summary
   cluster.plot_cluster_summary(regions, cluster_labels, figsize=(12, 14))

Dependencies
-----------

Required packages:

- numpy
- matplotlib
- scipy
- networkx
- sklearn (for clustering utilities)

Notes
-----

- Correlation matrices should be symmetric with values between -1 and 1
- Region names should be unique strings
- The package handles both single and bilateral (lh_/rh_) hemisphere naming conventions
- Network graphs automatically filter edges based on correlation strength thresholds
- Clustering uses hierarchical clustering with Ward linkage by default