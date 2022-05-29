# -*- coding: utf-8 -*-
# @Time: 2022/5/29  20:44
# @Author: 2811755762@qq.com
"""
    Description:
        线段树上面的节点，实际上是一些区间的集合，并且按中点维护了两个节点
"""


class IntervalNode:
    def __init__(self, intervals):
        self.left = None
        self.right = None
        self.intervals = []
        self.point = self.determine_median(intervals)

        to_left, to_right = [], []
        for interval in intervals:
            if interval.get_end() < self.point:
                to_left.append(interval)
            elif interval.get_start() > self.point:
                to_right.append(interval)
            else:
                self.intervals.append(interval)
        if to_left:
            self.left = IntervalNode(to_left)
        if to_right:
            self.right = IntervalNode(to_right)

    @staticmethod
    def determine_median(intervals):
        """
        计算中点
        :param intervals:
        :return:
        """
        start = -1
        end = -1
        for interval in intervals:
            current_start = interval.get_start()
            current_end = interval.get_end()
            if start == -1 or current_start < start:
                start = current_start
            if end == -1 or current_end > end:
                end = current_end
        return (start + end) / 2


if __name__ == "__main__":
    pass
