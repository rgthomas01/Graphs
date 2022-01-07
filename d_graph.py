# Course: CS261 - Data Structures
# Author: Rachel Thomas
# Assignment:6
# Description: Implement a directed graph with the following methods add_vertex(), add_edge()
# remove_edge(), get_vertices(), get_edges()
# is_valid_path(), dfs(), bfs()
# has_cycle(), dijkstra()

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to graph, returns number of vertices in graph after the addition
        """
        self.adj_matrix.append([])
        for list in self.adj_matrix:
            while len(list) != len(self.adj_matrix):
                list.append(0)
        self.v_count = len(self.adj_matrix)
        return len(self.adj_matrix)

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a new edge to the graph. If either vertices does not exist, if the weight is negative, or if src and drc
        are the same method does nothing. If the edge already exists it will update its weight
        """
        if src == dst or weight < 0:
            return None

        if src > self.v_count - 1 or dst > self.v_count - 1:
            return None

        if self.adj_matrix[src][dst] != 0:
            self.adj_matrix[src][dst] = weight

        else:
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between two vertices. If either vertices does not exist or there is no edge between them it
        does nothing
        """

        if src > self.v_count - 1 or dst > self.v_count - 1:
            return None
        if src < 0 or dst < 0:
            return None

        if self.adj_matrix[src][dst] == 0:
            return None

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of vertices
        """
        vertex_list = []
        for i in range(len(self.adj_matrix)):
            vertex_list.append(i)
        return vertex_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []
        if len(self.adj_matrix) == 0:
            return edge_list

        x = -1
        y = -1
        for list in self.adj_matrix:  # for each list
            x += 1
            y = -1
            for value in list:
                y += 1
                if value != 0:
                    edge_list.append((x, y, value))
        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Returns true is given path is valid. Empty path is considered valid
        """
        if len(path) == 0:
            return True

        if len(path) == 1:
            if path[0] in self.get_vertices():
                return True
            else:
                return False

        for index in range(len(path)):
            if index + 1 <= len(path) - 1:
                item = path[index]
                next = path[index + 1]

                if self.adj_matrix[item][next] == 0:
                    return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns list of vertices from DFS in the order they were visited. Vertices are chosen by vertex indicies in
        ascending order
        """
        reachable = []
        stack = []
        successors = []

        if v_start not in self.get_vertices():
            return reachable
        else:
            stack.append(v_start)

        while len(stack) > 0:
            v = stack.pop()
            index = -1
            for item in self.adj_matrix[v]:
                index += 1
                if item != 0:
                    successors.append(index)
                successors = sorted(successors, reverse=True)

            if v not in reachable:
                reachable.append(v)
                if v == v_end:
                    return reachable
                for item in successors:
                    stack.append(item)
            successors = []
        return reachable

    def bfs(self, v_start, v_end=None) -> []:
        """
        Returns list of vertices from BFS in the order they were visited. Vertices are chosen by vertex indicies in
        ascending order
        """
        reachable = []
        q = deque()
        successors = []

        if v_start not in self.get_vertices():
            return reachable
        else:
            q.append(v_start)

        while len(q) > 0:
            v = q.popleft()
            index = -1
            for item in self.adj_matrix[v]:
                index += 1
                if item != 0:
                    successors.append(index)
                successors = sorted(successors)

            if v not in reachable:
                reachable.append(v)
                if v == v_end:
                    return reachable
                for item in successors:
                    q.append(item)
            successors = []
        return reachable

    def has_cycle(self):
        """
        Returns True if at least one cycle in graph. False otherwise
        """
        flag = {}
        stack = []
        visited = []
        successors = []

        vertex_list = self.get_vertices()
        if len(vertex_list) < 0:
            return False

        for v in vertex_list:
            for vertex in self.get_vertices():
                flag[vertex] = -1
            stack.append(v)

            while len(stack) > 0:
                v = stack.pop()
                flag[v] = 0
                index = -1
                for item in self.adj_matrix[v]:
                    index += 1
                    if item != 0:
                        successors.append(index)
                successors = sorted(successors, reverse=True)
                if v not in visited:
                    visited.append(v)
                    if len(successors) > 0:
                        for item in successors:
                            if flag[item] == 1:
                                flag[item] = 0
                        for item in successors:
                            if flag[item] == 0:
                                return True

                            elif flag[item] == -1:
                                stack.append(item)
                                flag[item] = 0

                            elif flag[item] == 1:
                                flag[item] = 0


                    else:
                        flag[v] = 1

                successors = []

        return False

    def dijkstra(self, src: int) -> []:
        """
        Performs Dijkstra algorithm to compute the length of shortest path from given vertex to all other vertices in
        the graph . Value at index of return list corresponds to length of path to that vertex
        """
        q = []
        visited = {}
        d = 0
        vertex = src
        successors = []

        heapq.heappush(q, (d, vertex))

        while len(q) > 0:
            d, vertex = heapq.heappop(q)
            index = -1
            if vertex not in visited.keys():
                visited[vertex] = d
                for item in self.adj_matrix[vertex]:  # get successors
                    index += 1
                    if item != 0:
                        successors.append((item + d, index))
                    successors = sorted(successors, reverse=True)
                    for item in successors:
                        heapq.heappush(q, (item))  # item plus d is weight + prev weight
                    successors = []

        solution = {}
        for i in range(len(self.adj_matrix)):
            solution[i] = float('inf')

        result = []
        for key in visited:
            value = visited[key]
            solution[key] = value

        for i in range(len(self.adj_matrix)):
            w = solution[i]
            result.append(w)
        return (result)


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')

    print("\nPDF - Cycles() example 2")
    print("--------------------------")
    edges = [(0, 4, 10), (2, 3, 3), (2, 5, 13), (3, 7, 11), (3, 5, 8), (2, 12, 3),
             (5, 2, 15), (7, 4, 14), (7, 8, 19), (9, 4, 5), (10, 11, 17), (11, 6, 2)]

    g = DirectedGraph(edges)
    print('\n', g)

    for i in range(13):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
