def encodeHuffman(fileIn, fileOut):
    pass

def decodeHuffman(fileIn, fileOut):
    pass

def count_chars(file):
    textDict = dict()
    with open(file, 'r') as f:
        for line in f:
            for char in line:
                if char in textDict:
                    textDict[char] += 1
                else:
                    textDict[char] = 1
    
    return textDict
print(count_chars('sample.txt'))

def probability_of_chars(textDict):
    char_sum = sum(textDict.values())
    for char in textDict:
        textDict[char] = textDict[char] / char_sum
    
    return textDict
    

print(probability_of_chars(count_chars('sample.txt')))