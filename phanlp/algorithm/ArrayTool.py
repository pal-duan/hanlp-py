

class ArrayTool:
    @classmethod
    def binary_search(cls, branches, node):
        length = len(branches)
        if not length:
            return -1
        low, high = 0, length - 1
        while low <= high:
            mid = (low + high) // 2
            if branches[mid] == node:
                return mid
            elif branches[mid] < node:
                low = mid + 1
            elif branches[mid] > node:
                high = mid - 1
        return -(low + 1)
