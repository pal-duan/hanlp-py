

from dictionary.CoreDictionary import CoreDictionary
from corpus.tag.Nature import Nature
from utility.Predefine import Predefine
from utility.MathUtility import MathUtility


class Vertex:
    """
    顶点
    """
    def __init__(self, real_word, attribute=None, word=None, word_id=None):
        assert len(real_word) > 0, "构造空白节点会导致死循环"
        if attribute is None:
            attribute = CoreDictionary.get(real_word)
        if word_id is None:
            word_id = -1 if attribute is None else -attribute.total_frequency
        if attribute is None:
            attribute = CoreDictionary.Attribute(Nature.from_string("n"), 1)
        if word is None:
            word = self.compile_real_word(real_word, attribute)
        self.word_id = word_id
        self.attribute = attribute
        self.word = word
        self.real_word = real_word
        self._from = None  # 到该节点的最短路径的前驱结点
        self.weight = None  # 最短路径对应的权重

    def compile_real_word(self, real_word, attribute):
        if len(attribute.nature) == 1:
            nature = attribute.nature[0]
            if nature.startswith("nr"):
                self.word_id = CoreDictionary.NR_WORD_ID
                return Predefine.TAG_PEOPLE
            elif nature.startswith("ns"):
                self.word_id = CoreDictionary.NS_WORD_ID
                return Predefine.TAG_PLACE
            elif nature == Nature.from_string("nx"):
                self.word_id = CoreDictionary.NX_WORD_ID
                if self.word_id == -1:
                    self.word_id = CoreDictionary.X_WORD_ID
                return Predefine.TAG_PROPER
            elif nature.startswith("nt") or nature == Nature.from_string("nit"):
                self.word_id = CoreDictionary.NT_WORD_ID
                return Predefine.TAG_GROUP
            elif nature.startswith("m"):
                self.word_id = CoreDictionary.M_WORD_ID
                self.attribute = CoreDictionary.get(CoreDictionary.M_WORD_ID)
                return Predefine.TAG_NUMBER
            elif nature.startswith("x"):
                self.word_id = CoreDictionary.X_WORD_ID
                self.attribute = CoreDictionary.get(CoreDictionary.X_WORD_ID)
                return Predefine.TAG_CLUSTER
            elif nature == Nature.from_string("t"):
                self.word_id = CoreDictionary.T_WORD_ID
                self.attribute = CoreDictionary.get(CoreDictionary.T_WORD_ID)
                return Predefine.TAG_TIME
        return real_word

    def update_from(self, _from):
        weight = _from.weight + MathUtility.calculate_weight(_from, self)
        if self._from is None or self.weight > weight:
            self._from = _from
            self.weight = weight

    def get_real_word(self):
        return self.real_word

    def get_from(self):
        return self._from

    def set_from(self, _from):
        self._from = _from

    def get_attribute(self):
        return self.attribute

    def confirm_nature(self, nature):
        if len(self.attribute.nature) == 1 and self.attribute.nature[0] == nature:
            return True
        result = True
        frequency = self.attribute.get_nature_frequency(nature)
        if frequency == 0:
            frequency = 1000
            result = False
        self.attribute = CoreDictionary.Attribute(nature, frequency)
        return result

    def get_nature(self):
        if len(self.attribute.nature) == 1:
            return self.attribute.nature[0]
        return None

    def guess_nature(self):
        return self.attribute.nature[0]

    def has_nature(self, nature):
        return self.attribute.get_nature_frequency(nature) > 0

    def copy(self):
        return Vertex(self.real_word, self.attribute, self.word)

    def set_word(self, word):
        self.word = word
        return self

    def set_real_word(self, real_word):
        self.real_word = real_word
        return self

    @staticmethod
    def new_number_instance(real_word):
        return Vertex(real_word, CoreDictionary.Attribute(Nature.from_string("m"), 1000), Predefine.TAG_NUMBER)

    @staticmethod
    def new_b():
        return Vertex(
            " ",
            CoreDictionary.Attribute(Nature.from_string("begin"), Predefine.TOTAL_FREQUENCY / 10),
            Predefine.TAG_BIGIN,
            CoreDictionary.get_word_id(Predefine.TAG_BIGIN)
        )

    @staticmethod
    def new_e():
        return Vertex(
            " ",
            CoreDictionary.Attribute(Nature.from_string("end"), Predefine.TOTAL_FREQUENCY / 10),
            Predefine.TAG_END,
            CoreDictionary.get_word_id(Predefine.TAG_END)
        )

    def length(self):
        return len(self.real_word)

    __len__ = length

    def to_string(self):
        return self.real_word

    __str__ = to_string
    __repr__ = to_string
