from collections import Counter

class StringCounter:
    def __init__(self):
        self.counter = Counter()

    def update(self, string):
        self.counter[string] += 1

    def guess(self):
        if not self.counter:
            return ''
        return self.counter.most_common(1)[0][0]