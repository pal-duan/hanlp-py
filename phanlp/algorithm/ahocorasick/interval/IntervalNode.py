# -*- coding: utf-8 -*-
# @Time: 2022/5/29  20:44
# @Author: 2811755762@qq.com
"""
    Description:
        线段树上面的节点，实际上是一些区间的集合，并且按中点维护了两个节点
"""
from enum import Enum


class IntervalNode:
    class Direction(Enum):
        LEFT = 0
        RIGHT = 1

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

    def find_overlaps(self, interval):
        overlaps = []
        if self.point < interval.get_start():
            self.add_to_overlaps(interval, overlaps, self.find_overlapping_ranges(self.right, interval))
            self.add_to_overlaps(interval, overlaps, self.check_for_overlaps_to_right(interval))
        elif self.point > interval.get_end():
            self.add_to_overlaps(interval, overlaps, self.find_overlapping_ranges(self.left, interval))
            self.add_to_overlaps(interval, overlaps, self.check_for_overlaps_to_left(interval))

    def check_for_overlaps_to_left(self, interval):
        return self.check_for_overlaps(interval, self.Direction.LEFT)

    def check_for_overlaps_to_right(self, interval):
        return self.check_for_overlaps(interval, self.Direction.RIGHT)

    def check_for_overlaps(self, interval, direction):
        overlaps = []
        for current_interval in self.intervals:
            if direction == self.Direction.LEFT:
                if current_interval.get_start <= interval.get_end():
                    overlaps.append(current_interval)
            elif direction == self.Direction.RIGHT:
                if current_interval.get_end() >= interval.get_start():
                    overlaps.append(current_interval)
        return overlaps

    @staticmethod
    def add_to_overlaps(interval, overlaps, new_overlaps):
        for current_interval in new_overlaps:
            if current_interval != interval:
                overlaps.append(current_interval)

    @staticmethod
    def find_overlapping_ranges(node, interval):
        if node is not None:
            return node.find_overlaps(interval)
        return []


if __name__ == "__main__":
    pass
