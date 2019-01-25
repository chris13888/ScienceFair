import pkg_resources
import spacy
import pickle

file = pkg_resources.resource_filename(__name__, '/text/processing.txt')
text = open(file, 'r').read()

model = {}

processor = spacy.load('en_core_web_lg')

doc = processor(text.lower())

print('PROCESSING')
prev_word = '---'
for word in doc:
    if word.is_stop or not word.is_alpha:
        continue
    else:
        if prev_word in model.keys():
            if word.text.lower in model[prev_word].keys():
                model[prev_word][word.text] += 1
                continue
            model[prev_word][word.text] = 1
        else:
            model[prev_word] = {word.text: 1}
        prev_word = word.text

output = pkg_resources.resource_filename(__name__, '/text/model.pickle')
new_model = {}

for key, value in model.items():
    new_model[key] = {}
    total_occurences = sum(value.values())
    for k, v in value.items():
        new_model[key][k] = v/total_occurences

print(new_model)
pickle.dump(new_model, open(output, 'wb'))
