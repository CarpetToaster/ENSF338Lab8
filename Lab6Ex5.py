import random 
import timeit


class PQNode:
    def __init__(self, item,  next = None):
        self.item = item
        self.next = next

# This implementation will take lower priority number value to be higher priority (i.e. prio = 0 is dequeued before prio = 9)
class ListPriorityQueue:
    def __init__(self, head = None):
        self.head = head
    
    def enqueue(self, item):
        newNode = PQNode(item)
        
        if self.head == None:
            self.head = newNode
            return
        
        pointer = self.head 
        while pointer.next != None and newNode.item > pointer.next.item:
            pointer = pointer.next
            
            
        newNode.next = pointer.next
        pointer.next = newNode
        
        
    def dequeue(self):
        if self.head == None:
            return None
        
        returnee = self.head
        self.head = self.head.next
        return returnee.item        
        


# From ex4 implementation but as minheap instead (comparisons are flipped, and variable largest is changed to smallest)

class Node:
    dictionary = {}
    
    def __init__(self, name):
        self.name = name
        self.item = self.dictionary[self.name]
        
    def _updateNodeItem(self):
        self.item = self.dictionary[self.name]
        
    def itemm(self):
        self.item = self.dictionary[self.name]
        return self.item


class HeapPriorityQueue:
    def __init__(self):
        self.heap = []
        self.length = 0
        
    def heapify(self, arr: list): 
        start = len(arr)//2 - 1
        self.heap = arr
        self.length = len(arr)
        
        # use post-order traversal to make a max heap
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
    
    
    
# TESTING IMPLEMENTATIONS  
'''
lpq = ListPriorityQueue()

for i in range(10):
    lpq.enqueue(i)
    
lpq.enqueue(12)
lpq.enqueue(20)
lpq.enqueue(14)
    
pointer = lpq.head
for i in range(13):
    print(pointer.item)
    pointer = pointer.next

print(120*"*")  
print(lpq.dequeue())
print(120*"*")  

pointer = lpq.head
for i in range(12):
    print(pointer.item)
    pointer = pointer.next
    
print("\n")
    
testArray = [1, 3, 5, 4, 6, 13, 10, 9, 8, 15, 17]

testHeap = HeapPriorityQueue()
testHeap.heapify(testArray)
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.enqueue(13)
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
print(120*"*")
testHeap.dequeue()
testHeap.printHeap()
print(testHeap.isHeap())
'''

"""
def heapVsList():
    tasks = random.choices([0, 1], weights=[(7/3), 1], k=1000) # weights are equivalent to 0.7 and 0.3 for pure probability.
    
    '''
    print(tasks)
    ones = 0
    zeros = 0 
    for i in range(1000):
        if tasks[i] == 0:
            zeros += 1
        else:
            ones += 1
            
    print(zeros, ones)
    ''' # check it produces expected amounts (the first time it ran it got exactly 700 300 haha)
    
    # test Lists first
    listQueue = ListPriorityQueue()
    listQueueTime = timeit.timeit(lambda: test(listQueue, tasks), number = 10)
    
    # Now test the heap
    heapQueue = HeapPriorityQueue()
    heapQueueTime = timeit.timeit(lambda: test(heapQueue, tasks), number = 10)
    
    print(listQueueTime, heapQueueTime)


def test(queue, tasks):
    for i in tasks:
        if tasks[i] == 0:
            incomingInt = random.choice(range(1000))
            queue.enqueue(incomingInt)
        else:
            queue.dequeue()
            
heapVsList()

'''
4)      After running the script, we can see the results in the terminal. On average, the List implementaion takes just under a second while the heap implementation takes 
        around 0.005 -- Although occaisonally the list will take somewhere between 0.001 and 0.2 seconds to complete (This probably comes down to some insane streak of luck where all dequeues were generated, or some 
        strange error, regardless it was worth mentioning). This makes sense when considering the nature of each of the sata structures: linked lists are at their core linear 
        and always take linear time to just traverse and also to enqueue, although their dequeues are O(1) since we just pop from head. Heaps are derived from binary trees, which are deisgned
        to have logarithmic times, so although both enqueues and dequeues are O(log(n)), since we enqueue way more, the faster time complexity pays off a lot - In fact even if we were 
        queuing and dequeuing the same amount, the heap should still be faster due to the nature of how slowly logarithms grow.
'''
            
"""



