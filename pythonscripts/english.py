import spacy
from spacy.tokens import Token

from .parser import Parser
from .synfinder import syn

import collections

Token.set_extension('spelling', default = '--')

class Document():
    # --- The Document class statics.
    parser = Parser(depth=2)
    processor = spacy.load('en_core_web_lg')
    _adjacency = 3  # The longest n-grams used. I am using unigrams, bigrams, and trigrams.
    # ---
    def __init__(self, text):
        self.text = text
        self.document = Document.processor(self.text)
        self.text_length = len([token for token in self.document if token.is_alpha])
        self.wordlist = [[word.text for word in sentence if not word.is_stop and word.is_alpha] for sentence in self.document.sents]

        self.spelling = {}
        self.synonyms = {}
        self.common_ngrams = {}

    def spellcheck(self):
        """Checks for incorrect spellings, gives suggestions."""
        pre = '----'
        for word in self.document:
            if (not (Document.parser.word(word.lemma_.lower()) or (Document.parser.word(word.text.lower())))) and (word.is_alpha) and not(word.is_stop):
                self.spelling[word.text.lower()] = [i.lower() for i in Document.parser.correct(word.text.lower(), pre, top=6)]
                pre = word.text.lower()

    def phrase_freq(self):
        """Finds repeated words through n-grams. I inadvertently used n-grams without even knowing what they were."""
        c = collections.Counter()
        for sentence in self.wordlist:
            # print(f'Start of a sentence! {sentence}, {len(sentence)}')
            for index in range(len(sentence)):
                grams = []
                for extra in range(1, Document._adjacency+1):
                    if index+extra > len(sentence):
                        # print(index+extra, 'over', len(sentence), sentence[index:index+extra])
                        continue
                    grams.append(' '.join(sentence[index:index+extra]).lower())
                # print(grams)
                c.update(grams)

        for gram, count in c.items():
            if count+len(gram.split()) < 6:
                continue

            self.common_ngrams[gram] = count
            for word in self.document:
                if word.text.lower() not in gram:
                    continue

                if word.text.lower() in self.synonyms.keys():
                    continue
                try: self.synonyms[word.text.lower()] = syn(word)
                except: self.synonyms[word.text.lower()] = []
        # print(self.common_ngrams)
    def evaluate(self):
        """Calls spellcheck and finds the phrase frequency."""
        self.spellcheck()
        self.phrase_freq()

    def returnHTML(self):
        """Returns the HTML of all the changes."""
        html = '<div class="highlight-yellow" style="padding:10px">'
        for ngram, count in self.common_ngrams.items():
            html += f'<p>The word(s) <span class="bordered">{ngram}</span> appeared {count} times.<br>'
            for word in ngram.split():
                try:
                    if len(self.synonyms[word])>0:
                        try: html += f'- Synonyms for word {word}: {", ".join(self.synonyms[word])}<br>'
                        except: continue
                    else:
                        html += f'- Synonyms for word {word}: none found.<br>'
                except:
                    continue
            html += '</p>'
        if self.common_ngrams == {}:
            html += 'You didn\'t repeat too many things! Hooray!'
        html += '</div><br><div class="highlight-red" style="padding:10px">'
        for word, correction in self.spelling.items():
            html += f'<p>It seems that <span class="bordered">{word}</span> is misspelled. Here are some possible corrections: '
            if len(correction)>0:
                html += f'{", ".join(correction)}</p>'
            else:
                html += f'no possible corrections found.'
        if self.spelling == {}:
            html += 'No spelling errors! Hooray!'
        html += '</div>'
        print(self.synonyms)
        return html
