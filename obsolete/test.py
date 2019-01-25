import re
url = 'http://www.casr.ca/ai-boeing-msa-challenger.htm'
thing = re.sub(r'/{2,}', r'/', url).split('/')
if thing[0].startswith('http'):
    thing = thing[1]
else:
    thing = thing[0]
print(thing)
thing = thing.replace('www.', '')
print(thing)
thing = re.sub(r'[\-_]', r' ', thing)
thing = ' '.join(thing.split('.')[:-1]).title()

print(thing)
