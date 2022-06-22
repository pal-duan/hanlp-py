"""
基本打分器
"""
from algorithm.pytreemap import TreeMap, TreeSet


class BaseScorer:
    def __init__(self):
        self.storage = TreeMap()
        self.boost = 1.0

    def set_boost(self, boost):
        self.boost = boost
        return self

    def add_sentence(self, sentence):
        key = self.generate_key(sentence)
        if key is None:
            return
        value_set = self.storage.get(key)
        if value_set is None:
            value_set = TreeSet()
            self.storage.put(key, value_set)
        value_set.add(sentence)

    def generate_key(self, sentence):
        pass

    def compute_score(self, outer_sentence):
        result = TreeMap()
        key_outer = self.generate_key(outer_sentence)
        if key_outer is None:
            return result
        for k, v in self.storage.items():
            score = key_outer.similarity(k)
            for sentence in v:
                result.put(sentence, score)
        return result

    def remove_all_sentences(self):
        self.storage.clear()
