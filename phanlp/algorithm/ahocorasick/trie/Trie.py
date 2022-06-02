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
from algorithm.ahocorasick.interval.IntervalTree import IntervalTree
from algorithm.ahocorasick.trie.FragmentToken import FragmentToken
from algorithm.ahocorasick.trie.MatchToken import MatchToken
from algorithm.pytreemap import TreeMap


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

    def remain_longest(self, collected_emits=None):
        if collected_emits is None:
            self.trie_config.remain_longest = True
            return self
        if len(collected_emits) < 2:
            return
        emit_map_start = TreeMap()
        for emit in collected_emits:
            pre = emit_map_start.get(emit.get_start())
            if pre is None or len(pre) < emit.size():
                emit_map_start.put(emit.get_start(), emit)

        if emit_map_start.size() < 2:
            collected_emits.clear()
            collected_emits.extend(emit_map_start.values())
            return

        emit_map_end = TreeMap()
        for emit in emit_map_start.values():
            pre = emit_map_end.get(emit.get_end())
            if pre is None or pre.size() < emit.size():
                emit_map_end.put(emit.get_end(), emit)
        collected_emits.clear()
        collected_emits.extend(emit_map_end.values())

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
        interval_tree = IntervalTree(collected_emits)
        interval_tree.remove_overlaps(collected_emits)

        last_collected_position = -1
        for emit in collected_emits:
            if emit.get_start() - last_collected_position > 1:
                tokens.append(self.create_fragment(emit, text, last_collected_position))
            tokens.append(self.create_match(emit, text))
            last_collected_position = emit.get_end()

        if len(text) - last_collected_position > 1:
            tokens.append(self.create_fragment(None, text, last_collected_position))
        return tokens

    @staticmethod
    def create_fragment(emit, text, last_collected_position):
        return FragmentToken(text[last_collected_position+1:len(text) if emit is None else emit.get_start()])

    @staticmethod
    def create_match(emit, text):
        return MatchToken(text[emit.get_start():emit.get_end()+1], emit)

    def dfs(self):
        # TODO
        pass

    def has_keyword(self, text):
        self.check_for_constructed_failure_states()
        current_state = self.root_state
        for i in range(len(text)):
            next_state = self.get_state(current_state, text[i])
            if next_state is not None and next_state != current_state and len(next_state.get_emits()) != 0:
                return True
            current_state = next_state
        return False




if __name__ == "__main__":
    pass
