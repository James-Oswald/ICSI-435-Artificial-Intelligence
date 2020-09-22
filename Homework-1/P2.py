
import numpy as np
from collections import deque

rawTest = {
    "S": {"a":2, "b":3, "d":5},
    "a": {"S":2, "c":4},
    "b": {"S":3, "d":4},
    "c": {"a":4, "d":1, "e":2},
    "d": {"b":4, "S":5, "c":1, "e":5},
    "e": {"c":2, "d":5}
}


rawG3 = {
    "S": {"d":3, "e":9, "p":1},
    "a": {"b":2, "c":2},
    "b": {"a":2, "d":1},
    "c": {"a":2, "d":8, "f":3},
    "d": {"S":3, "b":1, "c":8, "e":2},
    "e": {"d":2, "S":9, "h":8, "r":2},
    "f": {"c":3, "G":2, "r":2},
    "h": {"p":4, "q":4, "e":8},
    "p": {"S":1, "h":4, "q":15},
    "q": {"p":15, "h":4},
    "r": {"e":2, "f":2},
    "G": {"f":2}
}

rawG4 = {
    "S": {"d":3, "e":9, "p":1},
    "a": {},
    "b": {"a":2},
    "c": {"a":2},
    "d": {"b":1, "c":8, "e":2},
    "e": {"h":8, "r":2},
    "f": {"c":3, "G":2},
    "h": {"p":4, "q":4},
    "p": {"q":15},
    "q": {},
    "r": {"f":2},
    "G": {}
}

#letter to number for converting node labels to number
labels = ["S", "a", "b", "c", "d", "e", "f", "h", "p", "q", "r", "G"]
def l2n(l):
    return labels.index(l)
def n2l(n):
    return labels[n]

#convert the raw letter vertex list into a numeric vertex list
def adjList(rawGraph):
    rv = [None] * len(rawGraph)
    for nodeKey in rawGraph:
        rv[l2n(nodeKey)] = {l2n(k):v for (k,v) in rawGraph[nodeKey].items()}
    return rv

#convert the raw letter vertex list into a numeric adjacency matrix
def adjMat(rawGraph):
    aList = adjList(rawGraph)
    aMat = np.zeros((len(aList), len(aList)))
    for i in range(0, len(aList)):
        for elm in aList[i]:
            aMat[i, elm] = aList[i][elm]
    return aMat

print(adjList(rawTest))
print(adjMat(rawTest))

