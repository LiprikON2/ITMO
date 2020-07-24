from collections import defaultdict
import re

text = "Hello there. General Kenobi! Kenobi Kenobi"


class Tree(defaultdict):
    def __call__(self):
        return Tree(self)

    def __init__(self, parent):
        self.parent = parent
        self.default_factory = self
        self.count = 1

def textToNodes(text):
    wordList = re.sub("[^\w]", " ",  text).split()
    
    tree = Tree(None)
    for i, word in enumerate(wordList):
        for j, letter in enumerate(word):
            tree[i][j] = letter
            
    return tree
            
def recursiveRef(nested, idxList):
    if len(idxList) > 1:
        return recursiveRef(nested[idxList[0]], idxList[1:])
    return nested[idxList[0]] 


myTree = textToNodes(text)

print(recursiveRef(myTree, [5, 0]))
            