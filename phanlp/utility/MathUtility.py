

import math

from dictionary.CoreBiGramTableDictionary import CoreBiGramTableDictionary
from utility.Predefine import Predefine


class MathUtility:
    @classmethod
    def calculate_weight(cls, _from, to):
        f_from = _from.get_attribute().total_frequency
        f_bi_gram = CoreBiGramTableDictionary.get_bi_frequency(_from.word_id, to.word_id)
        f_to = to.get_attribute().total_frequency
        return -math.log(Predefine.LAMBDA * (Predefine.myu * f_bi_gram / (f_from + 1) + 1 - Predefine.myu) +
                         (1 - Predefine.LAMBDA) * f_to / Predefine.TOTAL_FREQUENCY)
