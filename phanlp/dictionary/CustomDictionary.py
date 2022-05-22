# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:07
# @Author: 2811755762@qq.com
"""
    Description:
    自定义词典
"""
from dictionary.DynamicCustomDictionary import DynamicCustomDictionary
from config import CUSTOM_DICTIONARY_PATH


class CustomDictionary(object):
    DEFAULT = DynamicCustomDictionary(CUSTOM_DICTIONARY_PATH)

    def __init__(self):
        pass

    @classmethod
    def get(cls, word: str):
        return cls.DEFAULT.get(word)

    @classmethod
    def contains(cls, word):
        return cls.DEFAULT.contains(word)


if __name__ == "__main__":
    from algorithm.pytreemap import TreeMap
    import time
    import re
    data = TreeMap()
    start = time.time()
    with open("D:\\模型\\hanlp-py\\data\\dictionary\\custom\\CustomDictionary.txt", "r", encoding="utf-8") as f:
        for line in f:
            s = re.split(r"\s", line.strip())
            # s = line.strip().split("\t")
            if s[0] in data:
                print(s[0])
            data[s[0]] = "-".join(s[1:])
    print(f"文件读取耗时：{time.time() - start}")
    print(data.size())
    err = []
    i = 0
    for key, value in data.items():
        f = CustomDictionary.contains(key)
        if not f:
            err.append(key)
        else:
            v = CustomDictionary.get(key)
            if v != value:
                i += 1
    print(err, i)
    print(len(err))
