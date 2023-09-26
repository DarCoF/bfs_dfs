import os
import sys
sys.setrecursionlimit(6500)
from typing import Callable, Iterable, Sequence
import warnings
import random
from manim.mobject.graphing.scale import _ScaleBase, LinearBase


current_script_path = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.abspath(os.path.join(current_script_path, ".."))  # Go up one level
sys.path.append(root_directory)

from manim import *
from manim.camera.camera import Camera
from manim.constants import ORIGIN, PI, TAU
from graph import RandomGraph
import numpy as np
from render_graph import Node, Edge

# Run multiples tests with different numbers of edges and nodes. Each experiment must be timestamped at the beginning
# and at execution end. Measured times will be plotted in a graph for comparison.
import time
import unittest

class Graph3D(ThreeDScene):

    def __init__(self,
        camera_class=ThreeDCamera,
        ambient_camera_rotation=None,
        default_angled_camera_orientation_kwargs=None,
        n_nodes: int = 20, 
        n_edges: int = 100, 
        is_bfs_search: bool = True,
        is_directed: bool = False,
        **kwargs):
        
        super().__init__(
        camera_class=camera_class,
        ambient_camera_rotation=ambient_camera_rotation,
        default_angled_camera_orientation_kwargs=default_angled_camera_orientation_kwargs)

        self._n_nodes = n_nodes
        self._n_edges = n_edges
        self.random_graph = RandomGraph(self._n_nodes, self._n_edges, is_directed=is_directed)
        self.is_bfs_search = is_bfs_search

        if len(self.random_graph.get_nodes) > 0:
            self.parent : list = [-1 for _ in range (len(self.random_graph.get_nodes))]
            self.node_status: list[str] = ['U' for _ in range(len(self.random_graph.get_nodes))]
            self.edge_status: list[str] = ['U' for _ in range(len(self.random_graph.get_edges))]
            self.node_coordinates: list[list] = self._generate_sparse_coordinates(len(self.random_graph.get_nodes))

        else:
            raise ValueError('Number of nodes in graph must be at least 1. Please provide a different value for n_nodes')        
        self.queue = []
        self.nodes_3d: list[VMobject] = []
        self.edges_3d: list[VMobject] = []
        
        self.redraw = None

    def _generate_sparse_coordinates(self, n_nodes = 0, cube_size = 2.5):
        # Implement your algorithm to generate sparse 3D coordinates here
        # For example, you can use random coordinates within a specific range
        # while ensuring that they are not too close to each other.

        # Dummy example: Generate random coordinates within a cube
        coordinates = []
        for _ in range(n_nodes):
            x = np.random.uniform(-cube_size, cube_size)
            y = np.random.uniform(-cube_size, cube_size)
            z = np.random.uniform(-cube_size, cube_size)
            coordinates.append([x, y, z])
        return coordinates
    
    def draw_initial_map(self):
        # Create as many nodes objects as nodes are in random_graph
        for idx in range(len(self.random_graph.get_nodes)):
            node = Node(label=str(idx))
            node.set_x(0)
            node.set_y(0)
            node.set_z(0)
            self.nodes_3d.append(node)

        for EI in self.random_graph.get_edges:
            source, target = EI
            handle = np.array([1, 0, 0])
            edge = Edge(start_anchor= np.array(self.node_coordinates[source]), start_handle= np.array(self.node_coordinates[source]) + handle, end_anchor= np.array(self.node_coordinates[target]), end_handle= np.array(self.node_coordinates[target]) + handle)
            # Modify connecting points: start and end
            self.edges_3d.append(edge)

        # Animate the node spheres. At the beginning of the anim they appear in the origin and each move concurrently to their respective positions.
        animations = [self.nodes_3d[node].animate.move_to(self.node_coordinates[node]) for node in self.random_graph.get_nodes]

        node_animation = AnimationGroup(*animations)
        self.move_camera(phi=60 * DEGREES)
        self.move_camera(theta=45 * DEGREES)
        # self.begin_ambient_camera_rotation(
        #     rate=PI / 10, about = 'theta'
        # )
        self.play(node_animation)

        # Create animation for edges
        animations_edges = [Create(self.edges_3d[edge]) for edge in range(len(self.random_graph.get_edges))]
        self.play(AnimationGroup(*animations_edges))
        # self.wait(5)   
            
    def _draw_graph(self):
        cache_nodes = ['U' for _ in range(len(self.random_graph.get_nodes))]
        cache_edges = ['U' for _ in range(len(self.random_graph.get_edges))]
        # Draw a map
        def redraw_map():
            nonlocal cache_nodes, cache_edges
            print(cache_nodes, self.node_status)
            diff_nodes = diff_arrays(self.node_status, cache_nodes) # Mask function -> Compares two lists of str and returns a binary list
            diff_edges = diff_arrays(self.edge_status, cache_edges) # Mask function -> Compares two lists of str and returns a binary list
            if 1 in diff_nodes:
                idx_n = diff_nodes.index(1)
                node = self.nodes_3d[idx_n]
                node_animation = AnimationGroup(node.animate.set_fill(color="#FF4500", opacity=1), node.animate.set_stroke(color=ORANGE, opacity=1))
                self.play(node_animation)
                print(cache_nodes)
            else:
                warnings.warn("Node status array not changed from previous state. Incorrect call to update graph.", UserWarning)
            if 1 in diff_edges:
                idx_e = diff_edges.index(1)
                edge = self.edges_3d[idx_e]
                edge_animation = AnimationGroup(edge.animate.set_stroke(color="#00FFFF", opacity=1, width = 1.25))
                self.play(edge_animation)
            cache_nodes, cache_edges = self.node_status.copy(), self.edge_status.copy()          
        return redraw_map

    def _update(self, node: int = -1, edge: int = -1, node_status : str = '', is_first: bool = False):
        if node > -1:
            if node_status == 'D':
                self.node_status[node] = 'D'
            if node_status == 'P':
                self.node_status[node] = 'P'
        if edge > -1:
            self.edge_status[edge] = 'D'
        
        print('Parent status: {}'.format(self.parent), 'Node status: {}'.format(self.node_status), 'Edge status: {}'.format(self.edge_status))


        # if is_first:
        #     self.redraw = self._draw_graph()
        #     self.redraw()
        # else:
        #     self.redraw()

    def _find_edge(self, start_node: int = None, end_node: int = None):
        # Go search in self.random_graph.get_edges the tuple corresponding to (start_node, end_node) or viceversa
        for tuple in self.random_graph.get_edges:
            if tuple == (start_node, end_node):
                return self.random_graph.get_edges.index((start_node, end_node))
            if tuple == (end_node, start_node):
                return self.random_graph.get_edges.index((end_node, start_node))

    def do_bfs(self):
        node = random.choice(self.random_graph.get_nodes)
        self.queue.append(node)
        self._update(node = node, node_status='D', is_first=True)
        while len(self.queue) > 0:
            v = self.queue.pop(0)
            for adj_n in self.random_graph.get_adjacency_list[v]:
                if self.node_status[adj_n] == 'U':
                    self.queue.append(adj_n)
                    self.parent[adj_n] = v
                    edge = self._find_edge(v, adj_n)
                    self._update(node=adj_n, edge=edge, node_status='D', is_first=False)
            self._update(node=v, node_status='P', is_first=False)

    # def do_dfs(self, start_node: int = 0):
    #     node = start_node
    #     self._update(node = start_node, node_status='D', is_first=True)
    #     for adj_n in self.random_graph.get_adjacency_list[node]:
    #         if self.node_status[adj_n] == 'U':
    #             self.parent[adj_n] = node
    #             edge = self._find_edge(node, adj_n)
    #             self._update(node=adj_n, edge=edge, node_status='D', is_first=False)
    #             self.do_dfs(adj_n)
    #         if self.node_status[adj_n] == 'D':
    #             edge = self._find_edge(node, adj_n)
    #             self._update(edge = edge, is_first=False)
    #     self._update(node = node, node_status='P', is_first=False)

    def do_dfs(self, start_node: int = None):
        self._update(node = start_node, node_status='D', is_first=True)
        stack = [start_node]
        while stack:
            node = stack.pop()
            for adj_n in self.random_graph.get_adjacency_list[node]:
                if self.node_status[adj_n] == 'U':
                    stack.append(adj_n)
                    self.parent[adj_n] = node
                    edge = self._find_edge(node, adj_n)
                    self._update(node=adj_n, edge=edge, node_status='D', is_first=False)
                elif self.node_status[adj_n] == 'D':
                    edge = self._find_edge(node, adj_n)
                    self._update(edge=edge, is_first=False)
            self._update(node=node, node_status='P', is_first=False)
    
    def _find_path(self, end: int = None):
        path = []
        # Recursive function to build the path from x to the root
        def build_path(node):
            if node == -1:
                print("Root node reached.")
                return
            else:
                build_path(self.parent[node])
                path.append(node)
                return

        build_path(end)
        return path
        
    def draw_path(self, node_end: int = None, color = RED):
        path_s_e = self._find_path(node_end)
        for idx in range(len(path_s_e) -1):
            node_current, node_next = path_s_e[idx], path_s_e[idx + 1]
            edge_idx = self._find_edge(node_current, node_next)
            edge = self.edges_3d[edge_idx]
            node_curr = self.nodes_3d[node_current]
            node_next = self.nodes_3d[node_next] 
            self.play(edge.animate.set_stroke(color=color, opacity=1), node_curr.animate.set_fill(color=color), node_next.animate.set_fill(color=color))

    def construct(self):
        # Execute search algorithm
        if self.is_bfs_search:
            self.do_bfs()
        else:
            self.do_dfs(start_node=random.choice(self.random_graph.get_nodes))

def code_to_test(nodes: int = 0, edges: int = 0):
    # Replace with your actual code
    graph = Graph3D(n_nodes = nodes, n_edges = edges, is_bfs_search=False)
    graph.render(preview=False)

def time_execution_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        args[0].execution_times[func.__name__] = execution_time
    return wrapper

class TestCodeExecutionTime(unittest.TestCase):

    execution_times = {}
    
    # @time_execution_decorator
    # def test_execution_time_1(self):
    #     code_to_test(10, 20)

    # @time_execution_decorator
    # def test_execution_time_2(self):
    #     code_to_test(50, 100)

    # @time_execution_decorator
    # def test_execution_time_3(self):
    #     code_to_test(100, 200)

    # @time_execution_decorator
    # def test_execution_time_4(self):
    #     code_to_test(250, 500)

    # @time_execution_decorator
    # def test_execution_time_5(self):
    #     code_to_test(500, 750)

    # @time_execution_decorator
    # def test_execution_time_6(self):
    #     code_to_test(1250, 2500)

    # @time_execution_decorator
    # def test_execution_time_7(self):
    #     code_to_test(3500, 7000)
    #     print(self.execution_times)

    # @time_execution_decorator
    # def test_execution_time_8(self):
    #     code_to_test(6250, 12500)

    @time_execution_decorator
    def test_execution_time_9(self):
        code_to_test(15000, 30000)

    # @time_execution_decorator
    # def test_execution_time_10(self):
    #     code_to_test(31250, 62500)

    # @time_execution_decorator
    # def test_execution_time_11(self):
    #     code_to_test(50000, 62500)

    def tearDown(self):
        print(self.execution_times)
        self.assertLess(self.execution_times[self._testMethodName], 10800) # Replace 1 with your desired maximum allowed execution time



if __name__ == "__main__":

    unittest.main()    
    # Print execution times after all tests have run
    print(TestCodeExecutionTime.execution_times)