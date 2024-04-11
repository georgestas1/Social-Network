import heapq

class Graph:
    def __init__(self):
        self.vertices = {}
        self.directed = False
        self.path = ''

    def add_vertex(self, id, data=None):
        if id in self.vertices:
            print("Vertex already in graph")
        else:
            vertex = Vertex(id, data)
            self.vertices[id] = vertex

    def add_edge(self, ida, idb, weight=1):
        if ida in self.vertices and idb in self.vertices:
            edge = Edge(idb, weight)
            self.vertices[ida].add_edge(idb, edge)
            if not self.directed:
                edge = Edge(ida, weight)
                self.vertices[idb].add_edge(ida, edge)

    def get_weight(self, ida, idb):
        if ida in self.vertices and idb in self.vertices:
            if idb in self.vertices[ida].edges:
                return self.vertices[ida].edges[idb].weight
        return 0

    def set_weight(self, ida, idb, weight):
        if ida in self.vertices and idb in self.vertices:
            if idb in self.vertices[ida].edges:
                self.vertices[ida].edges[idb].weight = weight
            if not self.directed and ida in self.vertices[idb].edges:
                self.vertices[idb].edges[ida].weight = weight

    def get_number_of_edges(self, name):
        if name in self.vertices:
            return len(self.vertices[name].edges)
        return 0

    def display_number_of_edges(self):
        for v in self.vertices:
            print(v, end=': ')
            print(len(self.vertices[v].edges))

    def display_edges(self):
        for v in self.vertices:
            print(v, end=': ')
            print('Edges: ', end='')
            for e in self.vertices[v].edges:
                edge = self.vertices[v].edges[e]
                print('[', e, edge.weight, '] ', end='')
            print()

    def get_edges(self, id):
        if id in self.vertices:
            return self.vertices[id].edges
        return None

    def relax(self, va, vb, w):
        if vb.distance > va.distance + w:
            vb.distance = va.distance + w
            vb.parent = va

    def dijkstra(self, start):
        for v in self.vertices:
            self.vertices[v].init_bfs()
        self.vertices[start].distance = 0
        Q = []
        for vertex in self.vertices:
            Q.append(self.vertices[vertex])
        Q.sort(key=lambda x: x.distance)
        while len(Q) > 0:
            u = Q.pop(0)
            for e in u.edges:
                v = self.vertices[e]
                w = u.edges[e].weight
                self.relax(u, v, w)
            Q.sort(key=lambda x: x.distance)

    def print_shortest_path(self, start, dest):
        start_vertex = self.vertices[start]
        dest_vertex = self.vertices[dest]
        if dest_vertex.parent is not None:
            self.print_shortest_path(start, dest_vertex.parent.id)
        elif dest != start:
            self.path = "No path from start to dest"
            return
        self.path += str(dest) + ' ' 

    def bfs(self, start):
        if start not in self.vertices:
            print("Starting vertex not found")
            return
        for v in self.vertices:
            self.vertices[v].init_bfs()
        queue = []
        queue.append(self.vertices[start])
        self.vertices[start].color = 'gray'
        self.vertices[start].distance = 0
        while len(queue) > 0:
            vertex = queue.pop(0)
            for e in vertex.edges:
                did = vertex.edges[e].destination
                destination = self.vertices[did]
                if destination.color == 'white':
                    destination.color = 'gray'
                    destination.parent = vertex
                    destination.distance = vertex.distance + 1
                    queue.append(destination)
            vertex.color = 'black'


class Vertex:
    def __init__(self, id, data=None):
        self.id = id
        self.edges = {}
        self.data = data
        self.distance = float('inf')
        self.parent = None

    def add_edge(self, idb, edge):
        self.edges[idb] = edge

    def init_bfs(self):
        self.distance = float('inf')
        self.color = 'white'
        self.parent = None


class Edge:
    def __init__(self, destination, weight=1):
        self.destination = destination
        self.weight = weight


if __name__ == '__main__':
    g = Graph()
    g.directed = True
    vertices = ['A', 'B', 'C', 'D', 'G', 'F', 'H', 'J', 'K', 'X']
    for v in vertices:
        g.add_vertex(v)
    g.add_edge('A', 'B', 3)
    g.add_edge('A', 'C', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'G', 7)
    g.add_edge('C', 'F', 1)
    g.add_edge('G', 'H', 3)
    g.add_edge('G', 'F', 4)
    g.add_edge('F', 'H', 2)
    g.add_edge('F', 'J', 6)
    g.add_edge('H', 'D', 3)
    g.add_edge('H', 'J', 5)
    g.add_edge('D', 'K', 6)
    g.add_edge('D', 'J', 2)
    g.add_edge('D', 'H', 2)
    g.add_edge('J', 'K', 2)
    g.dijkstra('A')
    g.print_shortest_path('A', 'K')
    print(g.path)
