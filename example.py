
from collections import deque
from queue import PriorityQueue
from data import runtests

"""
Jan Martowicz, nr albumu 420112
Opis algorytmu: Poniżej zaimplementowałem aglorytm dynamiczny obliczający maksymalną sumę choronioną przez lordów.
1. Najpierw z podanego grafu tworzę MST, przy pomocy algorytmu kruskala. Krawędzie w takim drzewie to będą jedyne jakie potrzebuję.
2. Obliczone wcześniej drzewo ukorzeniam w jakimś punkcie, w moim algorytmie przyjąłem że jest to wierzchołek 1, ponieważ zakładam że graf ma co
najmniej jeden weirzchołek.
3. Od teraz wierzchołki są reprezentowane jako obiekty klasy Vertex. Vertex posiada informację o rodzicu w drzewie, o dzieciach, o sąsiadach
wraz z wagami krawędzi do nich, o poziomie w drzewie (korzeń ma poziom 0). Zawiera także informację o tym jaki jest dotychczasowy maksymalny wynik
dla podrzewa znajdującego się nie wyżej niż ten wierzchołek (algorytm dynamiczny).
4. Wykorzystuję algorytm bfs do przeanalizowania drzewa
5. Następnie dla każdego lorda obliczam LCA (Lowest Common Ancestor) wszystkich jego wierzchołków. W ten sposób będę wiedział w którym miejscu rozważać wzięcie
lub nie wzięcie tego lorda - właśnie w LCA. Stąd każdy Vertex ma atrybut lords_to_check, czyli przechowuje którym lordów rozważyć w danym wierzchołku.
6. dla każdego lorda obliczam wartość której będzie bronił, jeśli go wybierzemy, oraz wierzchołki, których wyniki musimy wziać pod uwagę jeśli będziemy brać 
danego lorda - będziemy wtedy je sumować. Odpowiedzialna jest za to funkcja count_lord_way
7. Ostatni krok algorytmu polega na przeszukaniu grafu od liści do korzenia (robię to przy pomocy kolejki priorytetowej, priorytetem są poziomy wierzchołków)
Jeśli w danym wierzchołku LCA lorda -> maxresult = max( wartość lorda + suma maxresult wierzchołków sąsiadujących z lordem, suma maxresult dzieci danego wierzchołka)
Jeśli w danym wierzchołku nie rozważamy danego lorda -> maxresult = suma maxresult dzieci danego wierzchołka
Ostatecznym wynikiem jest maxresult korzenia, jako że wtedy przeszliśmy cały graf


"""

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

def kruskal_MST(N,G): #Algorytm Kruskala MST
    G.sort(key=lambda edge: edge[2])
    MST=[]
    nodes=[Kruskal_Node(i) for i in range(N+1)]
    for x,y,w in G:
        if find(nodes[x]) != find(nodes[y]):
            union(nodes[x],nodes[y])
            MST.append((x,y,w))
    return MST

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


def get_LCA(a,b,tree): #funkcja liczy LCA dwóch wierzchołków
    if tree[a].level > tree[b].level:
        a,b=b,a
    while tree[b].level > tree[a].level:

        b=tree[b].parent
    while a!=b:
        b=tree[b].parent
        a=tree[a].parent
    return a

def count_lord_way(tree,lord, lord_lca): #funkcja liczy wartość dróg chronionych przez lorda
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
            
def solve(N,streets,lords):
    MST = kruskal_MST(N,streets) #minimal spanning tree
    tree = [Vertex() for _ in range(N+1)]

    for u,v,w in MST:
        tree[u].add_neighbour(v,w)
        tree[v].add_neighbour(u,w)

    
    #Ukorzenienie drzewa
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
    
    #Analiza lordów (LCA, sąsiadujące wierzchołki)
    l=len(lords)
    lord_value = [0 for _ in range(l)] #wartości dla każdego lorda
    lord_dots = [[] for _ in range(l)] #wierzchołki sąsiadujące z lordem
    for i in range(l):
        
        fortresses=lords[i]
        n=len(fortresses)
        if n<=1:
            continue
        lord_LCA = get_LCA(fortresses[0],fortresses[1],tree)
        for j in range(2,n):
            lord_LCA = get_LCA(lord_LCA,fortresses[j],tree)
            
        tree[lord_LCA].lords_to_check.append(i)
        lord_value[i],lord_dots[i]= count_lord_way(tree, lords[i], lord_LCA)
    

    #Ostateczne, przeszukanie grafu, aktualizacja .maxresult dla każdego wierzchołka
    m=len(tree)
    p = PriorityQueue()
    included = [False for _ in  range(m)]
    for i in range(1,m): #wierzchołki indeksowane od 1, wrzucam liście do kolejki
        if len(tree[i].children)==0:
            p.put((-tree[i].level, i))
            included[i]=True


    l,v=p.get() #wyciągam element z kolejki
    while v is not None: 
        if len(tree[v].lords_to_check)>0: #jęsli sprawdzam w tym wierzchołku lorda
            
            for lord in tree[v].lords_to_check:
                res=lord_value[lord]
                for vertex in lord_dots[lord]:
                    res+=tree[vertex].maxresult
                tree[v].maxresult=max(tree[v].maxresult,res)

        sum_children=0
        for child in tree[v].children: #sumuję .maxresult wszystkich dzieci
            sum_children += tree[child].maxresult
        tree[v].maxresult = max(tree[v].maxresult,sum_children)
        next_v=tree[v].parent
        if next_v==None: #jeśli jestem aktualnie w korzeniu, to wrzucam do kolejki wartość None, aby zakończyć pętle
            p.put((1,next_v))
        elif not included[next_v]:
            p.put((-tree[next_v].level, next_v))
            included[next_v]=True
        l,v=p.get() #wyciągam element z kolejki

    return tree[1].maxresult #zwracam maxresult po przeszukaniu całego grafu


  
runtests(solve)



    
