

class Token:
    def __init__(self, fragment):
        self.fragment = fragment

    def get_fragment(self):
        return self.fragment

    def is_match(self):
        pass

    def get_emit(self):
        pass

    def to_string(self):
        return f"{self.fragment}/{self.is_match()}"
