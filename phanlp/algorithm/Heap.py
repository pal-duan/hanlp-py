# -*- coding: utf-8 -*-
# @Time: 2022/5/14  13:06
# @Author: 2811755762@qq.com
"""
    Description:
    堆的实现
"""


class HeapEmptyError(Exception):
    pass


class BaseHeap(object):
    @staticmethod
    def compare(x, y):
        return True if x > y else False

    def __init__(self, max_size: int = None, compare=None):
        if max_size is None:
            max_size = float("inf")
        self.max_size = max_size
        self.data = []
        self.count = 0
        if compare is not None:
            self.compare = compare

    def __len__(self):
        return self.count

    def length(self):
        return len(self)

    def is_empty(self):
        return self.count == 0

    def __str__(self):
        return None if self.count == 0 else self.data[:self.count]

    def push(self, value):
        if self.count >= self.max_size:
            if self.compare(self.data[0], value):
                self.pop()
                self.push(value)
            return
        self.data.append(value)
        self._shift_up(self.count)
        self.count += 1

    @staticmethod
    def _parent(index):
        assert index != 0
        return (index - 1) // 2

    @staticmethod
    def _left_child(index):
        return 2 * index + 1

    @staticmethod
    def _right_child(index):
        return 2 * index + 2

    def _shift_up(self, index):
        while index > 0 and self.compare(self.data[index], self.data[self._parent(index)]):
            parent = self._parent(index)
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            index = parent

    def _shift_down(self, index):
        while self._left_child(index) < self.count:
            left_child_index = self._left_child(index)
            right_child_index = self._right_child(index)

            max_index = left_child_index
            if right_child_index < self.count and self.compare(self.data[right_child_index], self.data[left_child_index]):
                max_index = right_child_index

            if self.compare(self.data[index], self.data[max_index]):
                break

            self.data[index], self.data[max_index] = self.data[max_index], self.data[index]
            index = max_index

    def pop(self):
        if not self.count:
            raise HeapEmptyError
        value = self.data[0]
        self.data[0], self.data[self.count-1] = self.data[self.count-1], self.data[0]
        self.data.pop()
        self.count -= 1
        self._shift_down(0)
        return value

    def heapify(self, array):
        if not array:
            return
        for i in array:
            self.push(i)
        return self

    def to_list(self):
        # 自毁型操作
        ans = []
        while not self.is_empty():
            ans.append(self.pop())
        return ans[::-1]


class MaxHeap(BaseHeap):
    def __init__(self, size=None, compare=lambda x, y: True if x > y else False):
        super().__init__(size, compare)


class MinHeap(BaseHeap):
    def __init__(self, size=None, compare=lambda x, y: True if x < y else False):
        super().__init__(size, compare)


if __name__ == "__main__":
    a = MinHeap(3)
    l = [1,6,2,5,3,4,9,8,7,0, 0 , 0]
    # for i in l:
    #     a.push(i)
    a.heapify(l)
    print(a.to_list())
    print(a.count)
    # for i in range(len(l)):
    #     print(a.pop())
