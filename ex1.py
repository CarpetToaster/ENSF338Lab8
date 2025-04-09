import re

class GraphNode:
    """Represents a node in the graph."""
    def __init__(self, data):
        self.data = data

class Graph:
    """Undirected graph implemented with an adjacency list."""
    def __init__(self):
        self.nodes = {}      # Maps node data (str) to GraphNode objects
        self.adjacency = {}  # Adjacency list: {node_data: {neighbor_data: weight}}

    def addNode(self, data):
        """Adds a node with the given data (string). Returns the node."""
        if data in self.nodes:
            return self.nodes[data]  # Avoid duplicates
        node = GraphNode(data)
        self.nodes[data] = node
        self.adjacency[data] = {}  # Initialize empty neighbor dict
        return node

    def removeNode(self, node):
        """Removes a node and all connected edges."""
        data = node.data
        if data not in self.nodes:
            return
        
        # Remove all edges connected to this node
        for neighbor in list(self.adjacency[data].keys()):
            del self.adjacency[neighbor][data]
        
        # Remove the node
        del self.nodes[data]
        del self.adjacency[data]

    def addEdge(self, n1, n2, weight=1.0):
        """Adds an undirected edge between n1 and n2 with the given weight."""
        d1, d2 = n1.data, n2.data
        if d1 in self.nodes and d2 in self.nodes:
            self.adjacency[d1][d2] = weight
            self.adjacency[d2][d1] = weight  # Undirected graph

    def removeEdge(self, n1, n2):
        """Removes the edge between n1 and n2."""
        d1, d2 = n1.data, n2.data
        if d1 in self.adjacency and d2 in self.adjacency[d1]:
            del self.adjacency[d1][d2]
        if d2 in self.adjacency and d1 in self.adjacency[d2]:
            del self.adjacency[d2][d1]

    def importFromFile(self, file):
        """Imports a graph from a GraphViz file. Returns None on failure."""
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
        except FileNotFoundError:
            return None

        # Check for "strict graph" (undirected)
        if not content.startswith("strict graph"):
            return None
        if "digraph" in content.splitlines()[0]:  # Reject directed graphs
            return None

        # Extract the body between curly braces
        start = content.find('{')
        end = content.rfind('}')
        if start == -1 or end == -1 or start >= end:
            return None
        body = content[start + 1:end].strip()

        # Clear existing graph
        self.nodes.clear()
        self.adjacency.clear()

        # Parse edges (format: "node1 -- node2 [weight=X];")
        edge_pattern = re.compile(r'"?([\w-]+)"?\s*--\s*"?([\w-]+)"?\s*(?:\[weight=([\d.]+)\])?')
        for line in body.split(';'):
            line = line.strip()
            if not line:
                continue
            match = edge_pattern.match(line)
            if not match:
                return None  # Invalid edge format

            n1, n2, weight_str = match.groups()
            weight = 1.0 if weight_str is None else float(weight_str)

            # Add nodes and edge
            node1 = self.addNode(n1)
            node2 = self.addNode(n2)
            self.addEdge(node1, node2, weight)

        return self  # Success


if __name__ == "__main__":
    # Test with random.dot
    g = Graph()
    if g.importFromFile("random.dot") is None:
        print("Error: Failed to import the graph.")
    else:
        print(f"Nodes loaded: {len(g.nodes)}")
        print(f"Edges loaded: {sum(len(edges) for edges in g.adjacency.values()) // 2}")