# coding=utf-8
# Para uso de montículos mínimos
import heapq

class Heap(object):
    def __init__(self,data=[]):
        self.heap = [d for d in data]
        heapq.heapify(self.heap)

    def push(self, item):
        decorated = self.key(item), item
        heapq.heappush(self.heap, decorated)

    def pop(self):
        decorated = heapq.heappop(self.heap)
        return decorated

    def pushpop(self, item):
        decorated = self.key(item), item
        dd = heapq.heappushpop(self.heap, decorated)
        return dd[1]

    def replace(self, item):
        decorated = self.key(item), item
        dd = heapq.heapreplace(self.heap, decorated)
        return dd[1]

    # Dado un entero n, regresa los n elementos más pequeños.
    def getNSmallest(self,n=0):
        # Si no se asingó la n.
        if not n:
            n = len(self.heap)
        return heapq.nsmallest(n,self.heap)

    def size(self):
        return len (self.heap)

    def __len__(self):
        return len(self.heap)

if __name__ == '__main__':
    # Pruebas.
    li = [[1,"a"], [2,"c"], [3,"b"], [4,"e"], [5,"d"], [6,"f"], [7,"g"], [8,"h"], [9,"i"], [10,"j"]]
    heap = Heap(li)
    print(heap.getNSmallest())

