

from pathlib import Path

from collection.DAWG import dawg


class StopWordDictionary(dawg.DAWG):
    def __init__(self, data=[]):
        if isinstance(data, tuple) or isinstance(data, list):
            data = data
        elif isinstance(data, Path):
            res = []
            with open(data, encoding="utf-8") as f:
                for line in f:
                    res.append(line.strip())
            data = res
        elif isinstance(data, str):
            file = Path(data)
            if file.is_file():
                res = []
                with open(data) as f:
                    for line in f:
                        res.append(line)
                data = res
            else:
                data = []
        else:
            data = []
        super().__init__(data)

    def should_include(self, term):
        return term.word in self


if __name__ == '__main__':
    d = ["人", "狗", "猪"]
    s = StopWordDictionary(d)
    print("人" in s)
    print("鸡" in s)