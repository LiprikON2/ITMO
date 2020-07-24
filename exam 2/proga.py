import re

text = "Hello there. General Kenobi! Kenobi Kenobi"



class Node:
    def __init__(self, val, rest):
        self.val = val
        self.children = [None] # the pointer initially points to nothing
        self.count = 1
        if rest != None:
            self.val = rest[0]
            self.addWord(rest=rest)
        
        
    def addWord(rest):
        if letter not in self.children:
            self.children.add(Node(rest=rest[1:]))
        else:
            rootNode.children[rootNode.children.index(letter)].count += 1
            # go there
    
    
    
    # def traverse(val):
    #     node = self
    #     while node != None:
    #         print(node.val) # access the node value
    #         node = node.next # move on to the next node



def textToNodes(text):
    wordList = re.sub("[^\w]", " ",  text).split()
    
    rootNode = Node(None, None)
    for word in wordList:
        print('working on:', word)
        
        rootNode.addWord(word)
        return rootNode
            
print(textToNodes(text).children)
        
        
        
# node1 = Node('p')
# node2 = Node('y')
# node3 = Node('t')
# node4 = Node('h')
# node5 = Node('o')
# node6 = Node('n')


# node1.next = [node2]
# node2.next = [node3]
# node3.next = [node4]
# node5.next = [node6]

        

# print(node1.next[0].val)

# textToNodes(text)