"""
编辑距离打分器
"""


from suggest.scorer.BaseScorer import BaseScorer
from suggest.scorer.editdistance.CharArray import CharArray


class EditDistanceScorer(BaseScorer):
    def generate_key(self, sentence):
        if not sentence:
            return None
        return CharArray(sentence)
