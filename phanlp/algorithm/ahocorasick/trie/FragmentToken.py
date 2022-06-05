

from algorithm.ahocorasick.trie.Token import Token


class FragmentToken(Token):
    def __init__(self, fragment):
        super().__init__(fragment)

    def is_match(self):
        return False

    def get_emit(self):
        return None
