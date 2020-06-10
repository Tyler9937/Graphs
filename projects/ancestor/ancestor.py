"""
Simple graph implementation
"""
from collections import deque
# from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        This should be done using recursion.
        """
        if visited is None:
            visited = set()

        if path is None:
            path = []

        visited.add(starting_vertex)
        path = [*path, starting_vertex]

        if starting_vertex == destination_vertex:
            return path
        for n in self.get_neighbors(starting_vertex):

            if n not in visited:
                
                new_path = self.dfs_recursive(n, destination_vertex, visited, path)
                if new_path:

                    return new_path
        return None




def earliest_ancestor(ancestors, starting_node):
    graph = Graph() 
    longest_path = []

    # adding vertices and edges
    for tup in ancestors:
        graph.add_vertex(tup[0])
        graph.add_vertex(tup[1])

    for tup in ancestors:
        graph.add_edge(tup[0], tup[1])
  
    # calculating node paths saving longest
    for starting_vertex in graph.vertices:
        result = graph.dfs_recursive(starting_vertex, starting_node)


        if result is not None:
            if len(result) == len(longest_path):
                if result[0] < longest_path[0]:
                    longest_path = result
            elif len(result) > len(longest_path):
                longest_path = result

    if longest_path[0] == starting_node:

        return -1
    else:
        return longest_path[0] 
