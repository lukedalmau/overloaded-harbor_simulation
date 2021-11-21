import heapq

class Heap:
    def __init__(self, items=[]):
        self.heap = []
        self.count = 0
        for item in items:
            self.push(item)
    
    def push(self, item):
        self.count += 1
        heapq.heappush(self.heap, item)
    
    def pop(self):
        self.count -= 1
        return heapq.heappop(self.heap)
    
    def peek(self):
        return self.heap[0]
    
    def isEmpty(self):
        return self.count == 0
    
    def size(self):
        return self.count
    
    def __str__(self):
        return str(self.heap)
    
    def __repr__(self):
        return str(self.heap)
    
    def __len__(self):
        return self.count
    
    def __iter__(self):
        return iter(self.heap)
    
    def __contains__(self, item):
        return item in self.heap
    
    def __getitem__(self, index):
        return self.heap[index]
    
    def __setitem__(self, index, item):
        self.heap[index] = item
        heapq.heapify(self.heap)
    
    def __delitem__(self, index):
        del self.heap[index]
        heapq.heapify(self.heap)
    
