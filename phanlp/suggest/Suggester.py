"""
文本推荐器
"""
from algorithm.pytreemap import TreeMap
from suggest.scorer.editdistance.EditDistanceScorer import EditDistanceScorer
from suggest.scorer.lexeme.IdVectorScorer import IdVectorScorer
from suggest.scorer.pinyin.PinyinScorer import PinyinScorer


class Suggester:
    def __init__(self, scorer_list=None):
        if scorer_list is None:
            self.scorer_list = []
            # self.scorer_list.append(IdVectorScorer())
            self.scorer_list.append(EditDistanceScorer())
            # self.scorer_list.append(PinyinScorer())
        else:
            self.scorer_list = scorer_list

    def add_sentence(self, sentence):
        for scorer in self.scorer_list:
            scorer.add_sentence(sentence)

    def remove_all_sentences(self):
        for scorer in self.scorer_list:
            scorer.remove_all_sentences()

    def suggest(self, key, size):
        result_list = []
        score_map = TreeMap()
        for scorer in self.scorer_list:
            _map = scorer.compute_score(key)
            _max = self.__max(_map)
            for k, v in _map.items():
                score = score_map.get(k)
                if score is None:
                    score = 0.0
                score_map.put(k, score / _max + v * scorer.boost)
        for value in self.sort_score_map(score_map).values():
            for sentence in value:
                if len(result_list) >= size:
                    return result_list
                result_list.append(sentence)
        return result_list

    @staticmethod
    def sort_score_map(score_map):
        result = TreeMap()
        for k, v in score_map.items():
            sentence_set = result.get(k)
            if sentence_set is None:
                sentence_set = set()
                result.put(v, sentence_set)
            sentence_set.add(k)
        return result

    @staticmethod
    def __max(_map):
        the_max = 0.0
        for v in _map.values():
            the_max = max(the_max, v)
        return the_max



