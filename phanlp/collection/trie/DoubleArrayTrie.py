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
from algorithm.pytreemap import TreeMap
from utility.logger import logger


class ITrie(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build(self, key_value_map: dict) -> int:
        pass

    @abc.abstractmethod
    def save(self, out) -> bool:
        pass

    @abc.abstractmethod
    def load(self, fp, value) -> bool:
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
    def count(self) -> int:
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
            self.build(data)

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
                if cur > self.max_code:
                    self.max_code = cur
                elif cur < self.min_code:
                    self.min_code = cur

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

    def build(self, key_value_map: TreeMap) -> int:
        # key_value_map = to_treemap(key_value_map)
        assert key_value_map is not None
        self.key = list(key_value_map.keys())
        self.v = list(key_value_map.values())
        # self.length = [len(k) for k in self.key]
        self.key_size = len(self.key)
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

    def transition(self, current: int, c: str) -> int:
        b = self.base[current]
        p = b + c + 1
        if b == self.check[p]:
            b = self.base[p]
        else:
            return -1
        return b

    def get_cache_obj(self) -> dict:
        obj = {
            "base": self.base,
            "check": self.check,
            "size": self.size,
            "alloc_size": self.alloc_size,
            "error_": self.error_,
            "key": self.key,
            "key_size": self.key_size,
            "length": self.length,
            "value": self.value,
            "progress": self.progress,
            "next_check_pos": self.next_check_pos,
            "max_code": self.max_code,
            "min_code": self.min_code
        }
        return obj

    def save(self, out) -> bool:
        try:
            out.write(str(self.size) + "\n")
            for i in range(self.size):
                out.write(str(self.base[i]) + "\n")
                out.write((str(self.check[i])) + "\n")
        except Exception as e:
            logger.warning(f"DoubleArrayTree缓存失败，\ndetail: {e}")
            return False
        return True

    def load_from_json(self, attributes: dict) -> bool:
        try:
            self.base = attributes["base"]
            self.check = attributes["check"]
            self.size = attributes["size"]
            self.alloc_size = attributes["alloc_size"]
            self.error_ = attributes["error_"]
            self.key = attributes["key"]
            self.key_size = attributes["key_size"]
            self.length = attributes["length"]
            self.value = attributes["value"]
            self.progress = attributes["progress"]
            self.next_check_pos = attributes["next_check_pos"]
            self.max_code = attributes["max_code"]
            self.min_code = attributes["min_code"]
            self.v = attributes["v"]
        except Exception:
            return False
        return True

    def load(self, fp, value):
        if fp is None:
            return False
        self.size = int(fp.readline().strip())
        for i in range(self.size):
            self.base.append(int(fp.readline().strip()))
            self.check.append(int(fp.readline().strip()))
        self.v = value
        return True

    def get(self, key: str):
        index = self.exact_match_search(key)
        if index >= 0:
            return self.get_from_index(index)
        return None

    def get_from_index(self, index: int):
        return self.v[index]

    def get_value_array(self, a):
        # TODO
        pass

    def contain_key(self, key: str) -> bool:
        return self.exact_match_search(key) >= 0

    def count(self) -> int:
        return len(self.v)

    def __len__(self):
        return self.count()

    def __contains__(self, item):
        return self.contain_key(item)

    def __getitem__(self, item):
        return self.get(item)

    def __str__(self):
        return f"DoubleArrayTrie{{key_size={self.key_size}}}"


if __name__ == "__main__":
    import time
    import re
    import psutil
    import os
    from algorithm.pytreemap import TreeMap
    pid = os.getpid()
    p = psutil.Process(pid)
    info_start = p.memory_full_info().uss/1024
    data = TreeMap()
    start = time.time()
    with open("D:\\模型\\hanlp-py\\data\\dictionary\\CoreNatureDictionary.txt", "r", encoding="utf-8") as f:
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
    for key, value in data.items():
        f = a.contain_key(key)
        if not f:
            err.append(key)
        else:
            v = a.get(key)
            if v != value:
                print(f"key: {key}, value: {value}, v: {v}")
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
    info_end = p.memory_full_info().uss/1024
    print(f"程序占用了内存{info_end-info_start}KB")
