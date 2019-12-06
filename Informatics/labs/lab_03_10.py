from pprint import pprint as pp
# Задание 24
print('Задание 24')



bad_chars = [',', '.', '-', "'"]
textDict = dict()
with open('text1.txt', 'r') as f:
    for line in f:
        for word in line.split():
            for char in bad_chars:
                word = word.replace(char, '')
                
            if word in textDict:
                textDict[word] += 1
            else:
                textDict[word] = 1
                
pp(textDict)