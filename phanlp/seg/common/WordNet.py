

from seg.common.Vertex import Vertex


class WordNet:
    def __init__(self, sentence, vertex_list=None):
        self.sentence = sentence
        self.char_array = sentence  # 原始句子对应的数组
        self.vertexes = [[] for _ in range(len(self.char_array)+2)]  # 节点，每一行都是前缀词，跟图的表示方式不同
        if vertex_list is not None:
            i = 0
            for vertex in vertex_list:
                self.vertexes[i].append(vertex)
                self.size += 1
                i += len(vertex.real_word)
        else:
            self.vertexes[0].append(Vertex.new_b())
            self.vertexes[len(self.vertexes)-1].append(Vertex.new_e())
            self.size = 2  # 共有多少个节点

    def add(self, line, vertex):
        for old_vertex in self.vertexes[line]:
            if len(old_vertex.real_word) == len(vertex.real_word):
                return
        self.vertexes[line].append(vertex)
        self.size += 1

    def insert(self, line, vertex, word_net_all):
        for old_vertex in self.vertexes[line]:
            if len(old_vertex.real_word) == len(vertex.real_word):
                return
        self.vertexes[line].append(vertex)
        self.size += 1
        start = max(0, line-5)
        for l in range(line-1, start, -1):
            _all = word_net_all.get(l)
            if _all.size() <= self.vertexes[l].size():
                continue
            for pre in _all:
                if len(pre) + l == line:
                    self.vertexes[l].append(pre)
                    self.size += 1
        l = line + len(vertex.real_word)
        target_line = word_net_all.get(l)
        if self.vertexes[l].size() == 0 and target_line.size() != 0:
            self.size += target_line.size()
            self.vertexes[l] = target_line

    def add_all(self, vertex_list):
        i = 0
        for vertex in vertex_list:
            self.add(i, vertex)
            i += len(vertex.real_word)

    def get(self, line, length=None):
        if length is not None:
            for vertex in self.vertexes[line]:
                if len(vertex.real_word) == length:
                    return vertex
            return None
        else:
            return self.vertexes[line]

    def descending_iterator(self, line):
        for i in self.vertexes[line][::-1]:
            yield i

    def add_atom(self, line, atom_segment):
        pass







