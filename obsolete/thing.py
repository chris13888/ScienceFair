with open('original.txt', 'r') as rf, open('words.txt', 'w') as wf:
    for line in rf.read().split('\n')[1:]:
        ln = line.split()
        try:
            wf.write('{} {}\n'.format(ln[1], ln[2].replace(',', '')))
        except:
            continue
