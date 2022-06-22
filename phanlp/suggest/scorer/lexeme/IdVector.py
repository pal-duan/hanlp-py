

class IdVector(list):
    def __init__(self, sentence):
        if isinstance(sentence, str):
            # TODO
            sentence = []
        super().__init__(sentence)
