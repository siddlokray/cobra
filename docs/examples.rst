Examples
========

This page contains detailed examples of using CoBrA for different types of analysis.

Example 1: Basic Clustering
---------------------------

.. code-block:: python

   import cobra
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Generate sample brain connectivity data
   n_regions = 100
   np.random.seed(42)  # For reproducibility
   
   # Create a connectivity matrix with some structure
   connectivity_matrix = np.random.rand(n_regions, n_regions)
   connectivity_matrix = (connectivity_matrix + connectivity_matrix.T) / 2
   np.fill_diagonal(connectivity_matrix, 1.0)
   
   # Add some cluster structure
   for i in range(0, n_regions, 25):
       end_idx = min(i + 25, n_regions)
       connectivity_matrix[i:end_idx, i:end_idx] += 0.3
   
   # Create region names
   regions = [f'Region_{i:03d}' for i in range(n_regions)]
   
   # Perform clustering
   cluster_labels, reordered_matrix, reordered_regions = cobra.create_main_clustering_visualization(
       connectivity_matrix,
       regions,
       n_clusters=4,
       label_interval=10
   )
   
   plt.show()

Example 2: Network Analysis
--------------------------

.. code-block:: python

   import cobra
   import numpy as np
   import networkx as nx
   
   # Use the same connectivity matrix from Example 1
   # ... (connectivity_matrix and regions from above)
   
   # Create network graph
   G, pos = cobra.make_network_graph(
       connectivity_matrix,
       regions,
       cluster_labels,
       threshold=0.7,  # Higher threshold for cleaner network
       show_labels='hubs',
       figsize=(15, 12)
   )
   
   # Print network statistics
   print(f"Network Statistics:")
   print(f"  Nodes: {G.number_of_nodes()}")
   print(f"  Edges: {G.number_of_edges()}")
   print(f"  Density: {nx.density(G):.3f}")
   print(f"  Average clustering: {nx.average_clustering(G):.3f}")

Example 3: Custom Visualization
------------------------------

.. code-block:: python

   import cobra
   import numpy as np
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # Create custom color scheme
   n_regions = 80
   regions = [f'R{i:02d}' for i in range(n_regions)]
   
   # Generate connectivity data
   connectivity_matrix = np.random.rand(n_regions, n_regions)
   connectivity_matrix = (connectivity_matrix + connectivity_matrix.T) / 2
   np.fill_diagonal(connectivity_matrix, 1.0)
   
   # Custom colors for regions
   colors = plt.cm.Set3(np.linspace(0, 1, n_regions))
   
   # Perform clustering with custom parameters
   cluster_labels, reordered_matrix, reordered_regions = cobra.create_main_clustering_visualization(
       connectivity_matrix,
       regions,
       region_colors=colors,
       n_clusters=6,
       label_interval=8,
   )
   
   # Create network with custom styling
   G, pos = cobra.make_network_graph(
       reordered_matrix,
       reordered_regions,
       cluster_labels,
       threshold=0.6,
       node_colors=colors,
       color_by='custom',
       show_labels='all',
       figsize=(16, 14)
   )
   
   plt.tight_layout()
   plt.show()

Working with Real Data
---------------------

.. code-block:: python

   import cobra
   import pandas as pd
   import numpy as np
   
   # Example: Loading connectivity data from CSV
   # Assuming you have a CSV file with connectivity matrix
   
   def load_connectivity_data(filepath, region_names_file=None):
       """Load connectivity data from files."""
       
       # Load connectivity matrix
       connectivity_df = pd.read_csv(filepath, index_col=0)
       connectivity_matrix = connectivity_df.values
       
       # Load region names
       if region_names_file:
           regions_df = pd.read_csv(region_names_file)
           regions = regions_df['region_name'].tolist()
       else:
           regions = connectivity_df.index.tolist()
       
       return connectivity_matrix, regions
   
   # # Example usage:
   # connectivity_matrix, regions = load_connectivity_data(
   #     'connectivity_matrix.csv',
   #     'region_names.csv'
   # )
   # 
   # # Perform analysis
   # cluster_labels, reordered_matrix, reordered_regions = cobra.create_main_clustering_visualization(
   #     connectivity_matrix,
   #     regions,
   #     n_clusters='auto',  # Automatically determine number of clusters
   #     label_interval=1
   # )
