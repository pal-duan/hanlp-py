# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:11
# @Author: 2811755762@qq.com
"""
    Description:
    双数组Trie树
"""
# from collection.trie import ITrie
import abc
from utility.TreeMap import to_treemap
from collection.trie.Node import DictChildrenNode


class ITrie(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build(self, key_value_map: dict) -> int:
        pass

    @abc.abstractmethod
    def save(self, out) -> bool:
        pass

    @abc.abstractmethod
    def load(self, value) -> bool:
        pass

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def get_value_array(self, a):
        pass

    @abc.abstractmethod
    def contain_key(self, key: str) -> bool:
        pass

    @abc.abstractmethod
    def size(self) -> int:
        pass


class DoubleArrayTrie(ITrie):
    class Node:
        def __init__(self):
            self.code = None
            self.depth = None
            self.left = None
            self.right = None

        def __str__(self):
            return f"Node{{code={self.code}, depth={self.depth}, left={self.left}, right={self.right}}}"

    def __init__(self, data: dict = None):
        self.check = []
        self.base = []
        self.size = 0
        self.alloc_size = 0
        self.error_ = 0
        self.key = None
        self.key_size = None
        self.length = None
        self.value = None
        self.v = None
        self.progress = 0
        self.next_check_pos = 0
        self.max_code = 0
        self.min_code = 0
        if data is not None:
            self.data = to_treemap(data)
            # data = dict(sorted(data.items(), key=lambda x: x[0]))
            self.build(self.data)

    def fetch(self, parent: Node, slblings: list):
        if self.error_ < 0:
            return 0
        prev = 0
        for i in range(parent.left, parent.right):
            flag = self.length[i] if self.length is not None else len(self.key[i])
            if flag < parent.depth:
                continue
            tmp = self.key[i]
            cur = 0
            if (self.length[i] if self.length is not None else len(tmp)) != parent.depth:
                cur = ord(tmp[parent.depth]) + 1

            if prev > cur:
                self.error_ = -3
                return 0

            if cur != prev or len(slblings) == 0:
                tmp_node = self.Node()
                tmp_node.depth = parent.depth + 1
                tmp_node.code = cur
                tmp_node.left = i
                if len(slblings) != 0:
                    slblings[-1].right = i
                slblings.append(tmp_node)
            prev = cur
        if len(slblings) != 0:
            slblings[-1].right = parent.right
        return len(slblings)

    def insert(self, siblings: list, used):
        if self.error_ < 0:
            return 0
        begin = 0
        pos = max(siblings[0].code+1, self.next_check_pos) - 1
        nonzero_num = 0
        first = 0
        if self.alloc_size <= pos:
            self.resize(pos+1)

        while True:
            pos += 1
            if self.alloc_size <= pos:
                self.resize(pos+1)
            if self.check[pos] != 0:
                nonzero_num += 1
                continue
            elif first == 0:
                self.next_check_pos = pos
                first = 1

            begin = pos - siblings[0].code
            if self.alloc_size <= (begin + siblings[len(siblings)-1].code):
                self.resize(begin+siblings[len(siblings)-1].code)

            if begin in used:
                continue

            for i in range(1, len(siblings)):
                if self.check[begin+siblings[i].code] != 0:
                    break
            else:
                break

        if nonzero_num / (pos - self.next_check_pos + 1) >= 0.95:
            self.next_check_pos = pos

        used.add(begin)

        self.size = self.size if self.size > (begin + siblings[len(siblings)-1].code+1) else begin + siblings[len(siblings)-1].code + 1

        for i in range(len(siblings)):
            self.check[begin+siblings[i].code] = begin

        for i in range(len(siblings)):
            new_siblings = []
            if self.fetch(siblings[i], new_siblings) == 0:
                self.base[begin+siblings[i].code] = (-self.value[siblings[i].left-1]) if self.value is not None else (-siblings[i].left-1)
                if self.value is not None and (-self.value[siblings[i].left]-1) >= 0:
                    self.error_ = -2
                    return 0
                self.progress += 1
            else:
                h = self.insert(new_siblings, used)
                self.base[begin + siblings[i].code] = h
        return begin

    def build(self, key_value_map: dict) -> int:
        assert key_value_map is not None
        self.key = list(key_value_map.keys())
        self.v = list(key_value_map.values())
        # self.length = [len(k) for k in self.key]
        self.key_size = len(self.key)
        # self.resize(self.get_max_code(self.key))
        self.resize(65536*32)
        self.base[0] = 1
        self.next_check_pos = 0

        root_node = self.Node()
        root_node.left = 0
        root_node.right = self.key_size
        root_node.depth = 0

        siblings = []
        self.fetch(root_node, siblings)
        self.insert(siblings, set())

        self.key = None
        self.length = None
        return self.error_

    def resize(self, new_size):
        self.base += [0] * (new_size - len(self.base))
        self.check += [0] * (new_size - len(self.check))
        self.alloc_size = len(self.base)

    def get_max_code(self, key_list=None):
        key_list = self.key if key_list is None else key_list
        for key in key_list:
            for char in key:
                if ord(char) > self.max_code:
                    self.max_code = ord(char)
                if ord(char) < self.min_code:
                    self.min_code = ord(char)
        return self.max_code

    def exact_match_search(self, key: str, pos: int = 0, length: int = 0, node_pos: int = 0) -> int:
        if length <= 0:
            length = len(key)
        if node_pos <= 0:
            node_pos = 0
        result = -1
        b = self.base[node_pos]
        for i in range(pos, length):
            p = b + ord(key[i]) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return result

        p = b
        n = self.base[p]
        if b == self.check[p] and n < 0:
            result = -n - 1
        return result

    def save(self, out) -> bool:
        pass

    def load(self, value) -> bool:
        pass

    def get(self, index: int):
        return self.v[index]

    def get_value_array(self, a):
        pass

    def contain_key(self, key: str) -> bool:
        return self.exact_match_search(key) >= 0

    def size(self) -> int:
        return len(self.v)


if __name__ == "__main__":
    import time
    import re
    data = {}
    start = time.time()
    with open("D:\\project\\hanlp-py\\data\\dictionary\\CoreNatureDictionary.txt", "r", encoding="utf-8") as f:
        for line in f:
            s = re.split(r"\s", line.strip())
            # s = line.strip().split("\t")
            data[s[0]] = "-".join(s[1:])
    print(f"文件读取耗时：{time.time()-start}")
    start_1 = time.time()
    a = DoubleArrayTrie(data)
    print(f"构建双数组字典树耗时：{time.time()-start_1}")
    start_2 = time.time()
    err = []
    for key in a.data.keys():
        f = a.contain_key(key)
        if not f:
            err.append(key)
    print(err)
    print(len(err))
    print(f"遍历双数组字典树耗时：{time.time()-start_2}")
    # print("test")
    # print(a.size)
    # print(a.key_size)
    # print(a.alloc_size)
    # print(a.max_code)
    # print(a.progress)
    print(time.time() - start)
