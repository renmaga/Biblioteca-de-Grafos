# -*- coding: utf-8 -*-
"""Proyecto_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DO6z3EV4X1nfUYf9hyqbRJ16kqvD_hx8

# Biblioteca de generación y manejo de grafos

Biblioteca orientada a objetos, para describir y utilizar grafos.
"""

import random
import numpy as np
import math as mt

generated_graphs = []

"""## Clases

### Nodo
"""

class Node:
    def __init__(self, name , x = 0, y = 0, deg = 0):
        self.Name = name
        self.x_coord = x
        self.y_coord = y
        self.Degree = deg

    def node_name(self):
        return self.Name

    def node_deg(self):
        return self.Degree

    def add_degree(self):
        self.Degree = self.Degree + 1

"""### Arista"""

class Edge:
    def __init__(self, ini, fin, w = 0):
        self.Initial = ini
        self.Final = fin
        self.Weight = w

    def edge_initial(self):
        return self.Initial.node_name()
    def edge_final(self):
        return self.Final.node_name()
    def edge_nodes(self):
        return [self.Intitial,self.Final]

"""### Grafo"""

class Graph:
    def __init__(self, name, gtype = "graph"):
        self.Name = name
        self.Nodes = []
        self.Edges = []
        self.Gtype = gtype

    # Nodos
    def new_nodes(self, node_list):
        self.Nodes.extend(node_list)
    def get_nodes(self):
        return self.Nodes

    # aristas    
    def new_edges(self, edge_list):
        self.Edges.extend(edge_list)
    def get_edges(self):
        return self.Edges

# Función de exportado
    def save_graph(self, file_name):
        infile = self.Gtype + " " + self.Name + " {\n"

        # guarda nodos
        for i in range(len(self.Nodes)):
            infile += str(self.Nodes[i].Name) + ";\n"
        
        # tipo de arista
        if self.Gtype == "graph":
            edge_type = " -- "
        else:
            edge_type = " -> "
        # guarda aristas
        for j in range(len(self.Edges)):
            infile += str(self.Edges[j].Initial) + edge_type + str(self.Edges[j].Final) + ";\n"
        infile += "}"
        
        with open(file_name + '.gv', 'w') as outfile:
            outfile.write(infile)

"""## Modelos

### Malla
"""

def Grid(n, m, name, directed = False):
    Nodes = []
    Edges = []

    # genera nodos
    for j in range(m):
        for i in range(n): 
            Nodes.append(Node(i, x = i, y = j))

    # genera aristas
    for j in range(m - 1):
        for i in range(n - 1):
            Edges.append(Edge(i + n*j, i + n*j + 1))
            Edges.append(Edge(i + n*j, i + n*j + n))
    # orillas
    for i in range(m - 1):
        Edges.append(Edge(n - 1 + i*n, 2*n - 1 + i*n))
    for i in range(n-1):
        Edges.append(Edge(n*(m - 1) + i, n*(m - 1) + i + 1))

    if directed:
        new_graph = Graph(name, gtype = "digraph")
    else:
        new_graph = Graph(name)
    new_graph.new_nodes(Nodes)
    new_graph.new_edges(Edges)

    return new_graph

generated_graphs.append(Grid(3, 10, "Malla_30"))
generated_graphs.append(Grid(10, 10, "Malla_100"))
generated_graphs.append(Grid(20, 25, "Malla_500"))



"""### Erdös-Renyi"""

def Erdos_Renyi(n, m, name, directed = False, auto = False):
    matrix = np.zeros((n,n), dtype = int)    
    Nodes = []
    Edges = []

    # generando nodos
    for i in range(n):
        Nodes.append(Node(i))
    
    # generando aristas
    for i in range(m):  
        while True:    
            ini = random.randint(0, n - 1)
            fin = random.randint(0, n - 1)

            if ( (ini!=fin) or auto ) and matrix[ini][fin] == 0:
                break

        matrix[ini][fin] = 1

        Edges.append(Edge(ini,fin))
        if not directed:
            matrix[fin][ini] = 1
    
    if directed:
        new_graph = Graph(name, gtype = "digraph")
    else:
        new_graph = Graph(name)
    new_graph.new_nodes(Nodes)
    new_graph.new_edges(Edges)

    return new_graph

generated_graphs.append(Erdos_Renyi(30, 50, "E-R_30_m50"))
generated_graphs.append(Erdos_Renyi(100, 200, "E-R_100_m200"))
generated_graphs.append(Erdos_Renyi(500, 1000, "E-R_500_m1000"))

"""### Gilbert"""

def Gilbert(n, p, name, directed = False, auto = False):  
    Nodes = []
    Edges = []

    # generando n nodos
    for i in range(n):
        Nodes.append(Node(i))

    # generando aristas  
    lim = n + auto - 1

    for i in range(n):
        if not directed:
            lim = i + auto

        for j in range(lim):
            if random.random() <= p: # checa probabilidad
                if auto or (not i == j):
                    Edges.append(Edge(i, j))

    if directed:
        new_graph = Graph(name, gtype = "digraph")
    else:
        new_graph = Graph(name)
        
    new_graph.new_nodes(Nodes)
    new_graph.new_edges(Edges)

    return new_graph

generated_graphs.append(Gilbert(30,.5,"Gilbert_30_p50"))
generated_graphs.append(Gilbert(100,.3,"Gilbert_100_p30"))
generated_graphs.append(Gilbert(500,.2,"Gilbert_500_p20"))

"""### Geográfico Simple"""

def distance(x1, y1, x2, y2):
    dis = mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dis

def Simple_Geo(n, r, name,directed = False, auto = False):    
    Nodes=[]
    Edges=[]

    xvector = []
    yvector = []
    
    # nodos
    for i in range (n):
        x_i = random.random()
        xvector.append(x_i)

        y_i = random.random()
        yvector.append(y_i)

        Nodes.append(Node(i, x = x_i, y = y_i))

    # aristas
    for i in range(n):
        for j in range(n - i - 1 + auto):
            distan = distance(xvector[i], yvector[i], xvector[n - j - 1], yvector[n - j - 1])
            if distan < r:
                Edges.append(Edge(i, n - j - 1, w = distan))
    
    new_graph = Graph(name)
    new_graph.new_nodes(Nodes)
    new_graph.new_edges(Edges)

    return new_graph

generated_graphs.append(Simple_Geo(30,.2,"Geo_30_r2"))
generated_graphs.append(Simple_Geo(100,.4,"Geo_100_r4"))
generated_graphs.append(Simple_Geo(500,.7,"Geo_500_r7"))

"""### Barbasi Albert"""

def Barabasi_Albert(n, d, name, directed = False, auto = False):    
    Nodes=[]
    Edges=[]
    n_list = []

    # nodos
    for i in range(n): 
        Nodes.append(Node(i))
        n_list.append(0)

        # comparando con nodos existentes
        for j in range (0, i): 
            p = 1 - n_list[j] / d

            if random.random() < p:
                Edges.append(Edge(i, j))

                n_list[i] += 1
                n_list[j] += 1
                Nodes[i].add_degree()
                Nodes[j].add_degree()

    if directed:
        new_graph = Graph(name, gtype = "digraph")
    else:
        new_graph = Graph(name)

    new_graph.new_nodes(Nodes)
    new_graph.new_edges(Edges)

    return new_graph

generated_graphs.append(Barabasi_Albert(30,5,"B-A_30_5"))
generated_graphs.append(Barabasi_Albert(100,3,"B-A_100_3"))
generated_graphs.append(Barabasi_Albert(500,10,"B-A_500_10"))

"""### Dorogovtsev-Mendes"""

def Dorogovtsev_Mendes(n, name, directed = False):
    Nodes=[]
    Edges=[]

    #Primeros tres nodos    
    for i in range(3):
        Nodes.append(Node(i))

    vertex_l = [0, 1, 2]
    
    # primeras 3 aristas
    Edges.append(Edge(0, 1))
    Edges.append(Edge(1, 2))
    Edges.append(Edge(2, 0))

    edge_l = [[0, 1], [1, 2], [2, 0]]
    
    # nodos
    for i in range(n - 3):
        Nodes.append(Node(i + 3))
        vertex_l.append(i + 3)
    # aristas
        select = random.randint(0, len(edge_l) - 1)

        edge_l.append([i + 3, edge_l[select][0]])
        edge_l.append([i + 3, edge_l[select][1]])
        
        Edges.append(Edge(i + 3, edge_l[select][0]))
        Edges.append(Edge(i + 3, edge_l[select][1]))
    
    if directed:
        new_graph = Graph(name, gtype = "digraph")
    else:
        new_graph = Graph(name)
        
    new_graph.new_nodes(Nodes)
    new_graph.new_edges(Edges)

    return new_graph

generated_graphs.append(Dorogovtsev_Mendes(30,"D-Mendes_30"))
generated_graphs.append(Dorogovtsev_Mendes(100,"D-Mendes_100"))
generated_graphs.append(Dorogovtsev_Mendes(500,"D-Mendes_500"))

"""## Archivos"""

for i in range(len(generated_graphs)):
    generated_graphs[i].save_graph(generated_graphs[i].Name)