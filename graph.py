import snap
import pandas as pd
import matplotlib.pyplot as plt


class RandomGraph:
    """
    A class for creating and analyzing random undirected or directed graphs using the Snap.py library.

    Parameters:
    - n_nodes (int): The number of nodes in the graph.
    - n_edges (int): The number of edges in the graph.
    - is_directed (bool): True for directed graphs, False for undirected graphs.

    Example Usage:
    ```python
    # Create an undirected graph with 10 nodes and 20 edges
    graph = PlainGraph(n_nodes=10, n_edges=20, is_directed=False)
    ```

    Attributes:
    - n_nodes (int): The number of nodes in the graph.
    - n_edges (int): The number of edges in the graph.
    - is_directed (bool): True for directed graphs, False for undirected graphs.
    - graph (Snap.py graph object): The Snap.py graph representing the random graph.
    - n_degree (dict): A dictionary to store the degree distribution of nodes.
    """

    def __init__(self, n_nodes=0, n_edges=0, is_directed=False, verbose = False):
        """
        Initialize a PlainGraph object with the specified number of nodes and edges.

        Parameters:
        - n_nodes (int): The number of nodes in the graph.
        - n_edges (int): The number of edges in the graph.
        - is_directed (bool): True for directed graphs, False for undirected graphs.
        """
        self.n_nodes = n_nodes
        if n_edges > (n_nodes * (n_nodes - 1)) / 2 and is_directed==False:
            raise ValueError("Number of edges cannot be more than {} for a {} node undirected graph".format((n_nodes * (n_nodes - 1)) / 2, self.n_nodes))
        if n_edges > (n_nodes * (n_nodes - 1)) and is_directed==True:
            raise ValueError("Number of edges cannot be more than {} for a {} node undirected graph".format((n_nodes * (n_nodes - 1)), self.n_nodes))
        self.n_edges = n_edges
        self.is_directed = is_directed
        self.verbose = verbose

        if self.is_directed:
            self.graph = snap.GenRndGnm(snap.TNGraph, self.n_nodes, self.n_edges)
        else:
            self.graph = snap.GenRndGnm(snap.TUNGraph, self.n_nodes, self.n_edges)
        
        self.n_degree = {}

    def __repr__(self):
        """
        Return a string representation of the PlainGraph object.
        """
        graph_type = "Directed" if self.is_directed else "Undirected"
        return f"Random Snap Graph ({graph_type}): Nodes={self.n_nodes}, Edges={self.n_edges}"

    def set_nodes(self):
        """
        Set the list of nodes in the graph.
        """
        self.nodes = [node.GetId() for node in self.graph.Nodes()]

    @property
    def get_nodes(self) -> list:
        """
        Get the list of nodes in the graph.

        Returns:
        - list: A list of node IDs.
        """
        if not hasattr(self, 'nodes'):
            self.set_nodes()
        return self.nodes

    def set_edges(self):
        """
        Set the list of edges in the graph.
        """
        self.edges = [(edge.GetSrcNId(), edge.GetDstNId()) for edge in self.graph.Edges()]

    @property
    def get_edges(self)-> list:
        """
        Get the list of edges in the graph.

        Returns:
        - list: A list of edge tuples (source node, target node).
        """
        if not hasattr(self, 'edges'):
            self.set_edges()
        if self.verbose:
            for EI in self.graph.Edges():
                print("edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId()))
        return self.edges
    
    def create_adjacency_list(self):
        """
        Create an adjacency list from the edges data.

        Returns:
        - list of lists: An adjacency list where each index indicates a vertex, and the item is a list of adjacent vertices.
        """
        adjacency_list: list = [[] for _ in range(self.n_nodes)]

        for edge in self.get_edges:
            source, target = edge
            adjacency_list[source].append(target)
            if not self.is_directed:
                adjacency_list[target].append(source)  # For undirected graphs, add both directions

        return adjacency_list

    @property
    def get_adjacency_list(self):
        """
        Get the adjacency list for the graph.

        Returns:
        - list of lists: An adjacency list where each index indicates a vertex, and the item is a list of adjacent vertices.
        """
        adjacency_list = self.create_adjacency_list()
        if self.verbose:
            print("Adjacency list for {} graph: {}".format(self.graph, adjacency_list))
        return adjacency_list

    def get_degree_distribution(self):
        """
        Get the degree distribution of nodes in the graph.

        Returns:
        - dict: A dictionary with node IDs as keys and their degrees as values.
        """
        for node in self.graph.Nodes():
            self.n_degree[node.GetId()] = node.GetDeg()
        return self.n_degree

    def get_average_degree(self):
        """
        Get the average degree of nodes in the graph.

        Returns:
        - float: The average degree.
        """
        if self.graph.GetNodes() == 0:
            return 0
        return 2 * self.graph.GetEdges() / self.graph.GetNodes()

    def get_clustering_coefficient(self):
        """
        Get the clustering coefficient of the graph.

        Returns:
        - float: The clustering coefficient.
        """
        return snap.GetClustCf(self.graph)

    def get_number_of_connected_components(self):
        """
        Get the number of connected components in the graph.

        Returns:
        - int: The number of connected components.
        """
        return snap.GetWccs(self.graph)
    
    def plot_graph(self, filename = 'graph_edges.txt', graph_title = 'List of edges'):
        return snap.DrawGViz(self.graph, snap.gvlDot, filename, graph_title)

    def save_graph_txt(self, filename = 'graph_edges.txt', title = 'List of edges'):
        return snap.SaveEdgeList(self.graph, filename, title)




if __name__ == "__main__" :

    random_graph = RandomGraph(n_nodes=20, n_edges=100, verbose=True)
    print(random_graph.get_nodes)
    # random_graph.plot_graph()
    # random_graph.save_graph_txt()

    