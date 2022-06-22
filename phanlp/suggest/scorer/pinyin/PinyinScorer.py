

from suggest.scorer.BaseScorer import BaseScorer


class PinyinScorer(BaseScorer):
    def generate_key(self, sentence):
        pinyin_key = PinyinKey(sentence)
        if pinyin_key.size() == 0:
            return None
        return pinyin_key
