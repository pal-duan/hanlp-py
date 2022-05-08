# -*- coding: utf-8 -*-
# @Time: 2022/5/7  10:40
# @Author: 2811755762@qq.com
from collection.trie.Node import DictChildrenNode, ListChildrenNode


class DCTrie(DictChildrenNode):
    def __init__(self):
        super().__init__()
        self.size = 0

    def __getitem__(self, key):
        state = self
        for char in key:
            state = state.children.get(char)
            if state is None:
                return None
        if not (state.status == self.StatusEnum.WORD_END_3 or state.status == self.StatusEnum.WORD_MIDDLE_2):
            return None
        return state.get_value()

    def __setitem__(self, key, value):
        if not key:
            return
        state = self
        for i, char in enumerate(key[:-1]):
            state.add_child(DictChildrenNode(char, None, self.StatusEnum.NOT_WORD_1))
            state = state.get_child(char)
        if state.add_child(DictChildrenNode(key[-1], value, self.StatusEnum.WORD_END_3)):
            self.size += 1

    def __delitem__(self, key):
        if not key:
            return
        state = self
        if key not in state:
            return
        if state.add_child(DictChildrenNode(key[-1], None, self.StatusEnum.UNDEFINED_0)):
            self.size -= 1

    def __contains__(self, item: str):
        return self[item] is not None

    def get(self, key):
        return self[key]

    def set(self, key, value):
        self[key] = value

    def remove(self, key):
        del self[key]



class LCTrie(ListChildrenNode):
    pass


if __name__ == "__main__":
    trie = DCTrie()
    trie["自然"] = "nature"
    trie["自然"] = "NATURE"
    trie["自然人"] = "human"
    trie["自然语言"] = "language"
    trie["自语"] = "talk to oneself"
    trie["入门"] = "introduction"
    del trie["自然"]
    print(trie.size)
    print(trie["自然语"])