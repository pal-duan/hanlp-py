# -*- coding: utf-8 -*-
# @Time: 2022/5/11  22:45
# @Author: 2811755762@qq.com
"""
    Description:
    
"""
from heapq import heappush,heappop
from collections import OrderedDict


def to_treemap(data: dict) -> OrderedDict:
    heap = []
    for item in data.keys():
        heappush(heap, item)

    sort = []
    while heap:
        sort.append(heappop(heap))

    treemap = OrderedDict()
    for key in sort:
        treemap[key] = data.get(key)

    return treemap


if __name__ == "__main__":
    pass
