from data import runtests

class Node:
    def __init__(self,value):
        self.val=value
        self.parent=self
        self.rank=0

def find(x): 
    if x.parent!=x:
        x.parent=find(x.parent)
    return x.parent

def union(x,y):
    x=find(x)
    y=find(y)
    if x.rank>y.rank:
        y.parent=x
    else:
        x.parent=y
        if x.rank==y.rank:
            y.rank+=1


def kruskal_MST(G): #graf w postaci listy krawędzi
    G.sort(key=lambda edge: edge[2]) #F=sorted(G, key=lambda egde: egde[2])
    #G.reverse()
    MST=[]
    nodes=[Node(i) for i in range(len(G))]
    for x,y,w in G:
        #Jeśli dodatkowa krawędź z tymi co już są nie tworzy cyklu, to ją dodaję
        if find(nodes[x]) != find(nodes[y]):
            union(nodes[x],nodes[y])
            MST.append((x,y,w))
    return MST

def edges_to_neighbours(N,edges):
    graph = [[] for _ in range(N+1)]
    for u,v,w in edges:
        graph[u].append((v,w))
        graph[v].append((u,w))
    return graph



def solution(N,edges,lords):
    MST = kruskal_MST(edges) #minimalne drzewo rozpinające
    tree=edges_to_neighbours(MST) #postać sąsiedztwa
    queue=[8]
    parent=[None for _ in range(N+1)]
    level = [None for _ in range(N+1)]
    level[8]=0
    while queue:
        node=queue.pop(0)
        for neighbour, weight in tree[node]:
            if neighbour not in parent:
                parent[neighbour]=node
                level[neighbour]=level[node]+1 #poziom
                queue.append(neighbour)
    
    

    
    # jaki wierzchołek najlepiej zakorzenić?

    return None









































{"arg": [17, [
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
  ],
  [
    [1, 4, 5],
    [3, 8],
    [6, 9, 10],
    [11, 12, 15],
    [7, 14, 17],
    [13, 16],
  ]],
  "hint": 57},

