# -*- coding: utf-8 -*-
# @Time: 2022/5/28  22:27
# @Author: 2811755762@qq.com
"""
    Description:
        一个状态有如下几个功能：
            success: 成功转移到另一个状态
            failure: 不可顺着字符串跳转的话，则跳转到一个浅一点的节点
            emits: 命中一个模式串
"""
from algorithm.pytreemap import TreeMap, TreeSet


class State:
    def __init__(self, depth=0):
        self.depth = depth
        self.failure = None
        self.emits = None
        self.success = TreeMap()

    def get_depth(self):
        return self.depth

    def add_emit(self, keyword):
        if self.emits is None:
            self.emits = TreeSet()
        self.emits.add(keyword)

    def add_emits(self, keyword_list):
        for keyword in keyword_list:
            self.add_emit(keyword)

    def get_emits(self):
        return [] if self.emits is None else self.emits

    def get_failure(self):
        return self.failure

    def set_failure(self, fail_state):
        self.failure = fail_state

    def next_state(self, character, ignore_root_state: bool = False):
        next_state = self.success.get(character)
        if not ignore_root_state and next_state is None and self.depth == 0:
            next_state = self
        return next_state

    def add_state(self, character):
        next_state = self.next_state(character, True)
        if next_state is None:
            next_state = State(self.depth+1)
            self.success.put(character, next_state)
        return next_state

    def get_states(self):
        return self.success.values()

    def get_transitions(self):
        return self.success.key_set()

    def to_string(self):
        return f"State{{depth={self.depth}, emits={self.emits}, success={self.success}, failure={self.failure}}}"

    __str__ = to_string
    __repr__ = to_string


if __name__ == "__main__":
    pass
