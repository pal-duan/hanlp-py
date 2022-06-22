

from suggest.scorer.lexeme.IdVector import IdVector
from suggest.scorer.BaseScorer import BaseScorer


class IdVectorScorer(BaseScorer):
    def generate_key(self, sentence):
        if not sentence:
            return None
        return IdVector(sentence)
