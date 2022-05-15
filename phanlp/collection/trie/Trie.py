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

    def build(self, data: dict):
        for key, value in data.items():
            self[key] = value


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
    import time
    import re
    import psutil
    import os

    pid = os.getpid()
    p = psutil.Process(pid)
    info_start = p.memory_full_info().uss / 1024

    start = time.time()
    # trie = DCTrie()
    # data = {}
    # with open("D:\\模型\\hanlp-py\\data\\dictionary\\CoreNatureDictionary.txt", "r", encoding="utf-8") as f:
    #     for line in f:
    #         s = re.split(r"\s", line.strip())
    #         data[s[0]] = "-".join(s[1:])
    # print(f"加载文件耗时：{time.time() - start}")
    # start_2 = time.time()
    # trie.build(data)
    # print(f"构建DCTrie耗时：{time.time() - start_2}")
    # start_1 = time.time()
    # for k, v in data.items():
    #     if k not in trie:
    #         print(k)
    #     else:
    #         assert v == trie[k]
    # print(f"遍历DCTrie耗时：{time.time() - start_1}")
    # print(f"总耗时：{time.time() - start}")


    # trie = LCTrie()
    # data = {}
    # with open("D:\\模型\\hanlp-py\\data\\dictionary\\CoreNatureDictionary.txt", "r", encoding="utf-8") as f:
    #     for line in f:
    #         s = re.split(r"\s", line.strip())
    #         data[s[0]] = "-".join(s[1:])
    # print(f"加载文件耗时：{time.time() - start}")
    # start_2 = time.time()
    # trie.build(data)
    # print(f"构建LCTrie耗时：{time.time() - start_2}")
    # start_1 = time.time()
    # for k, v in data.items():
    #     if k not in trie:
    #         print(k)
    #     else:
    #         assert v == trie[k]
    # print(f"遍历LCTrie耗时：{time.time() - start_1}")
    # print(f"总耗时：{time.time() - start}")

    trie = DCLCTrie()
    data = {}
    with open("D:\\模型\\hanlp-py\\data\\dictionary\\CoreNatureDictionary.txt", "r", encoding="utf-8") as f:
        for line in f:
            s = re.split(r"\s", line.strip())
            data[s[0]] = "-".join(s[1:])
    print(f"加载文件耗时：{time.time() - start}")
    start_2 = time.time()
    trie.build(data)
    print(f"构建DCLCTrie耗时：{time.time() - start_2}")
    start_1 = time.time()
    for k, v in data.items():
        if k not in trie:
            print(k)
        else:
            assert v == trie[k]
    print(f"遍历DCLCTrie耗时：{time.time() - start_1}")
    print(f"总耗时：{time.time() - start}")

    info_end = p.memory_full_info().uss / 1024
    print(f"程序占用了内存{info_end - info_start}KB")
