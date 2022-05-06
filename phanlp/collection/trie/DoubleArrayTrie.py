# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:11
# @Author: 2811755762@qq.com
"""
    Description:
    双数组Trie树
"""
# from collection.trie import ITrie
import abc


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

    def __init__(self):
        self.check = []
        self.base = []
        self.size = 0
        self.alloc_size = 0  # 无用
        self.error_ = 0
        self.key = None
        self.key_size = None
        self.length = None
        self.value = None
        self.v = None
        self.progress = None
        self.next_check_pos = None

    def fetch(self, parent: Node, slblings: list):
        pass

    def insert(self, slblings: list):
        pass

    def build(self, key_value_map: dict) -> int:
        assert key_value_map is not None
        self.key = list(key_value_map.keys())
        self.v = list(key_value_map.values())
        self.key_size = len(self.key)
        self.progress = 0
        self.base[0] = 1
        self.next_check_pos = 0

        root_node = self.Node()
        root_node.left = 0
        root_node.right = self.key_size
        root_node.depth = 0

        slblings = []
        self.fetch(root_node, slblings)
        self.insert(slblings)

        self.key = None
        self.length = None
        return self.error_








    def save(self, out) -> bool:
        pass

    def load(self, value) -> bool:
        pass

    def get(self, index: int):
        return self.v[index]

    def get_value_array(self, a):
        pass

    def contain_key(self, key: str) -> bool:
        pass

    def size(self) -> int:
        return len(self.v)


if __name__ == "__main__":
    a = DoubleArrayTrie()
    print("test")
