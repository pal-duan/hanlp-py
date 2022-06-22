"""
基于语义距离的班级距离实现
"""


class EditDistance:
    @classmethod
    def compute(cls, wrong_word, right_word):
        m = len(wrong_word)
        n = len(right_word)
        d = [[0] * (n + 1) for _ in range(m+1)]
        for j in range(n+1):
            d[0][j] = j
        for i in range(m+1):
            d[i][0] = i
        for i in range(1, m+1):
            ci = wrong_word[i-1]
            for j in range(1, n+1):
                cj = right_word[j-1]
                if ci == cj:
                    d[i][j] = d[i-1][j-1]
                elif i > 1 and j > 1 and ci == right_word[j-2] and cj == wrong_word[i-2]:
                    d[i][j] = 1 + min(d[i-2][j-2], min(d[i][j-1], d[i-1][j]))
                else:
                    d[i][j] = min(d[i-1][j-1] + 1, min(d[i][j-1] + 1, d[i-1][j] + 1))
        return d[m][n]


if __name__ == '__main__':
    print(EditDistance.compute("我是谁", "我是"))
