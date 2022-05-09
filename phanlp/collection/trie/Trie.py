# -*- coding: utf-8 -*-
# @Time: 2022/5/7  10:40
# @Author: 2811755762@qq.com
import abc
from collection.trie.Node import DictChildrenNode, ListChildrenNode, BaseNode


class BaseTrie(metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
        self.size = 0

    def __getitem__(self, key):
        state = self
        for char in key:
            state = state.get_child(char)
            if state is None:
                return None
        if not (state.status == BaseNode.StatusEnum.WORD_END_3 or state.status == BaseNode.StatusEnum.WORD_MIDDLE_2):
            return None
        return state.get_value()

    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass

    @abc.abstractmethod
    def __delitem__(self, key):
        pass

    def __contains__(self, item: str):
        return self[item] is not None

    def get(self, key):
        return self[key]

    def set(self, key, value):
        self[key] = value

    def remove(self, key):
        del self[key]


class DCTrie(DictChildrenNode, BaseTrie):
    def __init__(self):
        print(super())
        super().__init__()

    def __setitem__(self, key, value):
        if not key:
            return
        state = self
        for i, char in enumerate(key[:-1]):
            state.add_child(DictChildrenNode(char, None, BaseNode.StatusEnum.NOT_WORD_1))
            state = state.get_child(char)
        if state.add_child(DictChildrenNode(key[-1], value, BaseNode.StatusEnum.WORD_END_3)):
            self.size += 1

    def __delitem__(self, key):
        if not key:
            return
        state = self
        for char in key[:-1]:
            state = state.get_child(char)
            if state is None:
                return None
        if state.add_child(DictChildrenNode(key[-1], None, BaseNode.StatusEnum.UNDEFINED_0)):
            self.size -= 1

    def __str__(self):
        return f"DCTrie{{status={self.status}, key={self.key}, value={self.value}, " \
               f"children={len(self.children)}, size={self.size}}}"


class LCTrie(ListChildrenNode, BaseTrie):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        if not key:
            return
        state = self
        for i, char in enumerate(key[:-1]):
            state.add_child(ListChildrenNode(char, None, self.StatusEnum.NOT_WORD_1))
            state = state.get_child(char)
        if state.add_child(ListChildrenNode(key[-1], value, self.StatusEnum.WORD_END_3)):
            self.size += 1

    def __delitem__(self, key):
        if not key:
            return
        state = self
        for char in key[:-1]:
            state = state.get_child(char)
            if state is None:
                return None
        if state.add_child(ListChildrenNode(key[-1], None, self.StatusEnum.UNDEFINED_0)):
            self.size -= 1

    def __str__(self):
        return f"LCTrie{{status={self.status}, key={self.key}, value={self.value}, " \
               f"children={len(self.children)}, size={self.size}}}"


class DCLCTrie(DictChildrenNode, BaseTrie):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        if not key:
            return
        state = self
        for i, char in enumerate(key[:-1]):
            state.add_child(ListChildrenNode(char, None, self.StatusEnum.NOT_WORD_1))
            state = state.get_child(char)
        if state.add_child(ListChildrenNode(key[-1], value, self.StatusEnum.WORD_END_3)):
            self.size += 1

    def __delitem__(self, key):
        if not key:
            return
        state = self
        for char in key[:-1]:
            state = state.get_child(char)
            if state is None:
                return None
        if state.add_child(ListChildrenNode(key[-1], None, self.StatusEnum.UNDEFINED_0)):
            self.size -= 1

    def __str__(self):
        return f"DCLCTrie{{status={self.status}, key={self.key}, value={self.value}, " \
               f"children={len(self.children)}, size={self.size}}}"


if __name__ == "__main__":
    print(DCTrie.__mro__)
    trie = DCLCTrie()
    trie["自然"] = "nature"
    trie["自然"] = "NATURE"
    trie["自然人"] = "human"
    trie["自然语言"] = "language"
    trie["自语"] = "talk to oneself"
    trie["入门"] = "introduction"
    print(trie.size)
    del trie["自然"]
    print(trie.size)
    print(trie["自然语"])