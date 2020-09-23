
import numpy as np
import queue as Q

#Test set from 00_Search Algo_Solutions.pdf
rawTest = {
    "S": {"a":2, "b":3, "d":5},
    "a": {"S":2, "c":4},
    "b": {"S":3, "d":4},
    "c": {"a":4, "d":1, "e":2},
    "d": {"b":4, "S":5, "c":1, "e":5},
    "e": {"c":2, "d":5}
}

#G3 raw data as an ajacnecy list
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

#G4 raw data as an ajacnecy list
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

def printData(data):
    if data == None:
        print("Goal node not found")
        return
    print("\tStates Expanded: " + str([n2l(e) for e in data[0]]))
    print("\tPath Returned:   " + str([n2l(e) for e in data[1]]))

#print(adjList(rawTest))
#print(adjMat(rawTest))

def ucsMat(graph, start, end):
    queue = Q.PriorityQueue()
    queue.put((1, start))
    pathDict = {}
    expanded = [start]
    visited = [False for i in range(len(graph))]
    cumulativeCost = 0
    while not queue.empty():
        maxPriority = queue.get()
        visited[maxPriority[1]] = True
        #path.append(maxPriority[1])
        cumulativeCost = maxPriority[0]
        if maxPriority[1] == end:
            path = []
            back = end          #path calculation
            while back != start:
                path.append(back)
                back = pathDict[back]
            path.append(start)
            return expanded, list(reversed(path))
        edges = [(i, graph[maxPriority[1], i]) for i in range(0, len(graph[maxPriority[1]])) if graph[maxPriority[1], i] != 0]
        for (node, weight) in edges:
            if not visited[node]:
                if node not in expanded:
                    expanded.append(node)
                queue.put((cumulativeCost + weight, node))
                pathDict[node] = maxPriority[1]
    return None

def ucsList(graph, start, end):
    queue = Q.PriorityQueue()
    queue.put((0, start))
    pathDict = {}
    expanded = [start]
    visited = [False for i in range(len(graph))]
    cumulativeCost = 0
    while not queue.empty():
        maxPriority = queue.get()
        visited[maxPriority[1]] = True
        cumulativeCost = maxPriority[0]
        if maxPriority[1] == end:
            path = []
            back = end          #path calculation
            while back != start:
                path.append(back)
                back = pathDict[back]
            path.append(start)
            return expanded, list(reversed(path))
        edges = graph[maxPriority[1]].items()
        for (node, weight) in edges:
            if not visited[node]:
                if node not in expanded:
                    expanded.append(node)
                pathDict[node] = maxPriority[1]
                queue.put((cumulativeCost + weight, node))
    return None

print("P2) Perform UCS on weighted graph G3 and G4.")
print("Given the undirected weighted graph G3 represented as vertex-list: Perform UCS using PQ. (2pt)")
printData(ucsList(adjList(rawG3), l2n("S"), l2n("G")))
print("Given the undirected graph G3 represented as adjacency matrix: Perform UCS using PQ. (2pt)")
printData(ucsMat(adjMat(rawG3), l2n("S"), l2n("G")))
print("Given the directed weighted graph G4 represented as vertex-list: Perform UCS using PQ. (2pt)")
printData(ucsList(adjList(rawG4), l2n("S"), l2n("G")))
print("Given the directed weighted graph G4 represented as adjacency matrix:Perform UCS using PQ. (2pt)")
printData(ucsMat(adjMat(rawG4), l2n("S"), l2n("G")))
