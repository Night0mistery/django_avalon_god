import random
items = ['1','2','3','4','4','4']
for i in range(len(items)):
    index = random.randrange(len(items))
    print(items.pop(index))
    print(items)
