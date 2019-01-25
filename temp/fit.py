s = input()
f = input()

processed = []

num = 0
for c in f:
    if c == 'X':
        processed.append(f's[{num}].upper()')
        num += 1
    elif c == 'x':
        processed.append(f's[{num}].lower()')
        num += 1
    else:
        processed.append(f"{c.__repr__()}")
print(eval('+'.join(processed)))
