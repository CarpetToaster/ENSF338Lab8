import re
from ex1 import Graph, GraphNode
import timeit
import matplotlib.pyplot as plt


'''
1)      The slower way to implement a queue would be a simple array or linked list. Either or will have a search complexity of O(n).
        The faster way is to use a heap as a priority queue, as now enqueuing will have a time complexity of O(log(n)). 
'''

# New Node class used for comparison in HeapPriorityQueue
class Node:
    # Class member use is clearer later, but we need it for itemm()
    dictionary = {}
    
    def __init__(self, name):
        self.name = name
        self.item = self.dictionary[self.name]
    
    def itemm(self):
        self.item = self.dictionary[self.name]
        return self.item

#Modified heap prio queue as min heap from lab 6 ex5
class HeapPriorityQueue:
    def __init__(self):
        self.heap = []
        self.length = 0
        
    def heapify(self, arr: list): 
        start = len(arr)//2 - 1
        self.heap = arr
        self.length = len(arr)
        
        for i in range(start):
            self._makeHeap(i)
        
    def _makeHeap(self, root = 0):
        smallest = root
        left = 2*root + 1
        right = 2*root + 2
        
        if left < self.length and self.heap[left].itemm() < self.heap[smallest].itemm():
            smallest = left
            
        if right < self.length and self.heap[right].itemm() < self.heap[smallest].itemm():
            smallest = right
            
        if smallest != root:
            self.heap[root], self.heap[smallest] = self.heap[smallest], self.heap[root]
            self._makeHeap(smallest)
            
    def printHeap(self):
        for i in range(self.length):
            print(self.heap[i].itemm(), end=" ")
        print()
            
    def enqueue(self, item):
        self.length += 1
        self.heap.append(item)
        
        start = self.length - 1
        parent = (start - 1)//2
        while self.heap[start].itemm() > self.heap[parent].itemm() and start != 0:
            self.heap[start], self.heap[parent] = self.heap[parent], self.heap[start] 
            
            start = parent
            parent = (start - 1)//2
            
    def dequeue(self):
        if self.length == 0:
            return None
        
        self.length -= 1
        returnee = self.heap[0]
        self.heap[0] = self.heap[self.length]
        self.heap.pop()
        
        start = 0
        leftChild = 2*start + 1
        rightChild = 2*start + 2
        
        smallerChild = 0
        if leftChild < self.length:
            if rightChild < self.length:
                smallerChild = leftChild if (self.heap[leftChild].itemm() < self.heap[rightChild].itemm()) else rightChild
            else:
                smallerChild = leftChild
        
        while smallerChild < self.length and self.heap[start].itemm() > self.heap[smallerChild].itemm():
            self.heap[start], self.heap[smallerChild] = self.heap[smallerChild], self.heap[start]
            
            start = smallerChild
            leftChild = 2*start + 1
            rightChild = 2*start + 2
        
            if rightChild < self.length:
                smallerChild = leftChild if (self.heap[leftChild].itemm() < self.heap[rightChild].itemm()) else rightChild
            else:
                smallerChild = leftChild
            
        return returnee
    
    def isHeap(self, root = 0):
        if root >= int((self.length - 1)//2):
            return True
        
        if(self.heap[root].itemm() <= self.heap[2*root + 1].itemm() and 
        self.heap[root].itemm() <= self.heap[2*root + 2].itemm() and 
        self.isHeap(2*root + 1) and
        self.isHeap(2*root + 2)): 
            return True
      
        return False
    
    
    
# Graph2 adds the required methods, inherits from graph to keep life easy
class Graph2(Graph):
    
    def fastSP(self, node):
        currDist = {} # represent infinite with 999999
        pred = {}
        toBeChecked = {}
        queue = HeapPriorityQueue()

        for vertex in self.nodes:
            currDist[vertex] = 999999
            pred[vertex] = None
            toBeChecked[vertex] = True

        currDist[node] = 0
        Node.dictionary = currDist
        queue.enqueue(Node(node))

        while queue.length > 0:
            closestVertex = queue.dequeue().name
            toBeChecked[closestVertex] = False
        
        
            for unvisited in self.adjacency[closestVertex]:
                tempDist = currDist[closestVertex] + self.adjacency[closestVertex][unvisited]
                    
                if tempDist < currDist[unvisited]:
                    currDist[unvisited] = tempDist
                    pred[unvisited] = closestVertex
                
                    Node.dictionary = currDist
                    queue.enqueue(Node(unvisited))

        return currDist, pred
    
    
    
    def slowSP(self, node):
        currDist = {} # represent infinite with 999999
        pred = {}
        toBeChecked = []
        
        for vertex in self.nodes:
            currDist[vertex] = 999999
            pred[vertex] = None
            toBeChecked.append(vertex)
            
        currDist[node] = 0

        while len(toBeChecked) != 0:
            # Implementation here is just a linear search in an array, not even a priority queue but easy to implement.
            closestVertex = None
            for vertex in toBeChecked:
                if closestVertex == None or currDist[vertex] < currDist[closestVertex]:
                    closestVertex = vertex
                    
                    
            toBeChecked.remove(closestVertex)
            
             
            for unvisited in self.adjacency[closestVertex]:
                tempDist = currDist[closestVertex] + self.adjacency[closestVertex][unvisited]
                
                if tempDist < currDist[unvisited]:
                    currDist[unvisited] = tempDist
                    
                    pred[unvisited] = closestVertex
                        
        return currDist, pred


graph = Graph2()
if graph.importFromFile("random.dot") == None:
    print("Failed!")
    
else:
    slowSet = []
    fastSet = []

    # print(graph.fastSP("0"))
    # print(graph.slowSP("0"))
    
    for node in graph.nodes:
        print(f"Running node: {node}")
        slowTime = timeit.timeit(lambda: graph.slowSP(node), number = 1)
        print("slow finished")
        fastTime = timeit.timeit(lambda: graph.fastSP(node), number = 1)
        print("fast finished")
        slowSet.append(slowTime)
        fastSet.append(fastTime)
    
    print(f"\nslowSp:\nFastest = {min(slowSet)}, Average = {sum(slowSet)/len(slowSet)}, Slowest = {max(slowSet)}")
    print(f"\nfastSp:\nFastest = {min(fastSet)}, Average = {sum(fastSet)/len(fastSet)}, Slowest = {max(fastSet)}")    
    
    plt.hist(slowSet + fastSet, bins = 20, histtype="barstacked", color="white", edgecolor="blue")
    plt.show()
    
'''
4)      There appears to be a binormal distribution, with the left one likely being most contributed to by
        the faster algorithm and the slower being more contributed to by the slower one. Just looking at
        the fastet, slowest, and average times for each in the terminal supports this as well, since their
        slowests appear to be very similar while average match the peaks of the distribution, and the difference 
        between the fastest time is pretty large as well.
'''
        
        
        