
from corpus.tag.Nature import Nature
from config import SHOW_TERM_NATURE
from utility.LexiconUtility import LexiconUtility


class Term:
    def __init__(self, word: str, nature: Nature):
        self.word = word
        self.nature = nature

    def to_string(self):
        if SHOW_TERM_NATURE:
            return f"{self.word}/{self.nature}"
        return self.word

    __str__ = to_string
    __repr__ = to_string

    def length(self):
        return len(self.word)

    __len__ = length

    def get_frequency(self):
        return LexiconUtility.get_frequency(self.word)

    def __eq__(self, other):
        if isinstance(other, Term):
            if self.word == other.word and self.nature == other.nature:
                return True
        return self == other
