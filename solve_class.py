from kruskal import *
from collections import deque
from queue import PriorityQueue

class Vertex:
    def __init__(self):
        self.parent=None
        self.neighbours=[]
        self.level=None
        self.lords_to_check=[]
        self.result=0
    
    def add_neighbour(self, neighbour, weight):
        self.neighbours.append((neighbour,weight))

    def getWeight(self, neighbour):
        for v,w in self.neighbours:
            if v==neighbour: return w 


def get_LCA(a,b,tree):
    if tree[a].level > tree[b].level:
        a,b=b,a
    while tree[b].level > tree[a].level:
        b=tree[b].parent
    while a!=b:
        b=tree[b].parent
        a=tree[a].parent
    return a

def count_lord_way(tree,lord, lord_lca):
    length=0
    p=PriorityQueue()
    included=[False for _ in  range(len(tree))]
    
    for el in lord:
        if not included[el]:
            p.put((-tree[el].level, el))
            included[el]=True
    while True:
        l,u=p.get()
        if u==lord_lca: return length
        v=tree[u].parent
        length+=tree[u].getWeight(v)
        if not included[v]: 
            p.put((-tree[v].level, v))
            included[v]=True
    
            
    
    






def solve(N,streets,lords):
    MST = kruskal_MST(streets)
    tree = [Vertex() for _ in range(N+1)]

    for u,v,w in MST:
        tree[u].add_neighbour(v,w)
        tree[v].add_neighbour(u,w)

    q=deque([8])
    tree[8].level=0

    while q:
        u = q.popleft()

        for v,w in tree[u].neighbours:
            if v!=tree[u].parent:
                tree[v].parent = u
                tree[v].level = tree[u].level + 1
                q.append(v)
    
    for i in range(len(lords)):
        fortresses=lords[i]
        n=len(fortresses)
        lord_LCA = get_LCA(fortresses[0],fortresses[1],tree)
        for j in range(2,n):
            lord_LCA = get_LCA(lord_LCA,fortresses[j],tree)
        tree[lord_LCA].lords_to_check.append(i)
        lord_way= count_lord_way(tree, lords[i], lord_LCA) #dobrze liczy
        print(lord_way)
    #do tego momentu kod działa dobrze

        

    iterator=0
    for element in tree:
        print("Vertex: ",iterator, " " ,element.lords_to_check)
        iterator+=1


N=17
streets = [
    (1, 2, 8),
    (1, 3, 9),
    (1, 4, 10),
    (2, 3, 5),
    (2, 5, 6),
    (2, 7, 9),
    (3, 4, 7),
    (3, 5, 7),
    (3, 6, 8),
    (4, 6, 9),
    (5, 6, 7),
    (5, 7, 8),
    (5, 8, 9),
    (5, 9, 10),
    (6, 9, 11),
    (7, 8, 5),
    (7, 16, 9),
    (8, 9, 5),
    (8, 10, 6),
    (8, 11, 7),
    (8, 16, 9),
    (9, 11, 8),
    (9, 12, 8),
    (9, 17, 10),
    (10, 11, 5),
    (10, 12, 7),
    (10, 13, 8),
    (10, 17, 9),
    (11, 14, 9),
    (11, 16, 9),
    (12, 17, 10),
    (13, 14, 5),
    (13, 17, 4),
    (14, 15, 6),
    (14, 17, 6),
    (15, 16, 7),
]
lords = [
    [1, 4, 5],
    [3, 8],
    [6, 9, 10],
    [11, 12, 15],
    [7, 14, 17],
    [13, 16],
]



solve(N, streets, lords)
        




    
