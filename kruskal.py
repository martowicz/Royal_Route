class Kruskal_Node:
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


def kruskal_MST(N,G): #graf w postaci listy krawędzi
    G.sort(key=lambda edge: edge[2]) #F=sorted(G, key=lambda egde: egde[2])
    #G.reverse()
    MST=[]
    nodes=[Kruskal_Node(i) for i in range(N+1)]
    for x,y,w in G:
        #Jeśli dodatkowa krawędź z tymi co już są nie tworzy cyklu, to ją dodaję
        if find(nodes[x]) != find(nodes[y]):
            union(nodes[x],nodes[y])
            MST.append((x,y,w))
    return MST