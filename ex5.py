from collections import defaultdict

class Graph:
    def __init__(self):
        self.adj = defaultdict(list)

    def addNode(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def addEdge(self, u, v):
        self.addNode(u)
        self.addNode(v)
        self.adj[u].append(v) 

    def isdag(self):
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.adj:
            if node not in visited:
                if dfs(node):
                    return False 
        return True

    def toposort(self):
        visited = set()
        rec_stack = set()
        topo_order = []
        cycle_found = False

        def dfs(node):
            nonlocal cycle_found
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    cycle_found = True
            rec_stack.remove(node)
            topo_order.append(node)

        for node in self.adj:
            if node not in visited:
                dfs(node)

        if cycle_found:
            return None
        return topo_order[::-1] 

# Example usage
if __name__ == "__main__":
    g = Graph()
    g.addEdge("A", "C")
    g.addEdge("B", "C")
    g.addEdge("C", "D")
    g.addEdge("D", "E")

    print("Is DAG?", g.isdag())
    print("Topological Sort:", g.toposort())


# Question 1: Topological sorting can be implemented using an algorithm seen in
# class. Which algorithm? Why?


# Topological sorting can be implemented using **DFS traversal**.
# DFS is chosen here because:
# - It explores each path as deep as possible before backtracking,
# - Naturally supports post-order traversal, where a node is added to the result
#   only after all its dependencies (children) are visited,
# - A cycle is detected if we revisit a node that is currently in the recursion stack.
