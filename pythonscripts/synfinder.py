from requests import get
import pkg_resources
import json
import itertools, time, sys

key = open(pkg_resources.resource_filename(__name__, '/text/key.txt'),'r').read().strip()

converter = {'adj': 'adjective', 'adv': 'adverb'}
def syn(token):
    global key
    pos = token.pos_.lower()
    pos = converter[pos] if pos in converter.keys() else pos
    word = token.lemma_.lower()
    link = f'http://words.bighugelabs.com/api/2/{key}/{word}/json'

    response = get(link).text
    try:
        words = json.loads(response)
        print(words)
    except:
        print('There is an error.')
        return []
    if pos in words.keys():
        print(words)
        if 'syn' in words[pos]:
            return words[pos]['syn']
        elif 'sim' in words[pos]:
            return words[pos]['sim']
        elif 'rel' in word[pos]:
            return words[pos]['rel']
        else:
            return []
    else:
        all = []
        for i, j in words.items():
            for a, b in j.items():
                all.append(b)
        return all
