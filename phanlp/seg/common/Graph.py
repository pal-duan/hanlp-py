



class Graph:
    def __init__(self, vertexes):
        size = len(vertexes)
        self.vertexes = vertexes
        self.edges_to = [[] for _ in range(size)]

    def get_vertexes(self):
        return self.vertexes

    def get_edges_to(self):
        return self.edges_to

    def connect(self, _from, to, weight):
        self.edges_to[to].append(EdgeFrom())
