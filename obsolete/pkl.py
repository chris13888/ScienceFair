import pickle
import os

curpath = os.path.dirname(__file__)
dictionary = {}
with open(curpath+'data/allwords.txt', 'r', encoding='utf8') as file:
    for ln in file.read().split('\n'):
        line = ln.split()
        try:
            dictionary[line[1]] = int(line[2].replace(',', ''))
        except:
            continue

pickle.dump(dictionary, open(curpath+'data/words.pickle', 'wb'))
