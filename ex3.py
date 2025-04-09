class DisjointSet:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) 
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return False

        # union by rank
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1

        return True

class Graph:
    def __init__(self):
        self.adj = {} 

    def addNode(self, data):
        if data not in self.adj:
            self.adj[data] = []

    def addEdge(self, n1, n2, weight=1):
        self.addNode(n1)
        self.addNode(n2)
        self.adj[n1].append((n2, weight))
        self.adj[n2].append((n1, weight))  

    def mst(self):
        ds = DisjointSet()
        for node in self.adj:
            ds.make_set(node)


        edges = []
        for u in self.adj:
            for v, w in self.adj[u]:
                if (v, u, w) not in edges: 
                    edges.append((u, v, w))

        # Sort edges by weight
        edges.sort(key=lambda x: x[2])

        mst_graph = Graph()

        for u, v, w in edges:
            if ds.union(u, v):
                mst_graph.addEdge(u, v, w)

        return mst_graph

    def __str__(self):
        result = ""
        for node in self.adj:
            result += f"{node}: {self.adj[node]}\n"
        return result


if __name__ == "__main__":
    g = Graph()
    g.addEdge("A", "B", 4)
    g.addEdge("A", "C", 2)
    g.addEdge("B", "C", 5)
    g.addEdge("B", "D", 10)
    g.addEdge("C", "D", 3)
    g.addEdge("C", "E", 4)
    g.addEdge("D", "E", 1)

    print("Original Graph:")
    print(g)

    mst = g.mst()
    print("\nMinimum Spanning Tree:")
    print(mst)
