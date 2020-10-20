
import math         #used for math.inf

class BinaryTree():
    def __init__(self, name, value=0, flag="leaf"):
        self.left = None        #left subtree
        self.right = None       #right subtree
        self.name = name    #name of the node
        self.value = value      #Value of the node after minimax evaluation or default if leaf
        self.flag = flag        #Flag indicating min node, max node, or leaf

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def getName(self):
        return self.name

    def getChildren(self):
        return [self.left, self.right]

    def getFlag(self):
        return self.flag

    def setNodeValue(self,value):
        self.value = value

    def getNodeValue(self):
        return self.value

    def insertRight(self,newNode, value=0, flag="leaf"):
        if self.right == None:
            self.right = BinaryTree(newNode, value, flag)
        else:
            tree = BinaryTree(newNode, value, flag)
            tree.right = self.right
            self.right = tree
        return self.right

    def insertLeft(self,newNode, value=0, flag="leaf"):
        if self.left == None:
            self.left = BinaryTree(newNode, value, flag)
        else:
            tree = BinaryTree(newNode,value, flag)
            tree.left = self.left
            self.left = tree
        return self.left

def printTree(tree):
    if tree != None:
        printTree(tree.getLeftChild())
        print(tree.getNodeValue())
        printTree(tree.getRightChild())

# setting up the tree data
root = BinaryTree("root", flag="max")
l = root.insertLeft("l", flag="min")
r = root.insertRight("r", flag="min")
ll = l.insertLeft("ll", flag="max")
lr = l.insertRight("lr", flag="max")
rl = r.insertLeft("rl", flag="max")
rr = r.insertRight("rr", flag="max")
lll = ll.insertLeft("lll", flag="min")
llr = ll.insertRight("llr", flag="min")
lrl = lr.insertLeft("lrl", flag="min")
lrr = lr.insertRight("lrr", flag="min")
rll = rl.insertLeft("rll", flag="min")
rlr = rl.insertRight("rlr", flag="min")
rrl = rr.insertLeft("rrl", flag="min")
rrr = rr.insertRight("rrr", flag="min")
lll.insertLeft("llll", value=3)
lll.insertRight("lllr", value=10)
llr.insertLeft("llrl", value=2)
llr.insertRight("llrr", value=9)
lrl.insertLeft("lrll", value=10)
lrl.insertRight("lrlr", value=7)
lrr.insertLeft("lrrl", value=5)
lrr.insertRight("lrrr", value=9)
rll.insertLeft("rlll", value=2)
rll.insertRight("rllr", value=5)
rlr.insertLeft("rlrl", value=6)
rlr.insertRight("rlrr", value=4)
rrl.insertLeft("rrll", value=2)
rrl.insertRight("rrlr", value=7)
rrr.insertLeft("rrrl", value=9)
rrr.insertRight("rrrr", value=1)

def minimaxSearch(node):
    return {                #implmented with a dictionary case switch since its nice and pythonic 
        "leaf": lambda _: node.getNodeValue(),
        "min": lambda _: min(minimaxSearch(node.getLeftChild()), minimaxSearch(node.getRightChild())),
        "max": lambda _: max(minimaxSearch(node.getLeftChild()), minimaxSearch(node.getRightChild()))
    }[node.getFlag()](None) 

print("Performing Minimax Search:")
print("The chosen terminal state: " + str(minimaxSearch(root)) + "\n")

def alphaBetaPrune(node, alpha = -math.inf, beta = math.inf):
    if node.getFlag() == "leaf":        #if we're on a leaf
        return node.getNodeValue()
    elif node.getFlag() == "max":       #if we're on a max node
        v = -math.inf
        for child in node.getChildren():
            v = max(v, alphaBetaPrune(child, alpha, beta))
            if v >= beta:
                print("Pruned " + str(child.getName()) + " alpha: " + str(alpha) + " beta: " + str(beta))
                return v
            alpha = max(alpha, v)
        return v
    elif node.getFlag() == "min":       #if we're on a min node
        v = math.inf
        for child in node.getChildren():
            v = min(v, alphaBetaPrune(child, alpha, beta))
            if v <= alpha:
                print("Pruned " + str(child.getName()) + " alpha: " + str(alpha) + " beta: " + str(beta))
                return v
            beta = min(beta, v)
        return v

print("Performing Minimax Search with alpha-beta pruning:")
print("The chosen terminal state: " + str(alphaBetaPrune(root)))