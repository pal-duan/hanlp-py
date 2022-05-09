# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:11
# @Author: 2811755762@qq.com
"""
    Description:
    双数组Trie树
"""
# from collection.trie import ITrie
import abc
from collection.trie.Node import DictChildrenNode


# class ITrie(object, metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def build(self, key_value_map: dict) -> int:
#         pass
#
#     @abc.abstractmethod
#     def save(self, out) -> bool:
#         pass
#
#     @abc.abstractmethod
#     def load(self, value) -> bool:
#         pass
#
#     @abc.abstractmethod
#     def get(self, key):
#         pass
#
#     @abc.abstractmethod
#     def get_value_array(self, a):
#         pass
#
#     @abc.abstractmethod
#     def contain_key(self, key: str) -> bool:
#         pass
#
#     @abc.abstractmethod
#     def size(self) -> int:
#         pass
#
#
# class DoubleArrayTrie(ITrie):
#     class Node:
#         def __init__(self):
#             self.code = None
#             self.depth = None
#             self.left = None
#             self.right = None
#
#         def __str__(self):
#             return f"Node{{code={self.code}, depth={self.depth}, left={self.left}, right={self.right}}}"
#
#     def __init__(self):
#         self.check = []
#         self.base = []
#         self.size = 0
#         self.alloc_size = 0  # 无用
#         self.error_ = 0
#         self.key = None
#         self.key_size = None
#         self.length = None
#         self.value = None
#         self.v = None
#         self.progress = None
#         self.next_check_pos = None
#
#     def fetch(self, parent: Node, slblings: list):
#         if self.error_ < 0:
#             return 0
#         prev = 0
#         i = parent.left
#         while i < parent.right:
#             flag = self.length[i] if self.length is not None else len(self.key[i])
#             if flag < parent.depth:
#                 continue
#             tmp = self.key[i]
#             cur = 0
#             if self.length[i] if self.length is not None else len(tmp) != parent.depth:
#                 cur = tmp[parent.depth] + 1
#
#             if prev > cur:
#                 self.error_ = -3
#                 return 0
#
#             if cur != prev or len(slblings) == 0:
#                 tmp_node = self.Node()
#                 tmp_node.depth = parent.depth + 1
#                 tmp_node.code = cur
#                 tmp_node.left = i
#                 if len(slblings) != 0:
#                     slblings[-1].right = i
#                 slblings.append(tmp_node)
#             prev = cur
#             i +=1
#         if len(slblings) != 0:
#             slblings[-1].right = parent.right
#         return len(slblings)
#
#     def insert(self, slblings: list):
#         if self.error_ < 0:
#             return 0
#         begin = 0
#         pos = max(slblings[0].code+1, self.next_check_pos) - 1
#         nonzero_num = 0
#         first = 0
#         if
#
#     def build(self, key_value_map: dict) -> int:
#         assert key_value_map is not None
#         self.key = list(key_value_map.keys())
#         self.v = list(key_value_map.values())
#         self.key_size = len(self.key)
#         self.progress = 0
#         self.base[0] = 1
#         self.next_check_pos = 0
#
#         root_node = self.Node()
#         root_node.left = 0
#         root_node.right = self.key_size
#         root_node.depth = 0
#
#         slblings = []
#         self.fetch(root_node, slblings)
#         self.insert(slblings)
#
#         self.key = None
#         self.length = None
#         return self.error_
#
#
#
#
#
#
#
#
#     def save(self, out) -> bool:
#         pass
#
#     def load(self, value) -> bool:
#         pass
#
#     def get(self, index: int):
#         return self.v[index]
#
#     def get_value_array(self, a):
#         pass
#
#     def contain_key(self, key: str) -> bool:
#         pass
#
#     def size(self) -> int:
#         return len(self.v)


class Node(DictChildrenNode):
    def __init__(self, key, value, parent_node=None, path_to_this=None):
        super().__init__(key, value)
        self.parent_node = parent_node
        self.is_leaf = False
        self.path_to_this = path_to_this

    def is_leaf(self):
        return self.is_leaf

    def add_child(self, node):
        self.children[node.key] = node

    def set_leaf(self):
        self.is_left = True


class TrieHashMap:
    def __init__(self):
        self.root = Node("root", "")

    def add_term(self, element_list):
        current_node = self.root
        parent_path = ""
        for element in element_list:
            if element not in current_node.children:
                current_node.add_child(Node(element, ""))
            current_node = current_node.get_child(element)
            parent_path += element
        current_node.set_leaf()

    def contain_key(self, element_list):
        current_node = self.root



class HashMapTriePlus(TrieHashMap):
    pass


class DoubleArrayTrie:
    pass

if __name__ == "__main__":
    a = DoubleArrayTrie()
    print("test")
