import re
import time
from ex1 import Graph, GraphNode  

class Graph2:
    def __init__(self):
        self.nodes = {}          
        # Maps node data (str) to GraphNode objects
        self.data_to_index = {}   
        self.index_to_data = []  
        self.matrix = []          

    def addNode(self, data):
        if data in self.nodes:
            return self.nodes[data]
        node = GraphNode(data)
        self.nodes[data] = node
        index = len(self.index_to_data)
        self.data_to_index[data] = index
        self.index_to_data.append(data)
        # Expand the matrix
        new_size = index + 1
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * new_size)
        return node

    def removeNode(self, node):
        data = node.data
        if data not in self.nodes:
            return
        # Remove node from mappings and matrix
        index = self.data_to_index[data]
        del self.data_to_index[data]
        self.index_to_data.pop(index)
        del self.nodes[data]
        self.matrix.pop(index)
        for row in self.matrix:
            row.pop(index)
        self.data_to_index = {d: idx for idx, d in enumerate(self.index_to_data)}

    def addEdge(self, n1, n2, weight=1.0):
        d1, d2 = n1.data, n2.data
        if d1 not in self.data_to_index or d2 not in self.data_to_index:
            return
        i1, i2 = self.data_to_index[d1], self.data_to_index[d2]
        self.matrix[i1][i2] = weight
        self.matrix[i2][i1] = weight  

    def removeEdge(self, n1, n2):
        d1, d2 = n1.data, n2.data
        if d1 in self.data_to_index and d2 in self.data_to_index:
            i1, i2 = self.data_to_index[d1], self.data_to_index[d2]
            self.matrix[i1][i2] = 0
            self.matrix[i2][i1] = 0

    def importFromFile(self, file):
        # Similar to Graph's importFromFile but for adjacency matrix
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
        except FileNotFoundError:
            return None
        if not content.startswith("strict graph"):
            return None
        start = content.find('{')
        end = content.rfind('}')
        if start == -1 or end == -1 or start >= end:
            return None
        body = content[start+1:end].strip()
        edge_pattern = re.compile(r'"?([\w-]+)"?\s*--\s*"?([\w-]+)"?\s*(?:\[weight=([\d.]+)\])?')
        self.nodes.clear()
        self.data_to_index.clear()
        self.index_to_data.clear()
        self.matrix = []
        edges = []
        nodes_set = set()
        for line in body.split(';'):
            line = line.strip()
            if not line:
                continue
            match = edge_pattern.match(line)
            if not match:
                return None
            n1, n2, weight_str = match.groups()
            weight = 1.0 if weight_str is None else float(weight_str)
            edges.append((n1, n2, weight))
            nodes_set.add(n1)
            nodes_set.add(n2)
        for node in nodes_set:
            self.addNode(node)
        for n1, n2, weight in edges:
            node1 = self.nodes[n1]
            node2 = self.nodes[n2]
            self.addEdge(node1, node2, weight)
        return self

    def dfs(self):
        visited = set()
        result = []
        for data in self.index_to_data:
            if data not in visited:
                stack = [data]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        result.append(current)
                        current_idx = self.data_to_index[current]
                        # Iterate through all possible neighbors in matrix
                        for neighbor_idx, weight in enumerate(self.matrix[current_idx]):
                            if weight > 0:
                                neighbor_data = self.index_to_data[neighbor_idx]
                                if neighbor_data not in visited:
                                    stack.append(neighbor_data)
        return result

# Extend the original Graph class with DFS method
def graph_dfs(self):
    visited = set()
    result = []
    nodes = list(self.nodes.keys())
    for node in nodes:
        if node not in visited:
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    result.append(current)
                    # Push neighbors in reverse order for correct DFS order
                    for neighbor in reversed(list(self.adjacency[current].keys())):
                        if neighbor not in visited:
                            stack.append(neighbor)
    return result

Graph.dfs = graph_dfs

if __name__ == "__main__":
    g = Graph()
    if g.importFromFile("random.dot") is None:
        raise Exception("Failed to import graph")
    
    g2 = Graph2()
    if g2.importFromFile("random.dot") is None:
        raise Exception("Failed to import graph for Graph2")
    
    times_graph = []
    for _ in range(10):
        start = time.time()
        g.dfs()
        times_graph.append(time.time() - start)
    
    times_graph2 = []
    for _ in range(10):
        start = time.time()
        g2.dfs()
        times_graph2.append(time.time() - start)
    
    avg_graph = sum(times_graph) / 10
    max_graph = max(times_graph)
    min_graph = min(times_graph)
    
    avg_graph2 = sum(times_graph2) / 10
    max_graph2 = max(times_graph2)
    min_graph2 = min(times_graph2)
    
    print("Graph (Adjacency List) Results:")
    print(f"Average time: {avg_graph:.6f}s")
    print(f"Max time: {max_graph:.6f}s")
    print(f"Min time: {min_graph:.6f}s")
    print("\nGraph2 (Adjacency Matrix) Results:")
    print(f"Average time: {avg_graph2:.6f}s")
    print(f"Max time: {max_graph2:.6f}s")
    print(f"Min time: {min_graph2:.6f}s")

    # Discussion (as comments)
    # The adjacency list (Graph) implementation is faster than the adjacency matrix (Graph2).
    # This is because the adjacency matrix requires checking all nodes for each adjacency, resulting in O(n^2) time,
    # whereas the adjacency list only checks existing neighbors, leading to O(n + m) time, which is more efficient for sparse graphs.