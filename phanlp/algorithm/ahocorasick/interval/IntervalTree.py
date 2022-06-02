# -*- coding: utf-8 -*-
# @Time: 2022/5/29  20:41
# @Author: 2811755762@qq.com
"""
    Description:
        线段树，用于检查区间重叠
"""
from functools import cmp_to_key

from algorithm.ahocorasick.interval.IntervalNode import IntervalNode
from algorithm.pytreemap import TreeSet


def interval_compare_by_size(x, y):
    flag = x.size() - y.size()
    if flag == 0:
        flag = x.get_start() - y.get_start()
    return flag


def interval_compare_by_position(x, y):
    return x.get_start() - y.get_start()


class IntervalTree:
    def __init__(self, intervals=None):
        if intervals:
            self.root_node = IntervalNode(intervals)
        else:
            self.root_node = None

    def remove_overlaps(self, intervals: list):
        intervals.sort(key=cmp_to_key(interval_compare_by_size))
        remove_intervals = TreeSet()
        for interval in intervals:
            if remove_intervals.contains(interval):
                continue
            remove_intervals.add_all(self.find_overlaps(interval))

        for remove_interval in remove_intervals:
            intervals.remove(remove_interval)

        intervals.sort(key=cmp_to_key(interval_compare_by_position))
        return intervals

    def find_overlaps(self, interval):
        return self.root_node.find_overlaps(interval)


if __name__ == "__main__":
    pass
