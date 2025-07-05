import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

def make_network_graph(connectivity_matrix, regions, cluster_labels,
                      threshold=0.5, n_interations=100, figsize=(14, 10), save_path=None,
                      layout_type='spring', show_labels='selective',
                      node_colors=None, color_by='cluster', cleanliness=None,
                      orientation='horizontal'):
    """
    Create a clean, publication-ready network graph with flexible customization options.

    Parameters:
    -----------
    connectivity_matrix : array
        Correlation matrix between brain regions
    regions : list
        List of region names
    cluster_labels : array
        Cluster assignments for each region
    threshold : float, default=0.5
        Minimum correlation strength to show (higher = less crowded)
    n_interations : int, default=100
        Interations to minimize net "force"
    figsize : tuple, default=(14, 10)
        Figure size (width, height)
    save_path : str, optional
        Path to save the figure
    layout_type : str, default='spring'
        Layout algorithm: 'spring', 'circular', 'force_atlas', or 'kamada_kawai'
    show_labels : str, default='selective'
        Label display: 'all', 'selective', 'hubs', or 'none'
    node_colors : dict, list, or None
        Custom colors for nodes. Can be:
        - dict: {region_name: color} for specific regions
        - list: colors in same order as regions
        - None: use default coloring scheme
    color_by : str, default='cluster'
        Node coloring scheme: 'cluster', 'custom', 'degree', or 'betweenness'
    cleanliness : str, optional
        Preset configurations that override other parameters:
        - 'light': threshold=0.4, selective labels
        - 'medium': threshold=0.5, hub labels only
        - 'heavy': threshold=0.6, no labels
        - 'minimal': threshold=0.7, no labels, smaller figure
        - 'labeled': threshold=0.5, all labels, larger figure
    orientation : str, default='horizontal'
        Graph orientation: 'horizontal' or 'vertical'

    Returns:
    --------
    G : networkx.Graph
        The created network graph
    pos : dict
        Node positions for the layout
    """

    # Apply cleanliness presets if specified
    if cleanliness:
        if cleanliness == 'light':
            threshold, show_labels = 0.4, 'selective'
        elif cleanliness == 'medium':
            threshold, show_labels = 0.5, 'hubs'
        elif cleanliness == 'heavy':
            threshold, show_labels = 0.6, 'none'
        elif cleanliness == 'minimal':
            threshold, show_labels, figsize = 0.7, 'none', (10, 8)
        elif cleanliness == 'labeled':
            threshold, show_labels, figsize = 0.5, 'all', (16, 12)

    # Adjust figsize based on orientation
    if orientation == 'vertical':
        figsize = (figsize[1], figsize[0])  # Swap width and height

    # Create network graph
    G = nx.Graph()

    # Add nodes with cluster information
    for i, region in enumerate(regions):
        G.add_node(region, cluster=cluster_labels[i])

    # Add edges above threshold
    n = len(regions)
    edge_count = 0
    for i in range(n):
        for j in range(i+1, n):
            corr_val = connectivity_matrix[i, j]
            if abs(corr_val) > threshold:
                G.add_edge(regions[i], regions[j],
                          weight=abs(corr_val),
                          correlation=corr_val)
                edge_count += 1

    print(f"Network created with {G.number_of_nodes()} nodes and {edge_count} edges")
    print(f"Threshold: {threshold} (showing {edge_count}/{n*(n-1)//2} possible connections)")

    # Set up the plot
    fig, ax = plt.subplots(figsize=figsize, dpi=300, facecolor='white')

    # Choose layout - use original parameters for consistency
    if layout_type == 'spring':
        pos = nx.spring_layout(G, k=2, iterations=n_interations, seed=42)
    elif layout_type == 'circular':
        pos = nx.circular_layout(G)
    elif layout_type == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    elif layout_type == 'force_atlas':
        pos = nx.spring_layout(G, k=3, iterations=n_interations, seed=42, weight='weight')
    else:  # default to spring with original parameters
        pos = nx.spring_layout(G, k=2, iterations=n_interations, seed=42)

    # Apply orientation transformation
    if orientation == 'vertical':
        # Rotate positions by 90 degrees for vertical orientation
        pos = {node: (-y, x) for node, (x, y) in pos.items()}

    # Determine node colors
    final_node_colors = []

    if color_by == 'custom' and node_colors is not None:
        # Use custom colors
        if isinstance(node_colors, dict):
            # Dictionary mapping region names to colors
            n_clusters = len(np.unique(cluster_labels))
            cluster_colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))

            for node in G.nodes():
                if node in node_colors:
                    final_node_colors.append(node_colors[node])
                else:
                    # Fallback to cluster color if custom color not specified
                    cluster_id = cluster_labels[regions.index(node)]
                    final_node_colors.append(cluster_colors[cluster_id-1])

        elif isinstance(node_colors, (list, np.ndarray)):
            # List of colors in same order as regions
            if len(node_colors) == len(regions):
                final_node_colors = [node_colors[regions.index(node)] for node in G.nodes()]
            else:
                print("Warning: node_colors list length doesn't match regions. Using cluster colors.")
                color_by = 'cluster'
        else:
            print("Warning: Invalid node_colors format. Using cluster colors.")
            color_by = 'cluster'

    if color_by == 'cluster' or (color_by == 'custom' and node_colors is None):
        # Default cluster-based coloring
        n_clusters = len(np.unique(cluster_labels))
        cluster_colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))

        for node in G.nodes():
            cluster_id = cluster_labels[regions.index(node)]
            final_node_colors.append(cluster_colors[cluster_id-1])

    elif color_by == 'degree':
        # Color by node degree (connectivity)
        degrees = dict(G.degree())
        max_degree = max(degrees.values()) if degrees.values() else 1
        colormap = plt.cm.viridis

        for node in G.nodes():
            degree_norm = degrees[node] / max_degree
            final_node_colors.append(colormap(degree_norm))

    elif color_by == 'betweenness':
        # Color by betweenness centrality
        betweenness = nx.betweenness_centrality(G)
        max_betweenness = max(betweenness.values()) if betweenness.values() else 1
        colormap = plt.cm.plasma

        for node in G.nodes():
            bet_norm = betweenness[node] / max_betweenness if max_betweenness > 0 else 0
            final_node_colors.append(colormap(bet_norm))

    # Node sizes based on degree
    node_sizes = []
    for node in G.nodes():
        degree = G.degree(node)
        node_sizes.append(200 + degree * 20)  # Base size + degree scaling

    # Edge properties
    edges = G.edges()
    edge_colors = []
    edge_widths = []

    for u, v in edges:
        corr = G[u][v]['correlation']
        weight = G[u][v]['weight']

        # Color based on correlation sign
        if corr > 0:
            edge_colors.append('#2C3E50')  # Dark blue for positive
        else:
            edge_colors.append('#E74C3C')  # Red for negative

        # Width based on strength (but keep reasonable)
        edge_widths.append(max(0.5, min(3.0, weight * 4)))

    # Draw edges first (so they appear behind nodes)
    nx.draw_networkx_edges(G, pos,
                          width=edge_widths,
                          edge_color=edge_colors,
                          alpha=0.6,
                          ax=ax)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos,
                          node_color=final_node_colors,
                          node_size=node_sizes,
                          alpha=0.8,
                          edgecolors='white',
                          linewidths=1,
                          ax=ax)

    # Check if we have both hemispheres to determine label format
    has_lh = any(region.startswith('lh_') for region in regions)
    has_rh = any(region.startswith('rh_') for region in regions)
    show_hemisphere = has_lh and has_rh  # Only show hemisphere if both are present

    # Handle labels based on show_labels parameter
    if show_labels == 'all':
        # Show all labels with smart abbreviation
        labels_to_show = {}
        for node in G.nodes():
            # Create short, readable labels
            if show_hemisphere:
                # Keep hemisphere prefix if both lh and rh are present
                if node.startswith('lh_'):
                    clean_name = 'L-' + node[3:].replace('_', ' ')
                elif node.startswith('rh_'):
                    clean_name = 'R-' + node[3:].replace('_', ' ')
                else:
                    clean_name = node.replace('_', ' ')
            else:
                # Remove hemisphere prefix if only one hemisphere
                clean_name = node.replace('lh_', '').replace('rh_', '')
                clean_name = clean_name.replace('_', ' ')

            # Intelligent abbreviation
            if len(clean_name) <= 12:
                labels_to_show[node] = clean_name
            else:
                # Keep important words, abbreviate others
                words = clean_name.split()
                if len(words) == 1:
                    labels_to_show[node] = clean_name[:10] + '..'
                else:
                    # Keep first and last word, abbreviate middle
                    if len(words) == 2:
                        labels_to_show[node] = f"{words[0][:6]} {words[1][:6]}"
                    else:
                        labels_to_show[node] = f"{words[0][:5]} {words[-1][:5]}"

        # Draw labels with better positioning
        nx.draw_networkx_labels(G, pos, labels_to_show,
                               font_size=7, font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.15",
                                       facecolor="white", alpha=0.9,
                                       edgecolor='gray', linewidth=0.5),
                               ax=ax)

    elif show_labels == 'selective':
        # Show labels for high-degree nodes
        degrees = dict(G.degree())
        degree_threshold = np.percentile(list(degrees.values()), 80)

        labels_to_show = {}
        for node in G.nodes():
            if degrees[node] >= degree_threshold:
                # Clean up label names with hemisphere handling
                if show_hemisphere:
                    if node.startswith('lh_'):
                        clean_name = 'L-' + node[3:].replace('_', ' ')
                    elif node.startswith('rh_'):
                        clean_name = 'R-' + node[3:].replace('_', ' ')
                    else:
                        clean_name = node.replace('_', ' ')
                else:
                    clean_name = node.replace('lh_', '').replace('rh_', '').replace('_', ' ')

                if len(clean_name) > 15:
                    clean_name = clean_name[:12] + '...'
                labels_to_show[node] = clean_name

        nx.draw_networkx_labels(G, pos, labels_to_show,
                               font_size=8, font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2",
                                       facecolor="white", alpha=0.8),
                               ax=ax)

    elif show_labels == 'hubs':
        # Show only the top hub nodes
        degrees = dict(G.degree())
        top_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]

        labels_to_show = {}
        for node, degree in top_hubs:
            if show_hemisphere:
                if node.startswith('lh_'):
                    clean_name = 'L-' + node[3:].replace('_', ' ')
                elif node.startswith('rh_'):
                    clean_name = 'R-' + node[3:].replace('_', ' ')
                else:
                    clean_name = node.replace('_', ' ')
            else:
                clean_name = node.replace('lh_', '').replace('rh_', '').replace('_', ' ')

            if len(clean_name) > 15:
                clean_name = clean_name[:12] + '...'
            labels_to_show[node] = clean_name

        nx.draw_networkx_labels(G, pos, labels_to_show,
                               font_size=9, font_weight='bold',
                               bbox=dict(boxstyle="round,pad=0.3",
                                       facecolor="yellow", alpha=0.7),
                               ax=ax)

    # Create comprehensive legend
    legend_elements = []

    # Add legend based on coloring scheme
    if color_by == 'cluster':
        n_clusters = len(np.unique(cluster_labels))
        cluster_colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
        for i in range(n_clusters):
            legend_elements.append(Patch(facecolor=cluster_colors[i],
                                       label=f'Cluster {i+1}'))
    elif color_by == 'custom':
        legend_elements.append(Patch(facecolor='gray', label='Custom colors'))
    elif color_by == 'degree':
        legend_elements.append(Patch(facecolor=plt.cm.viridis(0.2), label='Low connectivity'))
        legend_elements.append(Patch(facecolor=plt.cm.viridis(0.8), label='High connectivity'))
    elif color_by == 'betweenness':
        legend_elements.append(Patch(facecolor=plt.cm.plasma(0.2), label='Low centrality'))
        legend_elements.append(Patch(facecolor=plt.cm.plasma(0.8), label='High centrality'))

    # Separator
    legend_elements.append(Patch(facecolor='none', edgecolor='none', label=''))

    # Correlation types
    legend_elements.append(Patch(facecolor='#2C3E50', label='Positive correlation'))
    legend_elements.append(Patch(facecolor='#E74C3C', label='Negative correlation'))

    # Node size explanation
    legend_elements.append(Patch(facecolor='none', edgecolor='none', label=''))
    legend_elements.append(Patch(facecolor='gray', alpha=0.5,
                                label='Node size ∝ connectivity'))

    # Position legend outside the plot
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5),
             frameon=True, fancybox=True, shadow=True)

    # Set title and clean up axes
    title = f'Brain Region Connectivity Network\n|τ| > {threshold} • {edge_count} connections'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')

    # Add network statistics as text
    if G.number_of_edges() > 0:
        avg_clustering = nx.average_clustering(G)
    else:
        avg_clustering = 0.0

    stats_text = f"""Network Statistics:
Nodes: {G.number_of_nodes()}
Edges: {G.number_of_edges()}
Density: {nx.density(G):.3f}
Avg. Clustering: {avg_clustering:.3f}"""

    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle="round,pad=0.4", facecolor="lightgray", alpha=0.8))

    plt.tight_layout()

    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        print(f"Network graph saved as: {save_path}")

    plt.show()

    return G, pos
