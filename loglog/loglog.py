import math
class BloomFilter:
    def __init__(self, len_of_bloom_filter: int, k:int, m:int):
        self.array = []
        self.bloom_array = []
        self.n = len_of_bloom_filter
        self.k = k
        self.m = m
        for i in range(0, self.n):
            self.bloom_array.append(0)

    def __str__(self):
        return f"array is: {self.array}, bloom filter is: {self.bloom_array}"

    def _make_hash(self, word):
        res = []
        for i in range(1, self.k+1):
            x = (ord(word[0])+ord(word[-1])*i) % self.n
            res.append(x)
        return res

    def add(self, word):
        res = self._make_hash(word)
        for i in range(0, self.k):
            self.bloom_array[res[i]] = 1
            self.array.append(word)
        return True

    def check_filter(self, word):
        res = self._make_hash(word)
        probability_false_positive = 0
        availability = False
        c = 0
        for i in range(0, self.k):
            if self.bloom_array[res[i]] == 1:
                c +=1
        if c == self.k:
            availability = True
            probability_false_positive = (
                1 - (math.e ** ((-self.k * self.m) / self.n))
            ) ** self.k
        if availability:
            return probability_false_positive
        else:
            return False

def add_text_in_bloom_filter(text):
    text = text.replace('  ', ' ')
    text = text.strip().split(' ')
    #print(text)
    res = set()
    for i in text:
        print(i)
        if i[-1] == '.' or i[-1] == ',' or i[-1] == '!' or i[-1] == '?' or i[-1] == ')':
            res.add(i[:-1:])
        elif i[0] == '(':
            res.add(i[1::])
        else:
            res.add(i)
    p = 0.08
    m = len(res)
    n = int(((math.log(p, 2))/math.log(2, math.e)) * (-m))+1
    k = int((n/m)*math.log(2, math.e))
    bloom_fil = BloomFilter(n, k, m)
    for i in res:
        bloom_fil.add(i)
    return bloom_fil

if __name__ == "__main__":
    print("input text: ")
    text = input()
    my_array = add_text_in_bloom_filter(text)
    while True:
        print("input word: ")
        word = input()
        res = my_array.check_filter(word)
        if res == False:
            print("no word")
        else:
            print(
                f"prob: {res}")