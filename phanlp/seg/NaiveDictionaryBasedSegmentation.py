

from dictionary.CoreDictionary import CoreDictionary


class NaiveDictionaryBasedSegmentation:
    @classmethod
    def fully_segment(cls, document: str, dictionary=CoreDictionary):
        result = []
        length = len(document)
        for i in range(length):
            for j in range(i+1, length+1):
                word = document[i:j]
                if dictionary.contains(word):
                    result.append(word)
        return result

    @classmethod
    def forward_longest_segment(cls, document: str, dictionary=CoreDictionary):
        result = []
        length = len(document)
        i = 0
        while i < length:
            longest_word = document[i: i+1]
            for j in range(i+1, length+1):
                word = document[i:j]
                if dictionary.contains(word):
                    if len(word) > len(longest_word):
                        longest_word = word
            result.append(longest_word)
            i += len(longest_word)
        return result

    @classmethod
    def backward_longest_segment(cls, document: str, dictionary=CoreDictionary):
        result = []
        length = len(document)
        i = length - 1
        while i >= 0:
            longest_word = document[i:i+1]
            for j in range(i+1):
                word = document[j:i+1]
                if dictionary.contains(word):
                    if len(word) > len(longest_word):
                        longest_word = word
                        break
            result.append(longest_word)
            i -= len(longest_word)
        return result[::-1]

    @classmethod
    def bidirectional_segment(cls, document: str, dictionary=CoreDictionary):
        f = cls.forward_longest_segment(document)
        b = cls.backward_longest_segment(document)
        if len(f) < len(b):
            return f
        elif len(f) > len(b):
            return b
        else:
            if cls.char_count(f) < cls.char_count(b):
                return f
            else:
                return b

    @staticmethod
    def char_count(word_list):
        count = 0
        for word in word_list:
            if len(word) == 1:
                count += 1
        return count


if __name__ == '__main__':
    text = "江西鄱阳湖干枯，中国最大淡水湖变成大草原"
    print(NaiveDictionaryBasedSegmentation.fully_segment(text))
    print(NaiveDictionaryBasedSegmentation.forward_longest_segment(text))
    print(NaiveDictionaryBasedSegmentation.backward_longest_segment(text))
    print(NaiveDictionaryBasedSegmentation.bidirectional_segment(text))
