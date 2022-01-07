# Course: 261
# Author: Rachel Thomas
# Assignment: 6
# Description:Implement an Undirected Graph class with the following methods; add_vertex(), add_edge()
# remove_edge(), remove_vertex(), get_vertices(), get_edges(), is_valid_path(), dfs(), bfs(),
# count_connected_components(), has_cycle()

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """

        self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return None

        if u not in self.adj_list and v not in self.adj_list:  # neither in list
            self.add_vertex(u)
            self.add_vertex(v)

        elif u not in self.adj_list:  # just u not in list
            self.add_vertex(u)
        elif v not in self.adj_list:  # just v not in list
            self.add_vertex(v)

        if v in self.adj_list[u]:  # already has an edge
            return None
        else:
            self.adj_list[u].append(v)

        if u in self.adj_list[v]:
            return None
        else:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v not in self.adj_list or u not in self.adj_list:
            return None

        if u not in self.adj_list[v]:
            return None

        else:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list:
            return None

        for vertex in self.adj_list[v]:  # things v is connected too
            self.adj_list[vertex].remove(v)  # remove all edges going to v
        del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertex_list = []
        if len(self.adj_list) == 0:
            return vertex_list
        else:
            for key in self.adj_list:
                vertex_list.append(key)
        return vertex_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []
        if len(self.adj_list) == 0:
            return edge_list

        for key in self.adj_list:
            for value in self.adj_list[key]:
                if (key, value) and (value, key) not in edge_list:
                    edge_list.append((key, value))
        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
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
                if item not in self.adj_list:
                    return False
                elif next not in self.adj_list[item]:
                    return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        reachable = []
        stack = []

        if v_start not in self.get_vertices():
            return reachable
        else:
            stack.append(v_start)

        while len(stack) > 0:
            v = stack.pop()
            successors = sorted(self.adj_list[v], reverse=True)
            if v not in reachable:
                reachable.append(v)
                if v == v_end:
                    return reachable
                for item in successors:
                    stack.append(item)
        return reachable

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        reachable = []
        q = deque()

        if v_start not in self.get_vertices():
            return reachable
        else:
            q.append(v_start)

        while len(q) > 0:
            v = q.popleft()
            successors = sorted(self.adj_list[v])
            if v not in reachable:
                reachable.append(v)
                if v == v_end:
                    return reachable
                for item in successors:
                    if item not in reachable:
                        q.append(item)

        return reachable

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        count = 0
        visited = []

        for vertex in self.get_vertices():
            if vertex not in visited:
                reachable = self.dfs(vertex)
                count += 1
                for vertex in reachable:
                    if vertex not in visited:
                        visited.append(vertex)
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        stack = []
        visited = []
        flags = {}

        for vertex in self.get_vertices():
            flags[vertex] = -1

        vertex_list = self.get_vertices()
        if len(vertex_list) > 0:
            v = vertex_list[0]
            stack.append(v)
            flags[v] = 0
        else:
            return False
        for v in vertex_list:
            stack.append(v)
            flags[v] = 0
            while len(stack) > 0:
                v = stack.pop()
                successors = sorted(self.adj_list[v], reverse=True)
                if v not in visited:
                    visited.append(v)
                    flags[v]= 1
                    if len(successors)>0:
                        for item in successors:
                            if flags[item] ==0:
                                return True
                            stack.append(item)
                            if flags[item] == -1:
                                flags[item]=0

        return False



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
