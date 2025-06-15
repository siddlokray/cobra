Quick Start
===========

This guide will help you get started with CoBRA quickly.

Basic Usage
-----------

Import CoBrA and create some sample data:

.. code-block:: python

   import cobra
   import numpy as np
   
   # Create sample connectivity matrix
   n_regions = 50
   connectivity_matrix = np.random.rand(n_regions, n_regions)
   # Make it symmetric
   connectivity_matrix = (connectivity_matrix + connectivity_matrix.T) / 2
   np.fill_diagonal(connectivity_matrix, 1.0)
   
   # Create region names
   regions = [f'Region_{i:02d}' for i in range(n_regions)]

Clustering Analysis
------------------

Perform clustering analysis on your connectivity data:

.. code-block:: python

   # Perform clustering with visualization
   cluster_labels, reordered_matrix, reordered_regions = cobra.create_main_clustering_visualization(
       connectivity_matrix, 
       regions, 
       n_clusters=4,
       label_interval=5
   )
   
   print(f"Found {len(set(cluster_labels))} clusters")
   print(f"Cluster labels: {cluster_labels[:10]}...")  # First 10 labels

Network Analysis
---------------

Create and analyze network graphs:

.. code-block:: python

   # Create network graph
   G, pos = cobra.make_network_graph(
       connectivity_matrix, 
       regions, 
       cluster_labels,
       threshold=0.5,
       show_labels='hubs'
   )
   
   print(f"Network has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

Data Preparation
---------------

Prepare your data for clustering:

.. code-block:: python

   # Prepare clustering data
   distance_matrix, linkage_matrix = cobra.prepare_clustering_data(
       connectivity_matrix, 
       regions
   )
   
   print(f"Distance matrix shape: {distance_matrix.shape}")
   print(f"Linkage matrix shape: {linkage_matrix.shape}")

Next Steps
----------

* Check out the :doc:`api` for detailed function documentation
* See :doc:`examples` for more complex use cases
* Visit the `GitHub repository <https://github.com/siddlokray/cobra>`_ for source code
