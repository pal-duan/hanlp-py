

from algorithm.EditDistance import EditDistance


class CharArray(list):
    def __init__(self, sentence):
        super().__init__(sentence)

    def similarity(self, other):
        distance = EditDistance.compute(self, other) + 1
        return 1.0 / distance


if __name__ == '__main__':
    a = CharArray("我是谁")
    b = CharArray("我是")
    print(a, b)
    print(a > b)
    c = [a, b]
    print(c)
    c.sort()
    print(c)
