# -*- coding: utf-8 -*-
# @Time: 2022/5/28  22:19
# @Author: 2811755762@qq.com
"""
    Description:
        基于Aho-Corasick白皮书， 贝尔实验室：ftp://163.13.200.222/assistant/bearhero/prog/%A8%E4%A5%A6/ac_bm.pdf
"""
from collections import deque

from algorithm.ahocorasick.trie.TrieConfig import TrieConfig
from algorithm.ahocorasick.trie.State import State
from algorithm.ahocorasick.trie.Emit import Emit


class Trie:
    def __init__(self, trie_config=TrieConfig(), kewords=None):
        self.trie_config = trie_config
        self.root_state = State()
        self.failure_states_constructed = False
        if kewords:
            self.add_all_keyword(kewords)

    def remove_overlaps(self):
        self.trie_config.set_allow_overlaps(False)
        return self

    def remain_longest(self):
        self.trie_config.remain_longest = True
        return self

    def add_keyword(self, keyword):
        if not keyword:
            return
        current_state = self.root_state
        for character in keyword:
            current_state = current_state.add_state(character)
        current_state.add_emit(keyword)

    def add_all_keyword(self, keywords):
        for keyword in keywords:
            self.add_keyword(keyword)

    def construct_failure_states(self):
        """
        建立failure表
        :return:
        """
        queue = deque()
        for depth_one_state in self.root_state.get_states():
            depth_one_state.set_failure(self.root_state)
            queue.append(depth_one_state)

        self.failure_states_constructed = True
        while queue:
            current_state = queue.popleft()
            for transition in current_state.get_transitions():
                target_state = current_state.next_state(transition)
                queue.append(target_state)
                trace_failure_state = current_state.get_failure()
                while trace_failure_state.next_state(transition) is None:
                    trace_failure_state = trace_failure_state.get_failure()
                new_failure_state = trace_failure_state.next_state(transition)
                target_state.set_failure(new_failure_state)
                target_state.add_emit(new_failure_state.get_emits())

    def check_for_constructed_failure_states(self):
        if not self.failure_states_constructed:
            self.construct_failure_states()

    @classmethod
    def get_state(cls, current_state, character):
        new_current_state = current_state.next_state(character)
        while new_current_state is None:
            current_state = current_state.get_failure()
            new_current_state = current_state.next_state(character)
        return new_current_state

    def parse_text(self, text):
        self.check_for_constructed_failure_states()
        position = 0
        current_state = self.root_state
        collected_emits = []
        for i in range(len(text)):
            current_state = self.get_state(current_state, text[i])
            self.store_emits(position, current_state, collected_emits)
            position += 1
        return collected_emits

    @classmethod
    def store_emits(cls, position, current_state, collected_emits):
        emits = current_state.get_emits()
        if emits:
            for emit in emits:
                collected_emits.append(Emit(position-len(emit)+1), position, emit)


    def tokenize(self, text):
        tokens = []
        collected_emits = self.parse_text(text)
        interval_tree = Interval

if __name__ == "__main__":
    pass
