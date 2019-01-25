import sys
import pickle
import pkg_resources
from collections import OrderedDict

class Parser():
    def __init__(self, *, depth=2):
        file = pkg_resources.resource_filename(__name__, '/text/words.txt')
        self.depth = depth
        self.worddict = {}
        with open(file, 'r') as rf:
            for line in rf.read().split('\n'):
                ln = line.split()
                try:
                    self.worddict[ln[0].lower()] = int(ln[1])
                except:
                    try: self.worddict[ln[0].lower()] = 1
                    except: continue
        model_file = pkg_resources.resource_filename(__name__, '/text/model.pickle')
        self.model = pickle.load(open(model_file, 'rb'))
        self.wordcount = sum(self.worddict.values())
    @staticmethod
    def edit(word, numedits=1):
        'Returns all the possible edits to a word in a given statement.'
        if (numedits == 1):
            'Base case in the recursive function.'
            letters = 'abcdefghijklmnopqrstuvwxyz'

            splits = [i for i in range(len(word)+1)]

            deletechar = [word[:split] + word[1+split:] for split in splits[:-1]]

            replacechar = [word[:split] + character + word[1+split:] for split in splits[:-1] for character in letters]

            insertchar = [word[:split] + character + word[split:] for split in splits for character in letters]

            swapchar = [word[:split-1] + word[split] + word[split-1] + word[1+split:] for split in splits[1:-1]]

            return (set().union(deletechar, replacechar, insertchar, swapchar))
        else:
            # What are the edits from a step lower (e.g., 2 edits rather than 3)?
            stepbelow = Parser.edit(word, numedits-1)

            # Edit all of the ones from the step below.
            return set().union(*[Parser.edit(i, 1) for i in stepbelow])

    def word(self, w):
        return w.lower() in self.worddict.keys()

    def scale(self, info):
        'Returns the scale that I use to judge most relevant correction.'
        num = (self.worddict[info[0]] / self.wordcount) * ((1/info[1]) ** 20)
        if info[2] != '----':
            d = self.model.get(info[2], None)
            if d != None:
                num *= self.model.get(info[2], {}).get(info[2], 0)+1.5
        return num

    def correct(self, word, prev_word, *, depth=None, top=None):
        'Returns the number of corrections.'

        if (depth == None): depth = self.depth
        candidates = []
        for i in range (depth):
            candidates += [(ed, i+1, prev_word) for ed in (Parser.edit(word, i+1)) if ed in self.worddict.keys()]

        # Sort by a measure of how close it is to the original and the frequency of the word.
        print('address' in self.worddict.keys())
        c = sorted(candidates, key = self.scale, reverse = True)

        # Remove repetition but keep order.
        c = list(OrderedDict.fromkeys([i[0] for i in c]))
        if top == None: return c
        else: return c[:top]

a = Parser()
print(a.correct('adres', '----'))
