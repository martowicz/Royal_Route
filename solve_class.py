from kruskal import *
from collections import deque
from queue import PriorityQueue
from data import runtests

class Vertex:
    def __init__(self):
        self.parent=None
        self.neighbours=[]
        self.level=None
        self.lords_to_check=[]
        self.maxresult=0
        self.children=[]
    
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
    dots=[]
    p=PriorityQueue()
    included=[False for _ in  range(len(tree))]
    
    for el in lord:
        if not included[el]:
            p.put((-tree[el].level, el))
            included[el]=True

    while True:
        l,u=p.get()
        for child in tree[u].children:
                if not included[child]:
                    dots.append(child)
        if u==lord_lca: return length,dots
        v=tree[u].parent
        length+=tree[u].getWeight(v)
        if not included[v]: 
            p.put((-tree[v].level, v))
            included[v]=True
            

    
            
    
"""
Muszę dodać tak aby każdy vertex miał atrybut children
Jeśli children = [] no to mamy do czynienia z liściem i jego wkładamy do kolejki
i od niego zaczynam przeszukiwanie. Pniemy się w górę aż dojdizemy do korzenia.
Operacji dokonujemy tylko i wyłącznie jeśli dany LORD ma w tym wierzchołku swoje LCA
mamy do wyboru 2 opcje: DP to maksymalna suma w danym wierzchołku
DP = max(suma dzieci wierzchołka, wartość lorda + to co pod nim)
Nie wiem tylko jak dodawać to co pod lordem (?)
"""






def solve(N,streets,lords):
    MST = kruskal_MST(N,streets)
    tree = [Vertex() for _ in range(N+1)]

    for u,v,w in MST:
        tree[u].add_neighbour(v,w)
        tree[v].add_neighbour(u,w)

    q=deque([1])
    tree[1].level=0

    while q:
        u = q.popleft()

        for v,w in tree[u].neighbours:
            if v!=tree[u].parent:
                tree[v].parent = u
                tree[u].children.append(v)
                tree[v].level = tree[u].level + 1
                q.append(v)
    l=len(lords)
    lord_value = [0 for _ in range(l)] #wartości dla każdego lorda
    lord_dots = [[] for _ in range(l)] #wierzchołki każdego lorda
    for i in range(l):
        
        fortresses=lords[i]
        n=len(fortresses)
        if n<=1:
            continue
        lord_LCA = get_LCA(fortresses[0],fortresses[1],tree)
        for j in range(2,n):
            lord_LCA = get_LCA(lord_LCA,fortresses[j],tree)
            
        tree[lord_LCA].lords_to_check.append(i)
        lord_value[i],lord_dots[i]= count_lord_way(tree, lords[i], lord_LCA) #dobrze liczy
    #do tego momentu kod działa dobrze


    #wrzucić do kolejki wszystkie liście
    m=len(tree)
    p = PriorityQueue()
    included = [False for _ in  range(m)]
    for i in range(1,m): #wierzchołki indeksowane od 1
        if len(tree[i].children)==0:
            p.put((-tree[i].level, i))
            included[i]=True
    #teraz w kolejce mam wszystkie dzieci
    l,v=p.get()
    while v is not None:
        if len(tree[v].lords_to_check)>0:
            
            for lord in tree[v].lords_to_check:
                res=lord_value[lord]
                for vertex in lord_dots[lord]:
                    res+=tree[vertex].maxresult
                tree[v].maxresult=max(tree[v].maxresult,res)

        sum_children=0
        for child in tree[v].children:
            sum_children += tree[child].maxresult
        tree[v].maxresult = max(tree[v].maxresult,sum_children)
        #tree[v].maxresult = max(sum_children, wzięcie lorda i tego co pod nim)
        #przydałoby się coś takiego jak lord_path
        next_v=tree[v].parent
        if next_v==None:
            p.put((1,next_v))
        elif not included[next_v]:
            p.put((-tree[next_v].level, next_v))
            included[next_v]=True
        
        l,v=p.get()
    return tree[1].maxresult



        
runtests(solve)


N=10
streets = [
    (1, 2, 1),
    (2, 3, 1),
    (3, 4, 1),
    (4, 5, 1),
    (5, 6, 1),
    (6, 7, 1),
    (7, 8, 1),
    (8, 9, 1),
    (9, 10, 1),
  ]
lords = [
    [1, 10],
    [2, 9],
    [3, 8],
    [4, 7],
    [5, 6],
  ]


solve(N, streets, lords)
        




    
