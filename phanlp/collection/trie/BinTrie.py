

from collection.trie.Trie import BaseTrie
from collection.trie.Node import ListChildrenNode
from algorithm.pytreemap import TreeSet


def char_hash(key: str, length: int = 5) -> int:
    # return abs(hash(key)) % (10 ** length)
    return ord(key)


class BinTrie(ListChildrenNode, BaseTrie):
    def __init__(self):
        super().__init__()
        self.children = [None] * 100000

    def get_child(self, char):
        a = char_hash(char)
        return self.children[a]

    def add_child(self, node):
        add = False
        target = self.children[char_hash(node.key)]
        if target is None:
            self.children[char_hash(node.key)] = node
            add = True
        else:
            add = target.change_child(node)
        return add

    def __setitem__(self, key, value):
        if not key:
            return
        state = self
        for i, char in enumerate(key):
            if i == 0:
                if i < len(key) - 1:
                    target = state.children[char_hash(char)]
                    if target is None:
                        node = ListChildrenNode(char, None, self.StatusEnum.NOT_WORD_1)
                        state.children[char_hash(char)] = node
                        state = node
                    else:
                        state = target
                else:
                    node = ListChildrenNode(char, value, self.StatusEnum.WORD_END_3)
                    state.children[char_hash(char)] = node
                    state = node
                    self.size += 1
            else:
                if i < len(key) - 1:
                    state.add_child(ListChildrenNode(char, None, self.StatusEnum.NOT_WORD_1))
                    state = state.get_child(char)
                else:
                    if state.add_child(ListChildrenNode(char, value, self.StatusEnum.WORD_END_3)):
                        self.size += 1
                    state = state.get_child(char)

    def __delitem__(self, key):
        if not key:
            return
        state = self
        if key not in state:
            return
        if len(key) == 1:
            state = state.children[char_hash(key[0])]
            state.value = None
            state.state = self.StatusEnum.NOT_WORD_1
            self.size -= 1
        for char in key[:-1]:
            state = state.get_child(char)
            if state is None:
                return None
        if state.add_child(ListChildrenNode(key[-1], None, self.StatusEnum.UNDEFINED_0)):
            self.size -= 1

    def prefix_search(self, key):
        """
        前缀查询
        :param key:
        :return:
        """
        entry_set = TreeSet()
        branch = self
        for char in key:
            if branch is None:
                return entry_set
            branch = branch.get_child(char)
        if branch is None:
            return entry_set
        branch.walk(key, entry_set)
        return entry_set

    def entry_set(self):
        entry_set = TreeSet()
        for node in self.children:
            if node is None:
                continue
            node.walk("", entry_set)
        return entry_set


if __name__ == "__main__":
    import time
    import re
    import psutil
    import os

    pid = os.getpid()
    p = psutil.Process(pid)
    info_start = p.memory_full_info().uss / 1024
    start = time.time()
    trie = BinTrie()
    data = {}
    with open("D:\\模型\\hanlp-py\\data\\dictionary\\CoreNatureDictionary.txt", "r", encoding="utf-8") as f:
        for line in f:
            s = re.split(r"\s", line.strip())
            data[s[0]] = "-".join(s[1:])
    print(f"加载文件耗时：{time.time() - start}")
    start_2 = time.time()
    trie.build(data)
    print(f"构建BinTrie耗时：{time.time()-start_2}")
    start_1 = time.time()
    for k, v in data.items():
        if k not in trie:
            print(k)
        else:
            assert v == trie[k]
    print(f"遍历BinTrie耗时：{time.time()-start_1}")
    print(f"总耗时：{time.time()-start}")
    info_end = p.memory_full_info().uss / 1024
    print(f"程序占用了内存{info_end - info_start}KB")
