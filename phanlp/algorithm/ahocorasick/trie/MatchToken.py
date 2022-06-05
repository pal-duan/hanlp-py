

from algorithm.ahocorasick.trie.Token import Token


class MatchToken(Token):
    def __init__(self, fragment, emit):
        super().__init__(fragment)
        self.emit = emit

    def is_match(self):
        return True

    def get_emit(self):
        return self.emit
