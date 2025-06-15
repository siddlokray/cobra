CoBRA: Connectivity Brain Regional Analysis
=========================================

CoBRA is a Python library for correlation-based region analysis, providing tools for clustering, visualization, and network analysis of connectivity data.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   examples

Features
--------

* **Clustering**: Advanced clustering algorithms for correlation matrices
* **Visualization**: Beautiful plotting functions for data exploration
* **Network Analysis**: Graph-based analysis of connectivity patterns
* **Easy to Use**: Simple API with sensible defaults

Quick Example
-------------

.. code-block:: python

   import cobra
   import numpy as np

   # Create sample connectivity matrix
   connectivity_matrix = np.random.rand(50, 50)
   regions = [f'Region_{i}' for i in range(50)]
   
   # Perform clustering analysis
   cluster_labels, reordered_matrix, reordered_regions = cobra.create_main_clustering_visualization(
       connectivity_matrix, regions, n_clusters=4
   )

Installation
------------

Install CoBRA using pip:

.. code-block:: bash

   pip install cobra-brain

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
