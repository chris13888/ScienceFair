import sys

def c(array, mode):
    if mode == 'C':
        return [list(r)[::-1] for r in zip(*array)]
    elif mode == 'A':
        return [list(r) for r in zip(*array)][::-1]
    elif mode == 'V':
        return array[::-1]
    elif mode == 'H':
        return [r[::-1]for r in array]

# data = sys.stdin.read().split('\n')
# output = sys.stdout
output = open('out.txt', 'w')
data = open('test.txt').read().split('\n')

n = int(data.pop(0))

array = [data.pop(0).split() for i in range(n)]

commands = list(data.pop(0))

for command in commands:
    array = c(array, command)
    for line in array: print(*line, file=output)
    print(file=output)
