

class TermFrequency:
    def __init__(self, word, frequency=1):
        self.word = word
        self.frequency = frequency

    def increase(self, number: int = 1):
        self.frequency += number
        return self.frequency

    def get_term(self):
        return self.word

    def get_frequency(self):
        return self.frequency

    def __lt__(self, other):
        if self.frequency == other.frequency:
            return self.word < other.word
        return self.frequency < other.frequency

    def __gt__(self, other):
        if self.frequency == other.frequency:
            return self.word > other.word
        return self.frequency > other.frequency

    def __str__(self):
        return f"{self.word}={self.frequency}"

    def __repr__(self):
        return f"{self.word}={self.frequency}"


